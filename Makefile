
.PHONY: setup
setup:
	pip install pip -Uq
	pip install poetry==1.3.0 -q
	poetry install

# CHECK
.PHONY: check
check: setup
	ruff check .

.PHONY: static
static: setup
	mypy climatedb
	mypy tests

# TEST

test: setup
	pytest tests -x --lf

test-ci:
	coverage run -m pytest tests --showlocals --full-trace --tb=short --show-capture=no -v
	coverage report -m

# CRAWLING & SCRAPING

DATA_HOME = ./data
crawl:
	cat newspapers.json | jq '.[].name' | xargs -n 1 -I {} scrapy crawl {} -o $(DATA_HOME)/articles/{}.jsonl -L DEBUG

crawl-one:
	scrapy crawl $(PAPER) -L DEBUG -o $(DATA_HOME)/articles/$(PAPER).jsonlines

# WEB APP

app: setup
	uvicorn climatedb.app:app --reload --port 8004

# DATABASE

seed:
	mkdir -p $(DATA_HOME)
	python scripts/seed.py

db-regen: seed
	python scripts/regen_database.py

S3_BUCKET=$(shell aws cloudformation describe-stacks --stack-name ClimatedbStack --region ap-southeast-2 --query 'Stacks[0].Outputs[?OutputKey==`BucketNameOutput`].OutputValue' --output text)
S3_DIR=s3://$(S3_BUCKET)
DATA_HOME=./data

.PHONY: pulls3 pulls3-urls pushs3
pulls3:
	aws --no-sign-request --region ap-southeast-2 s3 sync $(S3_DIR) $(DATA_HOME) --exclude 'html/*'
pulls3-urls:
	aws --region ap-southeast-2 s3 cp $(S3_DIR)/urls.jsonl $(DATA_HOME)/urls.jsonl
pushs3:
	aws s3 sync $(DATA_HOME) $(S3_DIR)

#  INFRA
.PHONY: infra
infra:
	cd infra && npx --yes aws-cdk@2.75.0 deploy
