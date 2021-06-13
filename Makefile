PROJECT_NAME = climate-news-db
PROJECT_HOME = $(HOME)/$(PROJECT_NAME)/data
S3_DIR = climate-news-db

setup:
	pip install -r requirements.txt
	pip install --editable .
	make init-data

init-data:
	mkdir -p $(PROJECT_HOME)/raw
	mkdir -p $(PROJECT_HOME)/final

app:
	python3 app.py

pushs3:
	aws s3 sync $(PROJECT_HOME) s3://$(S3_DIR) --exclude 'logs/*' --exclude 'temp/*' --profile adg

pulls3:
	aws s3 sync s3://$(S3_DIR) $(PROJECT_HOME) --exclude 'raw/*' --profile adg

scrape:
	make pulls3
	dbcollect all --num 5 --source google --parse
	make pushs3

parse:
	make pulls3
	dbcollect all --num 0 --no-search
	make pushs3

datasette:
	datasette $(PROJECT_HOME)/climatedb.sqlite

test:
	pytest tests

migrate:
	rm -rf data/climatedb.sqlite
	python3 scripts/migrate_to_sqlite.py
	cd data; zip -r ./climate-news-db-dataset.zip ./climate-news-db-dataset.csv ./article_body/

status:
	./scripts/status.sh
