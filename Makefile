include .env
export

#  these come from .env
S3_DIR = s3://$(S3_BUCKET)/$(DATA_DIR)

#  gets the keys of newspapers.json as a list
PAPERS:=$(shell cat $(DATA_HOME)/newspapers.json | jq 'keys[]')

all: app

#  DATA PIPELINE

pipe: db

setup:
	pip install -r requirements.txt -q
	pip install --editable . -q

setup-neu: poetry
	poetry config virtualenvs.create false --local
	poetry install

$(HOME)/.poetry/bin:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
poetry: $(HOME)/.poetry/bin

$(DATA_HOME)/urls.csv: $(DATA_HOME)/urls.jsonl scripts/create_urls_csv.py
	python3 scripts/create_urls_csv.py

$(DATA_HOME)/articles/$(PAPERS).jsonlines: $(DATA_HOME)/urls.csv
	echo $(PAPERS) | xargs -n 1 -I {} -- scrapy crawl {} -o $(DATA_HOME)/articles/{}.jsonlines -L INFO

scrapy: $(DATA_HOME)/articles/$(PAPERS).jsonlines

db: setup scrapy
	rm -rf $(DB_FI)
	python3 scripts/create_sqlite.py

#  APP

app:
	uvicorn app:app --reload

#  S3

pushs3:
	aws s3 sync $(DATA_HOME) $(S3_DIR) --exclude 'logs/*' --exclude 'temp/*' --exclude 'article_body/*'

pulls3:
	aws s3 sync $(S3_DIR) $(DATA_HOME) --exclude 'raw/*' --exclude 'temp/*' --exclude 'article_body/*'

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

# .SILENT: infra

AWSPROFILE=adg
IMAGENAME=climatedb-$(STAGE)

docker:
	./build-docker-image.sh $(ACCOUNTNUM) $(IMAGENAME) ./Dockerfile $(AWSPROFILE)

infra: sls-setup docker
	npx serverless deploy -s $(STAGE) --param account=$(ACCOUNTNUM) --verbose
