import random
import time
import logging
from urllib.error import HTTPError

from googlesearch import search as googlesearch
from datetime import datetime as dt


def now():
    return dt.utcnow().isoformat()


def google_search(site, query, start=1, stop=10, backoff=1.0):
    #  protects against a -1 example
    if stop <= 0:
        stop = 10

    try:
        qry = f"{query} site:{site}"
        time.sleep((2 ** backoff) + random.random())
        return list(googlesearch(qry, start=start, stop=stop, pause=1.0, user_agent="climatecoder"))

    except HTTPError as e:
        logger = logging.getLogger("climatedb")
        logger.info(f"{qry}, {e}, backoff {backoff}")
        return google_search(site, query, stop, backoff=backoff+1)


def collect_from_google(num, newspaper, logger=None):
    return google_search(
        newspaper["newspaper_url"],
        "climate change",
        stop=num
    )


def search(paper, num):
    urls = collect_from_google(num, paper)
    urls = [{'url': u, 'search_time_UTC': now()} for u in urls]
    return urls


def collect():
    return {
        'msg': 'collect service success'
    }
