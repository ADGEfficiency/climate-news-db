setup:
	pip install -r requirements.txt
	pip install --editable .

app:
	python3 app.py

inspect:
	./inspect.sh

pushs3:
	aws s3 sync ~/climate-news-db-data s3://climate-nlp

pulls3:
	aws s3 sync s3://climate-nlp ~/climate-news-db-data --exclude 'raw/*'

heal-db:
	python3 climatedb/heal.py

scrape:
	make pulls3
	dbcollect all --num 5 --source google --parse
	make pushs3

collect-urls:
	make pulls3
	dbcollect all --num 5 --source google --no-parse
	make pushs3
