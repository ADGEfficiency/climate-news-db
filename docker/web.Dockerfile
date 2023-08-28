FROM python:3.10.11

RUN apt-get update && apt-get install -y cron

WORKDIR /app

COPY ./poetry.lock ./pyproject.toml ./poetry.toml ./Makefile ./
COPY ./climatedb ./climatedb
COPY ./static ./static
COPY ./templates ./templates
COPY ./docker/web-entrypoint.sh ./entrypoint.sh
COPY ./data/db.sqlite ./data/db.sqlite
COPY ./data/climate-news-db-dataset.zip ./data/climate-news-db-dataset.zip
COPY ./newspapers.json ./newspapers.json

RUN make setup QUIET= && chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
