FROM public.ecr.aws/lambda/python:3.10
RUN yum install -y libxml2 gcc libxslt
RUN pip --no-cache-dir install uv
WORKDIR ${LAMBDA_TASK_ROOT}
ADD ./ ${LAMBDA_TASK_ROOT}
RUN uv pip install --system .
