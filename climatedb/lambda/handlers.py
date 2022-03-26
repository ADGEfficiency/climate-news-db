import boto3
import json

from rich import print
import asyncio

from climatedb import types

from climatedb.databases_neu import find_all_papers


async def call_lambda(function_name, event, invocation_type="RequestResponse"):
    """asynchronously call AWS Lambda using boto3"""
    try:
        client = boto3.Session().client("lambda")

        print(
            f"\n[bold blue]calling lambda[/]: [bold green]{function_name}[/]\n event: {event}"
        )
        return client.invoke(
            FunctionName=function_name,
            InvocationType=invocation_type,
            Payload=json.dumps(event),
        )
    except:
        #  just during dev
        print("error")

from climatedb.search import search

def search_handler(
    event: dict, context: types.Union[dict, None]
) -> types.Dict[str, str]:
    print(event)
    print(context)
    return search(event['newspaper'], 5)


async def main_async(newspapers):
    routines = [
        call_lambda("search_handler", {"newspaper": newspaper.name})
        for newspaper in newspapers[:3]
    ]
    await asyncio.gather(*routines)


def controller_handler(
    event: dict, context: types.Union[dict, None] = None
) -> types.Dict[str, str]:
    print("controller handler")
    loop = asyncio.get_event_loop()
    newspapers = find_all_papers()
    out = loop.run_until_complete(main_async(newspapers))
    return {
        "msg": f"ran {len(newspapers)} newspapers"
        "loop-out": str(out)
    }


if __name__ == "__main__":
    controller_handler({})
