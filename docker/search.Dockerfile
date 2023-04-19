FROM public.ecr.aws/lambda/python:3.10
COPY ../../poetry.lock ../../pyproject.toml ../../poetry.toml /
RUN pip --no-cache-dir install poetry==1.3.0 && poetry install --no-interaction --no-ansi
ADD ./ ${LAMBDA_TASK_ROOT}
