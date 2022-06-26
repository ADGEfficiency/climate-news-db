include .env
export

#  these come from .env
S3_DIR = s3://$(S3_BUCKET)/$(DATA_DIR)

#  gets the keys of newspapers.json as a list
PAPERS:=$(shell cat $(DATA_HOME)/newspapers.json | jq 'keys[]')

all: app


#  S3

pulls3:
	aws s3 sync $(S3_DIR) $(DATA_HOME) --exclude 'raw/*' --exclude 'temp/*' --exclude 'article_body/*'
pushs3:
	aws s3 sync $(DATA_HOME) $(S3_DIR) --exclude 'logs/*' --exclude 'temp/*' --exclude 'article_body/*' --exclude 'urls.jsonl'


#  DATA PIPELINE

setup:
	pip install poetry -q
	poetry config virtualenvs.create false --local
	poetry install -q

$(DATA_HOME)/urls.csv: $(DATA_HOME)/urls.jsonl scripts/create_urls_csv.py
	python3 scripts/create_urls_csv.py
create_urls: $(DATA_HOME)/urls.csv

scrapy: $(DATA_HOME)/urls.csv
	cat ./data-neu/newspapers.json | jq 'keys[]' | xargs -n 1 -I {} scrapy crawl {} -o $(DATA_HOME)/articles/{}.jsonlines -L INFO

db: scrapy
	rm -rf $(DB_FI)
	python3 scripts/create_sqlite.py

#  not pulling s3 here - will put in later
scrape: setup pulls3 create_urls scrapy db zip pushs3 docker-push

cron-scrape:
	touch "./cron-logs/$(shell date '+%F %T')"


#  APP

app:
	uvicorn app:app --reload


#  UTILS

clean:
	rm -rf $(DATA_HOME)/articles/* $(DATA_HOME)/db.sqlite $(DATA_HOME)/urls.csv

datasette:
	datasette $(DB_FI)

scrape-one:
	scrapy crawl $(PAPER) -L DEBUG -o $(DATA_HOME)/articles/$(PAPER).jsonlines

dbnodep:
	rm -rf $(DB_FI)
	python3 scripts/create_sqlite.py

zip:
	cd $(DATA_HOME); zip -r ./climate-news-db-dataset.zip ./*


#  INFRA

ACCOUNTNUM=$(shell aws sts get-caller-identity --query "Account" --output text)

./node_modules/serverless/README.md:
	npm install serverless
sls-setup: ./node_modules/serverless/README.md

AWSPROFILE=adg
IMAGENAME=climatedb-$(STAGE)

infra: sls-setup
	sh build-docker-image.sh $(ACCOUNTNUM) climatedb-dev lambda.Dockerfile $(AWSPROFILE)
	npx serverless deploy -s $(STAGE) --param account=$(ACCOUNTNUM) --verbose

docker-setup:
	sudo snap install docker
	sudo snap install --classic heroku

docker-push:
	sudo heroku auth:token | sudo docker login --username=_ registry.heroku.com --password-stdin
	mkdir -p clear-docker-cache
	touch "clear-docker-cache/$(shell date)"
	sudo heroku container:push web -a climate-news-db --recursive
	sudo heroku container:release web -a climate-news-db

inspect:
	python3 scripts/inspect.py
# 	echo $(PAPERS) | xargs -n 1 -I {} -- wc -l $(DATA_HOME)/articles/{}.jsonlines

