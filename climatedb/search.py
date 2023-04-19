import random
import time
from datetime import datetime, timezone
from urllib.error import HTTPError

import typer
from googlesearch import search as googlesearch
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


def google_search(
    site: str, query: str, start: int = 0, stop: int = 10, backoff: int = 1
) -> list:
    """helper for search"""
    assert stop > 0

    qry = f"{query} site:{site}"
    time.sleep((2**backoff) + random.random())

    try:
        return list(
            googlesearch(
                qry,
                num=stop,
                start=start,
                stop=stop,
                pause=0.5,
                user_agent="adgefficiency",
                tbs="qdr:d2",
            )
        )

    except HTTPError as e:
        raise e
        # print(f"{qry}, {e}, backoff {backoff}")
        # return google_search(site, query, start=stop, backoff=backoff + 1)


@app.command()
def cli(paper: str, query: str, num: int) -> None:
    settings = Settings()
    settings.setmodule("climatedb.settings")
    newspapers = [
        p for p in files.JSONFile("./newspapers.json").read() if paper in p["name"]
    ]
    newspaper = Newspaper(**newspapers[0])
    print(f"[green]search[/]:\n paper: {newspaper.name} n: {num} query: {query}")
    urls = google_search(newspaper.site, query, stop=num)
    urls = [{"url": u, "timestamp": get_timestamp()} for u in urls]
    db = JSONLines(settings["DATA_HOME"] / "urls.jsonl")
    db.write(urls)


if __name__ == "__main__":
    typer.run(cli)
