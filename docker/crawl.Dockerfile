FROM --platform=linux/amd64 python:3.11.4-alpine
RUN apk update
RUN apk add make automake gcc g++ subversion
WORKDIR /app
COPY Makefile pyproject.toml poetry.lock ./
RUN make setup QUIET=
COPY docker/crawl-entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh
CMD ["./entrypoint.sh"]
