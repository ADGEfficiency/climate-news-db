import json
import typing

import boto3
from rich import print

from climatedb.models import SearchLambdaEvent
from climatedb.utils import read_newspapers_json

region = "ap-southeast-2"


def get_lambda_function_name(logical_name: str) -> typing.Optional[str]:
    client = boto3.client("lambda", region_name=region)
    paginator = client.get_paginator("list_functions")
    for page in paginator.paginate():
        for function in page["Functions"]:
            if logical_name in function["FunctionName"]:
                return function["FunctionName"]


def get_exported_bucket_name(export_name: str) -> typing.Optional[str]:
    client = boto3.client("cloudformation", region_name=region)
    response = client.list_exports()
    for export in response["Exports"]:
        if export["Name"] == export_name:
            return export["Value"]


if __name__ == "__main__":
    bucket_name = get_exported_bucket_name("BucketName")
    function_name = get_lambda_function_name("SearchLambda")

    assert bucket_name is not None
    assert function_name is not None
    newspapers = read_newspapers_json()
    import random
    random.shuffle(newspapers)

    print(
        f"Bucket: {bucket_name} Function: {function_name} Newspapers {len(newspapers)}"
    )

    client = boto3.client("lambda", region_name=region)
    for newspaper in newspapers:
        print(f"Invoking {function_name} for {newspaper}")
        response = client.invoke(
            FunctionName=function_name,
            InvocationType="RequestResponse",
            Payload=SearchLambdaEvent(
                s3_bucket=bucket_name, newspaper_name=newspaper.name, num=5
            ).json(),
        )
        response_payload = json.loads(response["Payload"].read())
        print(f"Response: {response}\nPayload: {response_payload}")
