"""Functions for AWS Lambda."""

import typing


from climatedb import files
from climatedb.models import SearchLambdaEvent
from climatedb.search import search


def search_controller(
    event: dict, context: typing.Union[dict, None] = None
) -> list[dict[str, str]]:
    """Search newspaper sites for articles and write to JSON file on S3"""
    event = SearchLambdaEvent(**event).dict()
    pkg = []
    for query in ["climate change", "climate crisis"]:
        db = files.S3JSONLines(event["s3_bucket"], event["s3_key"])
        pkg.extend(search(event["newspaper_name"], query, event["num"], db))
    return pkg
