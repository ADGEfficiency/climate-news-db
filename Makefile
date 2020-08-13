setup:
	pip install -r requirements.txt

clean:
	rm -rf ~/climate-nlp/final
	rm -rf ~/climate-nlp/raw

app:
	python3 app.py

inspect:
	./inspect.sh

regen:
	parse --num -1 --newspapers all --source urls.data

push_s3:
	aws s3 sync ~/climate-nlp/final s3://climate-nlp/final --delete
	aws s3 sync ~/climate-nlp/raw s3://climate-nlp/raw

pull_s3:
	aws s3 sync s3://climate-nlp ~/climate-nlp --exclude 'raw/*'

scrape:
	make pull_s3
	collect --num 10 --newspapers all --source google
	python3 backward.py
	make push_s3
	touch /var/www/www_climate-news-db_com_wsgi.py
