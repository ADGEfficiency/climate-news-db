.PHONY: all
all: app

DATA_HOME = ./data

# SETUP
.PHONY: setup

QUIET := -q

setup:
	pip install pip -Uq
	pip install poetry==1.3.0 $(QUIET)
	poetry install $(QUIET)

# CHECK
.PHONY: check static

check: setup
	ruff check .

static: setup
	mypy climatedb
	mypy tests

# TEST
.PHONY: test test-ci

test: setup
	pytest tests -x --lf -s

test-ci:
	coverage run -m pytest tests --showlocals --full-trace --tb=short --show-capture=no -v -s
	coverage report -m

# DATABASE
.PHONY: setup-cron-jobs seed db-regen gpt pulls3 pulls3-urls pushs3

setup-cron-jobs:
	# echo "*/5 * * * * root cd /app && make restore-down" > /etc/cron.d/restore-down
	# chmod 0644 /etc/cron.d/restore-down
	# echo "* * * * * root echo 'ran-cron'" > /etc/cron.d/hello
	# chmod 0644 /etc/cron.d/hello
	echo "TODO - will setup litestream replication on webapp server here"

seed:
	mkdir -p $(DATA_HOME)
	python scripts/seed.py

db-regen: seed
	python scripts/regen_database.py

gpt:
	python ./climatedb/gpt.py

S3_BUCKET=$(shell aws cloudformation describe-stacks --stack-name ClimateNewsDB --region ap-southeast-2 --query 'Stacks[0].Outputs[?OutputKey==`BucketNameOutput`].OutputValue' --output text)
S3_DIR=s3://$(S3_BUCKET)

pulls3:
	aws --region ap-southeast-2 s3 sync $(S3_DIR) $(DATA_HOME) --exclude 'html/*'

pulls3-urls:
	echo "$(shell wc -l $(DATA_HOME)/urls.jsonl) urls"
	aws --region ap-southeast-2 s3 cp $(S3_DIR)/urls.jsonl $(DATA_HOME)/urls.jsonl
	echo "$(shell wc -l $(DATA_HOME)/urls.jsonl) urls"

pushs3:
	aws s3 sync $(DATA_HOME) $(S3_DIR)

#  INFRA
.PHONY: cdk run-search-lambdas aws-infra deploy

cdk:
	cd infra && npx --yes aws-cdk@2.75.0 deploy -vv --all

run-search-lambdas:
	python scripts/run-search-lambdas.py

aws-infra: cdk

deploy: crawl-cloud
	flyctl deploy --wait-timeout 120

# ARTICLE CRAWLING
.PHONY: crawl crawl-one crawl-cloud

crawl: pulls3-urls
	cat newspapers.json | jq '.[].name' | xargs -n 1 -I {} scrapy crawl {} -o $(DATA_HOME)/articles/{}.jsonl -L DEBUG

crawl-one:
	scrapy crawl $(PAPER) -L DEBUG -o $(DATA_HOME)/articles/$(PAPER).jsonlines

crawl-cloud: seed db-regen crawl pushs3

# WEB APP
.PHONY: app zip

PORT=8004
app: setup
	uvicorn climatedb.app:app --reload --port $(PORT) --host 0.0.0.0 --proxy-headers

zip:
	cd $(DATA_HOME); zip -r ./climate-news-db-dataset.zip ./* -x "./html/*" -x "./opinions/*"

