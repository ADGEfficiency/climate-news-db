import random
import time
from datetime import datetime, timezone
from urllib.error import HTTPError

import typer
from ddgs import DDGS
from rich import print
from scrapy.settings import Settings

from climatedb import files
from climatedb.files import JSONLines
from climatedb.models import Newspaper

app = typer.Typer()


def format_timestamp(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f%Z")


def get_timestamp() -> str:
    """Create standardized UTC timestamp."""
    stamp = datetime.now(timezone.utc)
    return format_timestamp(stamp)


def search_for_articles(
    site: str, query: str, num_results: int = 10, backoff: int = 1
) -> list:
    """helper for search"""
    qry = f"{query} site:{site}"
    time.sleep((2**backoff) + random.random())
    try:
        return list(DDGS().text(qry, max_resurlts=num_results))

    except HTTPError as e:
        raise e


@app.command()
def cli(paper: str, query: str, num: int) -> None:
    settings = Settings()
    settings.setmodule("climatedb.settings")
    newspapers = [
        p for p in files.JSONFile("./newspapers.json").read() if paper in p["name"]
    ]
    newspaper = Newspaper(**newspapers[0])
    print(f"[green]search[/]:\n paper: {newspaper.name} n: {num} query: {query}")
    results = search_for_articles(newspaper.site, query, num_results=num)
    urls = [r["href"] for r in results]
    print(f"found {len(urls)} results")
    urls = [{"url": u, "timestamp": get_timestamp()} for u in urls]
    db = JSONLines(settings["DATA_HOME"] / "urls.jsonl")
    db.write(urls)


if __name__ == "__main__":
    typer.run(cli)
