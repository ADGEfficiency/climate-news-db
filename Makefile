setup:
	pip install -r requirements.txt
	pip install --editable .

app:
	python3 app.py

inspect:
	./inspect.sh

push_s3:
	aws s3 sync ~/climate-news-db-data s3://climate-nlp

pull_s3:
	aws s3 sync s3://climate-nlp ~/climate-news-db-data --exclude 'raw/*'

scrape:
	make pull_s3
	dbcollect all --num 10 --source google --parse
	python3 climatedb/heal.py
	make push_s3
	touch /var/www/www_climate-news-db_com_wsgi.py

selenium-mac:
	wget https://github.com/mozilla/geckodriver/releases/download/v0.27.0/geckodriver-v0.27.0-macos.tar.gz
	tar -xf geckodriver-v0.27.0-macos.tar.gz
	mv geckodriver /usr/local/bin

selenium-mac-chrome:
	wget https://chromedriver.storage.googleapis.com/86.0.4240.22/chromedriver_mac64.zip
	unzip chromedriver_mac64.zip
