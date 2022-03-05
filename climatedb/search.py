from climatedb.config import data_home
from climatedb.engines import JSONLinesFile
import random
import time
import logging
from urllib.error import HTTPError

from googlesearch import search as googlesearch
from datetime import datetime as dt


def google_search(site, query, start=1, stop=10, backoff=1.0):
    #  protects against a -1 example
    if stop <= 0:
        stop = 10

    try:
        qry = f"{query} site:{site}"
        time.sleep((2**backoff) + random.random())
        return list(
            googlesearch(
                qry, start=start, stop=stop, pause=1.0, user_agent="climatecoder"
            )
        )

    except HTTPError as e:
        logger = logging.getLogger("climatedb")
        print(f"{qry}, {e}, backoff {backoff}")
        return google_search(site, query, stop, backoff=backoff + 1)


def search(paper, num):
    print(f"searching {paper} for {num} results")
    urls = google_search(paper["newspaper_url"], "climate change", stop=num)
    urls = [{"url": u, "search_time_UTC": now()} for u in urls]
    return urls


if __name__ == "__main__":
    from climatedb.databases_neu import JSONFile

    urls = JSONLinesFile(f"{data_home}/urls.jsonl", key="url")
    papers = JSONFile(f"{data_home}/newspapers.json").read()

    n_collect = 5
    for paper in papers.values():
        urls.add(search(paper, n_collect))
