setup:
	pip install -r requirements.txt

clean:
	rm -rf ~/climate-nlp/final
	rm -rf ~/climate-nlp/raw

app:
	python app.py

inspect:
	./inspect.sh
