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
    num = event["num"]
    paper = event["paper"]

    newspapers = [
        p for p in files.JSONFile("./newspapers.json").read() if paper in p["name"]
    ]
    paper = Newspaper(**newspapers[0])

    pkg = []
    for query in ["climate change", "climate crisis"]:
        print(f"[green]search[/]: paper: {paper.name} n: {num} query: {query}")
        urls = google_search(paper.site, query, stop=num)
        print(f"found {len(urls)} urls")
        print(urls)
        pkg.append(urls)
        urls = [{"url": u, "timestamp": get_timestamp()} for u in urls]
        db = files.S3JSONLines(event["s3_bucket"], event["s3_key"])
        db.write(urls)

    return pkg
