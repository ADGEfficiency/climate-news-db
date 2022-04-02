import asyncio
import json

import boto3
from rich import print

from climatedb.search import search
from climatedb import types

# from climatedb import databases as dbs
from climatedb.databases import find_all_papers
from climatedb.config import data_home, s3_bucket, s3_prefix

from climatedb import files


def controller_handler(
    event: dict, context: types.Union[dict, None] = None
) -> types.Dict[str, str]:
    """
    Could use the search lambda here, or just the handler here
    """

    bucket = event.get("s3_bucket", s3_bucket)
    key = event.get("s3_key", s3_prefix + "/urls.jsonl")

    urls_db = files.S3JSONLines(event["s3_bucket"], event["s3_key"])

    pkg = []
    for np in find_all_papers():
        urls = search(np, 5)
        urls_db.write(urls)
        pkg.extend(urls)

    return pkg


async def call_lambda(function_name, event, invocation_type="RequestResponse"):
    """asynchronously call AWS Lambda using boto3"""
    client = boto3.Session().client("lambda")

    print(
        f"\n[bold blue]calling lambda[/]: [bold green]{function_name}[/]\n event: {event}"
    )
    return client.invoke(
        FunctionName=function_name,
        InvocationType=invocation_type,
        Payload=json.dumps(event),
    )


def search_handler(
    event: dict, context: types.Union[dict, None]
) -> types.Dict[str, str]:
    print(event)
    print(context)
    results = search(event["newspaper"], 5)
    print(results)
    return results


async def main_async(newspapers):
    routines = [
        call_lambda("climatedb-dev-search", {"newspaper": newspaper.name})
        for newspaper in newspapers[:3]
    ]
    routines = await asyncio.gather(*routines)
    print(routines)
    print("done main async")


def controller_async_handler(
    event: dict, context: types.Union[dict, None] = None
) -> types.Dict[str, str]:
    print("controller handler")
    loop = asyncio.get_event_loop()
    newspapers = find_all_papers()
    out = loop.run_until_complete(main_async(newspapers))
    return {"msg": f"ran {len(newspapers)} newspapers", "loop-out": str(out)}


if __name__ == "__main__":
    controller_handler({"s3_bucket": s3_bucket, "s3_key": s3_prefix + "/urls.jsonl"})