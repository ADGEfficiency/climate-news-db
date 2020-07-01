setup:
	pip install -r requirements.txt

clean:
	rm -rf ~/climate-nlp

app:
	python app.py
