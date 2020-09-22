setup:
	pip install -r requirements.txt
	python3 setup.py install

app:
	python3 app.py

inspect:
	./inspect.sh

push_s3:
	aws s3 sync ~/climate-nlp s3://climate-nlp

pull_s3:
	aws s3 sync s3://climate-nlp ~/climate-nlp --exclude 'raw/*'

scrape:
	make pull_s3
	collect all --num 20 --source google --parse
	python3 climatedb/heal.py
	make push_s3
	touch /var/www/www_climate-news-db_com_wsgi.py
