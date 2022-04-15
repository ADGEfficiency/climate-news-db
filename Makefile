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
	aws s3 sync $(DATA_HOME) $(S3_DIR) --exclude 'logs/*' --exclude 'temp/*' --exclude 'article_body/*'


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

db: scrape-pipe
	rm -rf $(DB_FI)
	python3 scripts/create_sqlite.py

scrape: pulls3 setup create_urls scrapy db pushs3


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

inspect:
	echo $(PAPERS) | xargs -n 1 -I {} -- wc -l $(DATA_HOME)/articles/{}.jsonlines

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

docker-local:
	docker build -t climatedb-app-local . -f Dockerfile.web
docker-run:
	docker run -d --name climatedb-app-local -p 80:80 climatedb-app-local

docker-heroku:
	git add -u
	git commit -m 'heroku deploy'
	git push heroku tech/feb-2022-rebuild:main

infra: sls-setup
	npx serverless deploy -s $(STAGE) --param account=$(ACCOUNTNUM) --verbose

docker-setup:
	sudo snap install docker
	sudo snap install --classic heroku

docker-push:
	sudo heroku container:push web -a climate-news-db --recursive
	heroku container:release web -a climate-news-db
