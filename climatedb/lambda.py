"""Functions for AWS Lambda."""
import typing

from rich import print

from climatedb import files
from climatedb.models import Newspaper
from climatedb.search import get_timestamp, google_search


def search_controller(
    event: dict, context: typing.Union[dict, None] = None
) -> list[dict[str, str]]:
    """Search newspapers for articles about climate change.

    Appends to `urls.jsonl` on S3.  Run on a daily schedule.
    """
    #  duplication of logic in /Users/adam/climate-news-db/climatedb/search.py
    #  TODO refactor out

    newspapers = files.JSONFile("./newspapers.json").read()
    pkg = []
    num = event["num"]
    query = event["query"]
    for newspaper in newspapers:
        paper = Newspaper(**newspaper)
        print(f"[green]search[/]: paper: {paper.name} n: {num} query: {query}")
        urls = google_search(paper.site, query, stop=num)
        print(f"found {len(urls)} urls")
        print(urls)
        urls = [{"url": u, "timestamp": get_timestamp()} for u in urls]
        pkg.extend(urls)

    db = files.S3JSONLines(event["s3_bucket"], event["s3_key"])
    db.write(pkg)
    return pkg
