setup:
	pip install -r requirements.txt

clean:
	rm -rf ~/climate-nlp/final
	rm -rf ~/climate-nlp/raw

deploy:
	python app.py

inspect:
	./inspect.sh

regen:
	python3 download.py --num -1 --newspapers all --url_source urls.data
