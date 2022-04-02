FROM python:3.9

WORKDIR /code

#  setup python
COPY ./pyproject.toml /code/pyproject.toml
COPY ./poetry.lock /code/poetry.lock
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

#  move newspaper data
COPY ./data-neu/db.sqlite /code/data-neu/db.sqlite
COPY ./data-neu/newspapers.json /code/data-neu/newspapers.json
ENV DB_URI sqlite:////code/data-neu/db.sqlite

#  move source
COPY . /code

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
