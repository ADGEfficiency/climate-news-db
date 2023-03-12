FROM public.ecr.aws/lambda/python:3.8
COPY ./poetry.lock ./pyproject.toml .
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
COPY ./data-neu/db.sqlite ${LAMBDA_TASK_ROOT}/data-neu/db.sqlite
ADD ./ ${LAMBDA_TASK_ROOT}
