setup:
	pip install pip -Uq
	pip install poetry==1.3.0 -q
	poetry install

check:
	ruff check . --fix-only

static:
	mypy climatedb
	mypy tests

test:
	pytest tests

scrape: crawl

DATA_HOME = ./data-neu
crawl:
	# cat newspapers.json | jq 'keys[]' | xargs -n 1 -I {} scrapy crawl {} -o $(DATA_HOME)/articles/{}.jsonlines -L DEBUG

crawl-one:
	scrapy crawl $(PAPER) -L DEBUG -o $(DATA_HOME)/articles/$(PAPER).jsonlines
