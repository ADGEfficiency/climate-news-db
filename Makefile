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
	python3 download.py --num -1 --newspapers all --url_source urls.data

push_s3:
	aws s3 sync --delete ~/climate-nlp s3://climate-nlp

pull_s3:
	aws s3 sync s3://climate-nlp ~/climate-nlp
