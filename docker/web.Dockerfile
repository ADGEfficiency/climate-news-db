FROM python:3.10.11

RUN apt-get update && apt-get install -y cron

WORKDIR /app

COPY ./poetry.lock ./pyproject.toml ./poetry.toml ./Makefile ./
COPY ./climatedb ./climatedb
COPY ./static ./static
COPY ./templates ./templates
COPY ./docker/web-entrypoint.sh ./entrypoint.sh
COPY ./data/db.sqlite ./data/db.sqlite

RUN make setup && chmod +x ./entrypoint.sh && make setup-cron-jobs
ENTRYPOINT ["./entrypoint.sh"]
