include .env
-include .env.secret
export

all: app
scrape: setup pulls3 create_urls scrapy db zip pushs3 docker-push

#  S3

#  these come from .env
S3_DIR = s3://$(S3_BUCKET)/$(DATA_DIR)

pulls3:
	aws --no-sign-request --region ap-southeast-2 s3 sync $(S3_DIR) $(DATA_HOME) --exclude 'raw/*' --exclude 'temp/*' --exclude 'article_body/*'

pulls3-urls:
	aws --no-sign-request --region ap-southeast-2 s3 cp $(S3_DIR)/urls.jsonl $(DATA_HOME)/urls.jsonl --exclude 'raw/*' --exclude 'temp/*' --exclude 'article_body/*'

pushs3:
	aws s3 sync $(DATA_HOME) $(S3_DIR) --exclude 'logs/*' --exclude 'temp/*' --exclude 'article_body/*'

#  SCRAPE

setup:
	pip install poetry -q
	poetry config virtualenvs.create false --local
	poetry install -q

create_urls:
	python3 scripts/create_urls_csv.py

LOG := INFO
scrapy: create_urls
	cat ./data-neu/newspapers.json | jq 'keys[]' | xargs -n 1 -I {} scrapy crawl {} -o $(DATA_HOME)/articles/{}.jsonlines -L $(LOG)

db: scrapy
	rm -rf $(DB_FI)
	python3 scripts/create_sqlite_papers.py
	cat ./data-neu/newspapers.json | jq 'keys[]' | xargs -n 1 -I {} python ./scripts/create_sqlite_one.py {}
	python3 scripts/create_sqlite_app.py

#  SCRAPE INFRA

STAGE ?= dev

ACCOUNTNUM=$(shell aws sts get-caller-identity --query "Account" --output text)
AWSPROFILE=default
IMAGENAME=climatedb-$(STAGE)

./node_modules/serverless/README.md:
	npm install serverless
sls-setup: ./node_modules/serverless/README.md

infra: docker-aws infra-aws

docker-aws:
	sh build-docker-image.sh $(ACCOUNTNUM) climatedb-dev lambda.Dockerfile $(AWSPROFILE)

infra-aws: sls-setup
	npx serverless deploy -s $(STAGE) --param account=$(ACCOUNTNUM) --verbose

#  WEBAPP

app: setup
	uvicorn app:app --reload

#  WEBAPP INFRA

docker-setup:
	sudo snap install docker
	sudo snap install --classic heroku

docker-push:
	sudo heroku auth:token | sudo docker login --username=_ registry.heroku.com --password-stdin
	sudo heroku container:push web -a climate-news-db --recursive
	sudo heroku container:release web -a climate-news-db

#  UTILS

clean:
	rm -rf $(DATA_HOME)/articles/* $(DATA_HOME)/db.sqlite $(DATA_HOME)/urls.csv

datasette:
	datasette $(DB_FI)

scrape-one:
	scrapy crawl $(PAPER) -L DEBUG -o $(DATA_HOME)/articles/$(PAPER).jsonlines

zip:
	cd $(DATA_HOME); zip -r ./climate-news-db-dataset.zip ./* -x "./html/*"

check:
	ruff check .
	djlint . --extension=html --check --profile jinja

format:
	isort . --profile black
	black .
	ruff check . --fix-only
