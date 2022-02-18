PROJECT_NAME = climate-news-db
PROJECT_HOME = $(HOME)/$(PROJECT_NAME)/data
S3_DIR = climate-news-db

pipe: pulls3 collect clean migrate pushs3

collect:
	dbcollect all --num 0 --no-search --no-replace

migrate:
	rm -rf data/climatedb.sqlite
	python3 scripts/migrate_to_sqlite.py
	cd data; zip -r ./climate-news-db-dataset.zip ./climate-news-db-dataset.csv ./article_body/

clean:
	python3 scripts/clean_urls_json.py

pushs3:
	aws s3 sync $(PROJECT_HOME) s3://$(S3_DIR) --exclude 'logs/*' --exclude 'temp/*' --exclude 'article_body/*' --profile adg

pulls3:
	aws s3 sync s3://$(S3_DIR) $(PROJECT_HOME) --exclude 'raw/*' --exclude 'temp/*' --exclude 'article_body/*' --profile adg

setup:
	pip install -r requirements.txt
	pip install --editable .
	make init-data

init-data:
	mkdir -p $(PROJECT_HOME)/raw
	mkdir -p $(PROJECT_HOME)/final

app:
	python3 app.py

datasette:
	datasette $(PROJECT_HOME)/climatedb.sqlite

test:
	pytest tests

status:
	./scripts/status.sh

scrapy:
	scrapy startproject climate_news_db
