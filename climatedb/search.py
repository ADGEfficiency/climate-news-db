import random
import time
from datetime import datetime, timezone
from urllib.error import HTTPError

from googlesearch import search as googlesearch
from rich import print

from climatedb import types


def format_timestamp(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")


def get_timestamp():
    stamp = datetime.now(timezone.utc)
    return format_timestamp(stamp)


def search(paper: types.Newspaper, num: int, query: str = "climate change") -> list:
    """main"""
    print(f"searching {paper} for {num} results")
    urls = google_search(paper.newspaper_url, query, stop=num)
    urls = [{"url": u, "search_time_utc": get_timestamp()} for u in urls]
    return urls


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
