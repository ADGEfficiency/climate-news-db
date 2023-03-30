import random
import time
from datetime import datetime, timezone
from urllib.error import HTTPError

from googlesearch import search as googlesearch
from rich import print

from climatedb import files, models


def format_timestamp(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")


def get_timestamp():
    stamp = datetime.now(timezone.utc)
    return format_timestamp(stamp)


def google_search(
    site: str, query: str, start: int = 1, stop: int = 10, backoff: int = 1
):
    """helper for search"""

    #  protects against a -1 example
    if stop <= 0:
        stop = 10

    qry = f"{query} site:{site}"
    time.sleep((2**backoff) + random.random())
    try:
        return list(
            googlesearch(
                qry, start=start, stop=stop, pause=1.0, user_agent="adgefficiency"
            )
        )

    except HTTPError as e:
        print(f"{qry}, {e}, backoff {backoff}")
        return google_search(site, query, stop, backoff=backoff + 1)


import typer
from scrapy.settings import Settings

from climatedb.files import JSONLines
from climatedb.models import Newspaper

app = typer.Typer()


@app.command()
def cli(paper: str, query: str, num: int) -> None:
    settings = Settings()
    settings = Settings()
    settings.setmodule("climatedb.settings")

    newspapers = files.JSONFile("./newspapers.json").read()
    newspapers = [p for p in newspapers if paper in p["name"]]
    paper = Newspaper(**newspapers[0])

    query = "climate change"
    print(f"[green]searching[/]:\n {paper.name} n: {num} query: {query}")
    urls = google_search(paper.site, query, stop=num)
    urls = [{"url": u, "timestamp": get_timestamp()} for u in urls]

    db = JSONLines(settings["DATA_HOME"] / "urls.jsonl")
    db.write(urls)
    # urls = search(paper, 10, "climate crisis")
    # db.write(urls)


if __name__ == "__main__":
    typer.run(cli)
