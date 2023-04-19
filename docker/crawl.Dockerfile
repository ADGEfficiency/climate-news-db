FROM python:3.10.11
COPY ../../poetry.lock ../../pyproject.toml ../../poetry.toml /
RUN pip --no-cache-dir install poetry==1.3.0 && poetry install --no-interaction --no-ansi
CMD ["echo", "running"]
