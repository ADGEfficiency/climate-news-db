from datetime import datetime as dt
import logging
import random
import time
from urllib.error import HTTPError

import click
from googlesearch import search

from climatedb.databases import URLs
from climatedb.logger import make_logger
from climatedb.registry import get_newspapers_from_registry
from climatedb.parse_urls import main as parse_url


def now():
    return dt.utcnow().isoformat()


def collect_from_google(num, newspaper, logger=None):
    return google_search(
        newspaper["newspaper_url"],
        "climate change",
        stop=num
    )


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
@click.option(
    "--replace/--no-replace",
    default=True,
    help="Whether to replace in the final database",
)
@click.option(
    "--db", default="files", help="Which database to use.", show_default=True
)
def cli(num, newspapers, source, parse, check, replace, db):
    return main(num, newspapers, source, parse, check, replace, db)


def main(
    num,
    newspapers,
    source,
    parse,
    check,
    replace,
    db
):
    logger = make_logger("logger.log")
    logger.info(f"collecting {num} from {newspapers} from {source}")

    db = URLs('urls.jsonl', engine='jsonl')
    newspapers = get_newspapers_from_registry(newspapers)

    collection = []
    for paper in newspapers:

        if source == "google":
            logger.info(f'searching google for {num} for {paper["newspaper_id"]}')
            urls = collect_from_google(num, paper)
            urls = [{'url': u, 'search_time_UTC': now()} for u in urls]
            logger.info(f'found {len(urls)} for {paper["newspaper_id"]}')

        elif source == "urls.data":
            # TODO here we want a db.filter(paper=newspaper_id)
            #  maybe a key to get latest?

            urls = db.get(num=len(db))
            logger.info(f'loaded {len(urls)}')
            urls = [u for u in urls if paper["newspaper_url"] in u['url']]
            logger.info(f'loaded {len(urls)} for {paper["newspaper_id"]} from {db.name}')
            urls = urls[-num:]
            logger.info(f'filtered to {len(urls)} for {paper["newspaper_id"]} from {db.name}')

        if check or source == "google":
            urls = [u for u in urls if paper["checker"](u['url'], logger)]

        logger.info(f"saving to {db.name}")
        logger.info(f"  {len(db)} before")
        db.add(urls)
        logger.info(f"  {len(db)} after")
        collection.extend(urls)

    if parse:
        logger.info(f"parsing {len(collection)}")
        for url in collection:
            parse_url(url['url'], replace=replace, logger=logger)
