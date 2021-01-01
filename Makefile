PROJECT_NAME = climate-news-db
PROJECT_HOME = $(HOME)/$(PROJECT_NAME)/data
S3_DIR = climate-news-db

init:
	pip install -r requirements.txt
	pip install --editable .
	make init-data

init-data:
	mkdir -p $(PROJECT_HOME)/raw
	mkdir -p $(PROJECT_HOME)/final

clean:
	rm -rf "$(PROJECT_HOME)/raw"
	rm -rf "$(PROJECT_HOME)/final"
	make init-data

app:
	python3 app.py

pushs3:
	aws s3 sync $(PROJECT_HOME) s3://$(S3_DIR) --exclude 'logs/*'

pulls3:
	aws s3 sync s3://$(S3_DIR) $(PROJECT_HOME) --exclude 'raw/*'

scrape:
	make pulls3
	dbcollect all --num 5 --source google --parse
	make pushs3

collect-urls:
	make pulls3
	dbcollect all --num 5 --source google --no-parse
	make pushs3

datasette:
	datasette $(PROJECT_HOME)/climatedb.sqlite

test:
	pytest climatedb/tests

migrate:
	python3 scripts/migration/create_urls_json.py

status:
	./scripts/status.sh
