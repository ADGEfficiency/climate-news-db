setup:
	pip install pip -Uq
	pip install poetry==1.3.0 -q
	poetry install

check: setup
	ruff check .

static: setup
	mypy climatedb
	mypy tests

test: setup
	pytest tests -x --lf

test-ci:
	coverage run -m pytest tests --showlocals --full-trace --tb=short --show-capture=no -v
	coverage report -m

scrape: crawl

DATA_HOME = ./data-neu
crawl:
	cat newspapers.json | jq 'keys[]' | xargs -n 1 -I {} scrapy crawl {} -o $(DATA_HOME)/articles/{}.jsonl -L DEBUG

crawl-one:
	scrapy crawl $(PAPER) -L DEBUG -o $(DATA_HOME)/articles/$(PAPER).jsonlines

app: setup
	uvicorn climatedb.app:app --reload --port 8004
