FROM python:3.10.11

WORKDIR /app

COPY ./poetry.lock ./pyproject.toml ./poetry.toml ./Makefile ./
COPY ./climatedb ./climatedb
COPY ./static ./static
COPY ./templates ./templates

RUN make setup
RUN make restore-down -o setup
RUN make replicate -o setup
CMD ["make", "app", "-o", "setup", "PORT=8080"]
