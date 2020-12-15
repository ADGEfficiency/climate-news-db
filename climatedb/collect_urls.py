import logging
import random
import time
from urllib.error import HTTPError

import click
from googlesearch import search

from climatedb.database import File
from climatedb.logger import make_logger
from climatedb.newspapers.registry import registry
from climatedb.parse_urls import parse_url


def get_newspapers_from_registry(newspapers):
    if (newspapers == ("all",)) or (newspapers == ()):
        papers = registry
    else:
        if isinstance(newspapers, str):
            newspapers = [newspapers, ]
        papers = [n for n in registry if n["newspaper_id"] in newspapers]
    random.shuffle(papers)
    return papers

def collect_from_google(num, newspaper, logger=None):
    logger = logging.getLogger("climatedb")
    logger.info(f'searching for {num} from {newspaper["newspaper"]}')

    urls = google_search(newspaper["newspaper_url"], "climate change", stop=num)
    urls = [url for url in urls if newspaper["checker"](url, logger)]

    logger.info(f'search: found {len(urls)} for {newspaper["newspaper"]}')
    return urls


def google_search(site, query, start=1, stop=10, backoff=1.0):
    #  protects against a -1 example
    if stop <= 0:
        raise ValueError("stop of {stop} is invalid")

    try:
        qry = f"{query} site:{site}"
        time.sleep((2 ** backoff) + random.random())
        return list(search(qry, start=start, stop=stop, pause=1.0, user_agent="climatecoder"))

    except HTTPError as e:
        logger = logging.getLogger("climatedb")
        logger.info(f"{qry}, {e}, backoff {backoff}")
        return google_search(site, query, stop, backoff=backoff+1)


@click.command()
@click.argument("newspapers", nargs=-1)
@click.option(
    "-n",
    "--num",
    default=5,
    help="Number of urls to attempt to collect.",
    show_default=True,
)
@click.option(
    "--source", default="google", help="Where to look for urls.", show_default=True
)
@click.option(
    "--parse/--no-parse",
    default=True,
    help="Whether to parse the urls after collecting them.",
)
@click.option(
    "--check/--no-check",
    default=True,
    help="Whether to check the urls after collecting them.",
)
def cli(num, newspapers, source, parse, check):
    return main(num, newspapers, source, parse, check)


def main(num, newspapers, source, parse, check):
    logger = make_logger("logger.log")
    logger.info(f"collecting {num} from {newspapers} from {source}")

    urls_db = File('urls.data')
    newspapers = get_newspapers_from_registry(newspapers)

    collection = []
    for paper in newspapers:

        if source == "google":
            urls = collect_from_google(num, paper)
            logger.info(f"searched {len(urls)}")

        elif source == "urls.data":
            urls = urls_db.get(num)
            logger.info(f"loaded {len(urls)}")

        urls = [
            u for u in urls
            if paper["newspaper_url"] in u
        ]

        if check or source == "google":
            urls = [url for url in urls if paper["checker"](url, logger)]

        logger.info(f"saving {len(urls)} to db")
        urls_db.add(urls)
        collection.extend(urls)

    collection = list(set(collection))
    logger.info(f"parsing {len(collection)}")

    if parse:
        for url in collection:
            parse_url(url, rewrite=True, logger=logger)
