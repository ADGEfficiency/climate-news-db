PROJECT_NAME = climate-news-db
PROJECT_HOME = $(HOME)/$(PROJECT_NAME)/data
S3_DIR = climate-news-db

S3_BUCKET = climate-news-db
DATA_DIR = data-neu
DATA_HOME = $(HOME)/climate-news-db/$(DATA_DIR)
DB_FI = $(DATA_HOME)/db.sqlite
DB_URI = sqlite:////$(DB_FI)

export DATA_HOME
export DB_URI

all: app

old-pipe: pulls3 collect clean migrate pushs3

collect:
	dbcollect all --num 0 --no-search --no-replace

migrate:
	rm -rf data/climatedb.sqlite
	python3 scripts/migrate_to_sqlite.py
	cd data; zip -r ./climate-news-db-dataset.zip ./climate-news-db-dataset.csv ./article_body/

# pushs3:
# 	aws s3 sync $(PROJECT_HOME) s3://$(S3_DIR) --exclude 'logs/*' --exclude 'temp/*' --exclude 'article_body/*' --profile adg

# pulls3:
# 	aws s3 sync s3://$(S3_DIR) $(PROJECT_HOME) --exclude 'raw/*' --exclude 'temp/*' --exclude 'article_body/*' --profile adg

setup-ol:
	pip install -r requirements.txt
	pip install --editable .
	make init-data

init-data:
	mkdir -p $(PROJECT_HOME)/raw
	mkdir -p $(PROJECT_HOME)/final

# app:
# 	export DATA_HOME=$(DATA_HOME); export DB_URI=$(DB_URI); python3 neuapp.py

datasette:
	datasette $(PROJECT_HOME)/climatedb.sqlite

test:
	pytest tests

status:
	./scripts/status.sh

#  REWORK
#
setup:
	pip install -r requirements.txt -q
	pip install --editable .

#  gets the keys of newspapers.json as a list
papers:=$(shell cat $(DATA_HOME)/newspapers.json | jq 'keys[]')

$(DATA_HOME)/urls.csv: $(DATA_HOME)/urls.txt scripts/create_urls_csv.py
	python3 scripts/create_urls_csv.py

$(DATA_HOME)/articles/$(PAPERS).jsonlines: $(DATA_HOME)/urls.csv
	echo $(papers) | xargs -n 1 -I {} -- scrapy crawl {} -o $(DATA_HOME)/articles/{}.jsonlines -L INFO

scrapy: $(DATA_HOME)/articles/$(PAPERS).jsonlines

scrape-one:
	scrapy crawl $(PAPER) -o $(DATA_HOME)/articles/$(PAPER).jsonlines -L DEBUG

db: setup scrapy
# db:
	rm -rf $(DB_FI)
	python3 scripts/create_sqlite.py

pipe: db

app:
	uvicorn neuapp:app --reload

inspect:
	echo $(papers) | xargs -n 1 -I {} -- wc -l $(DATA_HOME)/articles/{}.jsonlines

S3_DIR = s3://$(S3_BUCKET)/$(DATA_DIR)
pushs3:
	aws s3 sync $(DATA_HOME) $(S3_DIR)  --exclude 'logs/*' --exclude 'temp/*' --exclude 'article_body/*'

pulls3:
	aws s3 sync $(S3_DIR) $(DATA_HOME) --exclude 'raw/*' --exclude 'temp/*' --exclude 'article_body/*'

clean:
	rm -rf $(DATA_HOME)/articles/* $(DATA_HOME)/db.sqlite $(DATA_HOME)/urls.csv
deep-clean: clean
	rm -rf $(DATA_HOME)/urls.csv
