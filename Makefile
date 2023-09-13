DATA_HOME = ./data

# --------------------------------------
#               WORKFLOWS
# --------------------------------------
.PHONY: crawl deploy

crawl: setup seed regen pushs3

deploy: crawl zip deploy-flyio

# --------------------------------------
#               SETUP
# --------------------------------------
.PHONY: setup

QUIET := -q

setup:
	pip install pip -Uq
	pip install poetry==1.3.0 $(QUIET)
	poetry install $(QUIET)

# --------------------------------------
#           ARTICLE CRAWLING
# --------------------------------------
.PHONY: crawl

crawl: setup pulls3-urls
	cat newspapers.json | jq '.[].name' | xargs -n 1 -I {} scrapy crawl {} -o $(DATA_HOME)/articles/{}.jsonl -L DEBUG

# --------------------------------------
#             WEB APP
# --------------------------------------
.PHONY: app zip

PORT=8004

app: setup
	uvicorn climatedb.app:app --reload --port $(PORT) --host 0.0.0.0 --proxy-headers

zip:
	cd $(DATA_HOME); zip -r ./climate-news-db-dataset.zip ./* -x "./html/*" -x "./opinions/*"

deploy-flyio:
	flyctl deploy --wait-timeout 360

# --------------------------------------
#             DATABASE
# --------------------------------------
.PHONY: seed regen

seed:
	mkdir -p $(DATA_HOME)/articles
	python scripts/seed.py

regen: seed
	python scripts/regen_database.py

# --------------------------------------
#                S3
# --------------------------------------
.PHONY: pulls3 pulls3-urls pushs3

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

# --------------------------------------
#             AWS INFRA
# --------------------------------------

.PHONY: run-search-lambdas infra

infra:
	cd infra && npx --yes aws-cdk@2.92.0 deploy -vv --all

# --------------------------------------
#               CHECK
# --------------------------------------
.PHONY: check static

check: setup
	ruff check climatedb infra scripts

static: setup
	mypy climatedb
	mypy tests

# --------------------------------------
#               TEST
# --------------------------------------
.PHONY: test test-ci

test: setup
	pytest tests -x --lf -s

test-ci: setup
	coverage run -m pytest tests --showlocals --full-trace --tb=short --show-capture=no -v -s
	coverage report -m

# --------------------------------------
#               DEV
# --------------------------------------

gpt:
	python ./climatedb/gpt.py

run-search-lambdas:
	python scripts/run-search-lambdas.py

crawl-one:
	scrapy crawl $(PAPER) -L DEBUG -o $(DATA_HOME)/articles/$(PAPER).jsonlines

