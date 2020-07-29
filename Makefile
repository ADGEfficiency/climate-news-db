setup:
	pip install -r requirements.txt

clean:
	rm -rf ~/climate-nlp/final
	rm -rf ~/climate-nlp/raw

app:
	python app.py

inspect:
	./inspect.sh

regen:
	python3 download.py --num -1 --newspapers all --source urls.data

push_s3:
	aws s3 sync ~/climate-nlp s3://climate-nlp --delete

pull_s3:
	aws s3 sync s3://climate-nlp ~/climate-nlp --exclude 'raw/*'

scrape:
	make pull_s3
	python3 download.py --num 10 --newspapers all --source google
	make push_s3
