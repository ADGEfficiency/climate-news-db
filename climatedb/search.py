from datetime import datetime
from urllib.error import HTTPError
import random
import time

from googlesearch import search as googlesearch
from rich import print

from climatedb.config import data_home
from climatedb import types


def search(paper: types.Newspaper, num: int, query: str = "climate change") -> list:
    """main"""
    print(f"searching {paper} for {num} results")
    urls = google_search(paper.newspaper_url, query, stop=num)
    urls = [{"url": u, "search_time_utc": datetime.utcnow().isoformat()} for u in urls]
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
