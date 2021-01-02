import json

import click

from climatedb.databases import URLs, Articles
from climatedb.logger import make_logger
from climatedb.parse_urls import main as parse_url
from climatedb.registry import get_newspapers_from_registry

from climatedb import services

l = make_logger("logs/logger.log")


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
    "--db", default="jsonl", help="Which article databases to use."
)
def cli(
    newspapers,
    num,
    search,
    parse,
    check,
    replace,
    db
):
    return main(
        newspapers,
        num,
        search,
        parse,
        check,
        replace,
        db
    )



def main(
    newspapers,
    num,
    search,
    parse,
    check,
    replace,
    db
):
    newspapers = get_newspapers_from_registry(newspapers)
    urls_db = URLs('urls/urls.jsonl', engine='jsonl')

    for paper in newspapers:
        newspaper_id = paper['newspaper_id']
        final = Articles(
            f"articles/final/{newspaper_id}",
            engine="json-folder",
            key='article_id'
        )

        def msg(value):
            return json.dumps({
                'msg': value
            })

        #  get urls
        urls = [u for u in urls_db.get() if paper["newspaper_url"] in u['url']]
        l.info(msg(f'loaded {len(urls)} for {newspaper_id}'))

        #  filter out if we aren't replacing
        if not replace:
            urls = [u for u in urls if not final.exists(paper['get_article_id'](u['url']))]
            l.info(json.dumps({'msg': f'filtered to {len(urls)} after exists check'}))
        urls = urls[-num:]
        l.info(json.dumps({'msg': f'filtered to {len(urls)} for {paper["newspaper_id"]} from {urls_db.name}'}))

        #  search
        new_urls = services.search(paper, num)
        urls_db.add(new_urls)

        l.info(json.dumps({'msg': f'found {len(urls)} for {paper["newspaper_id"]}'}))
        urls.extend(new_urls)

        #  filter out if we aren't replacing
        if not replace:
            urls = [u for u in urls if not final.exists(paper['get_article_id'](u['url']))]
            l.info(json.dumps({'msg': f'filtered to {len(urls)} after exists check'}))

        #  check urls
        l.info(json.dumps({'msg': f'checking {len(urls)}'}))
        checked_urls = []
        for u in urls:
            #  try check, catch a urlcheckerror?
            if paper["checker"](u['url']):
                checked_urls.append(u)
            else:
                l.info(json.dumps({'msg': f"{u['url']}, check error"}))

            #  colud remove these from urlsdb...

        urls_to_parse = checked_urls
        l.info(json.dumps({'msg': f'filtered to {len(urls)} after exists check'}))

        #  parse
        if parse:
            l.info(msg(f"parsing {len(urls_to_parse)} for {newspaper_id}"}))
            for url in urls_to_parse:
                parse_url(url['url'], replace=replace, logger=l)
