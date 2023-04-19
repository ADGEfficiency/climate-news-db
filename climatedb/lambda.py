"""Functions for AWS Lambda."""
import typing

from rich import print

from climatedb import files
from climatedb.models import Newspaper
from climatedb.search import get_timestamp, google_search


def search_controller(
    event: dict, context: typing.Union[dict, None] = None
) -> list[dict[str, str]]:
    """Search all newspapers for climate articles.

    Reads newspapers from the SQLite database.

    Writes urls to `urls.jsonl` on S3.
    """
    #  duplication of /Users/adam/climate-news-db/climatedb/search.py

    newspapers = files.JSONFile("./newspapers.json").read()
    paper = Newspaper(**newspapers[0])

    pkg = []
    num = event["num"]
    for query in ["climate change", "climate crisis"]:
        for paper in newspapers:
            print(f"[green]search[/]:\n paper: {paper.name} n: {num} query: {query}")
            urls = google_search(paper.site, query, stop=num)
            urls = [{"url": u, "timestamp": get_timestamp()} for u in urls]
            pkg.extend(urls)

    db = files.S3JSONLines(event["s3_bucket"], event["s3_key"])
    db.write(pkg)
    return pkg
