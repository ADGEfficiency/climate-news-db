PROJECT_NAME = climate-news-db
PROJECT_HOME = $(HOME)/$(PROJECT_NAME)/data

init:
	pip install -r requirements.txt
	pip install --editable .
	make init-data

init-data:
	mkdir -p "$(PROJECT_HOME)/raw"
	mkdir -p "$(PROJECT_HOME)/final"

clean:
	rm -rf "$(PROJECT_HOME)"
	make init-data

app:
	python3 app.py

pushs3:
	aws s3 sync $(PROJECT_HOME)/s3 s3://climate-nlp

pulls3:
	mkdir -p "$(PROJECT_HOME)/s3"
	aws s3 sync s3://climate-nlp $(PROJECT_HOME)/s3 --exclude 'raw/*'

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
