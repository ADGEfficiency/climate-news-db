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

scrape:
	make pulls3
	dbcollect all --num 5 --source google --parse
	python3 climatedb/heal.py
	make pushs3

collect-urls:
	make pulls3
	dbcollect all --num 5 --source google --noparse
	python3 climatedb/heal.py
	make pushs3
