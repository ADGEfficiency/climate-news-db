import json

import click

from climatedb import services
from climatedb.databases import URLs, Articles
from climatedb.logger import make_logger
from climatedb.parse import main as parse_url
from climatedb.registry import get_newspapers_from_registry


class JSONLogger():
    def __init__(self):
        self.lgr = make_logger("logs/logger.log")

    def __call__(self, msgs):
        if isinstance(msgs, str):
            msgs = {'msg': msgs}
        self.lgr.info(json.dumps(msgs))


lgr = JSONLogger()


@click.command()
@click.argument(
    "newspapers",
    nargs=-1
)
@click.option(
    "-n",
    "--num",
    default=5,
    help="Number of urls to attempt to collect.",
    show_default=True,
)
@click.option(
    "--search/--no-search",
    default=True,
    help="If to search for more urls.",
)
@click.option(
    "--parse/--no-parse",
    default=True,
    help="Whether to parse the urls after collecting them.",
)
def cli(
    newspapers,
    num,
    search,
    parse,
):
    newspapers = get_newspapers_from_registry(newspapers)
    urls_db = URLs('urls/urls.jsonl', engine='jsonl')

    for paper in newspapers:
        newspaper_id = paper['newspaper_id']
        final = Articles(f"articles/final/{newspaper_id}")

        if search:
            urls = services.search(paper, num)
            urls_db.add(urls)
            lgr({
                'msg': f'searched, found {len(urls)}',
                'newspaper': newspaper_id
            })

        else:
            #  get from urls_db for this newspaper
            urls = [u for u in urls_db.get() if paper["newspaper_url"] in u['url']]
            lgr({
                'msg': f'loaded {len(urls)} for {newspaper_id}',
                'newspaper': newspaper_id
            })

        #  check if already exists
        urls = [
            u for u in urls
            if not final.exists(paper['get_article_id'](u['url']))
        ]
        lgr({'msg': f"{len(urls)} after exists check"})

        #  check if url is OK
        checked_urls = []
        for u in urls:
            #  try check, catch a urlcheckerror?
            if paper["checker"](u['url']):
                checked_urls.append(u)
            else:
                lgr({'msg': f"{u['url']}, check error"})

        urls = checked_urls
        lgr({'msg': f"{len(urls)} after url checks"})

        #  limit num
        urls = urls[-num:]
        lgr({'msg': f"{len(urls)} after num limit"})

        #  parse
        urls_to_parse = urls
        if parse:
            lgr({'msg': f"parsing {len(urls_to_parse)}"})
            for url in urls_to_parse:
                parse_url(url['url'], replace=True, lgr=lgr)
                lgr(f"{url}, parsed success")
        else:
            lgr({'msg': f"not parsing {len(urls_to_parse)}"})
