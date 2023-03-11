import random
import time
from datetime import datetime, timezone
from urllib.error import HTTPError

from googlesearch import search as googlesearch
from rich import print

from climatedb import types
from climatedb.databases import find_all_papers, load_newspapers_json


def format_timestamp(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")


def get_timestamp():
    stamp = datetime.now(timezone.utc)
    return format_timestamp(stamp)


def google_search(site, query, start=1, stop=10, backoff=1.0):
    """helper for search"""
    #  protects against a -1 example
    if stop <= 0:
        stop = 10

    try:
        qry = f"{query} site:{site}"
        time.sleep((2**backoff) + random.random())
        return list(
            googlesearch(
                qry, start=start, stop=stop, pause=1.0, user_agent="adgefficiency"
            )
        )

    except HTTPError as e:
        print(f"{qry}, {e}, backoff {backoff}")
        return google_search(site, query, stop, backoff=backoff + 1)


def search(paper: types.Newspaper, num: int, query: str = "climate change") -> list:
    """main"""
    print(f"searching:\n {paper.name} n: {num} query: {query}")
    urls = google_search(paper.newspaper_url, query, stop=num)
    urls = [{"url": u, "search_time_utc": get_timestamp()} for u in urls]
    return urls


if __name__ == "__main__":
    from climatedb.files import JSONLines
    from climatedb.types import Newspaper

    papers = load_newspapers_json()
    for paper in ["daily_post", "daily_nation", "batimes", "folha"]:
        print(paper)
        paper = Newspaper(**papers[paper])
        db = JSONLines("./data-neu/urls.jsonl")
        urls = search(paper, 10, "climate change")
        db.write(urls)
        urls = search(paper, 10, "climate crisis")
        db.write(urls)
