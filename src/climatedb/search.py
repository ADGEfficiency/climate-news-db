import random
import time
from datetime import datetime, timezone
from urllib.error import HTTPError

import typer
from ddgs import DDGS
from rich import print
from scrapy.settings import Settings

from climatedb import files
from climatedb.files import JSONLines, S3JSONLines
from climatedb.models import Newspaper
from climatedb.utils import get_one_newspaper

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
    time.sleep((2**backoff) + random.random())
    try:
        return list(DDGS().text(f'"{query}" site:{site}', max_resurlts=num_results))

    except HTTPError as e:
        raise e


def search(paper: str, query: str, num: int, db: JSONLines | S3JSONLines) -> list[dict[str, str]]:
    newspaper = get_one_newspaper(paper)
    print(f"[green]search[/]:\n paper: {newspaper.name} n: {num} query: {query}")
    results = search_for_articles(newspaper.site, query, num_results=num)
    print(f"found {len(results)} results")
    urls = [{"url": r["href"], "timestamp": get_timestamp()} for r in results]
    db.write(urls)
    return urls


@app.command()
def cli(paper: str, query: str, num: int) -> None:
    settings = Settings()
    settings.setmodule("climatedb.settings")
    db = JSONLines(settings["DATA_HOME"] / "urls.jsonl")
    search(paper, query, num, db)


if __name__ == "__main__":
    typer.run(cli)
