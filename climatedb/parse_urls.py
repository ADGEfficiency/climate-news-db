from climatedb.databases import RawArticles, Articles
from climatedb.registry import find_newspaper_from_url, get_newspaper
from climatedb.utils import form_article_id

from datetime import datetime
import html.parser


def get_article_id(url, paper):
    if "get_article_id" in paper.keys():
        return paper["get_article_id"](url)
    else:
        return form_article_id(url, idx=-1)


def main(
    url,
    logger,
    replace=True,
    raw=None,
    final=None
):
    paper = find_newspaper_from_url(url)
    newspaper_id = paper["newspaper_id"]

    if not raw:
        raw = RawArticles(f"raw/{newspaper_id}")
    if not final:
        final = Articles(
            f"final/{newspaper_id}",
            engine="json-folder",
            key='article_id'
        )
    article_id = get_article_id(url, paper)
    exists = final.exists(article_id)
    if exists and not replace:
        logger.info(f"{url}, already exists in final and not replacing")

    if exists and replace:
        logger.info(f"{url}, already exists in final and replacing")
        parsed = parse_url(url, paper)

    if not exists:
        logger.info(f"{url}, not in final")
        parsed = parse_url(url, paper)

    else:
        parsed = {'error': f'{url}, parse_url not run'}

    if 'error' in parsed.keys():
        logger.info(parsed['error'])

    if parsed and 'error' not in parsed.keys():
        save_parsed(parsed, logger, raw, final)


from climatedb.utils import ParserError
from requests.exceptions import TooManyRedirects

from requests import HTTPError
def parse_url(url, paper):
    newspaper_id = paper["newspaper_id"]
    msg = f"{url}, {newspaper_id}, parsing\n"

    try:
        parsed = paper['parser'](url)
    except (HTTPError, ParserError, TooManyRedirects) as error:
        msg += f"{url}, parsing error, {error}\n"
        return {'error': msg}

    try:
        parsed = check_parsed_article(parsed)
    except AssertionError as error:
        msg += f"{url}, check error, {error}\n"
        return {'error': msg}

    return parsed



def check_parsed_article(parsed):
    if not parsed:
        return {}

    newspaper = get_newspaper(parsed["newspaper_id"])
    parsed["date_uploaded"] = datetime.utcnow().isoformat()
    parsed = {**parsed, **newspaper}

    del parsed["checker"]
    del parsed["parser"]
    del parsed["get_article_id"]

    schema = [
        "newspaper",
        "newspaper_id",
        "newspaper_url",
        "body",
        "headline",
        "html",
        "article_url",
        "article_id",
        "date_published"
    ]
    for sc in schema:
        #  check key exists
        if sc not in parsed.keys():
            raise ValueError(f"{sc} missing from parsed article")

        #  check value length
        val = parsed[sc]
        if len(val) < 2:
            url = parsed["article_url"]
            msg = f"{url} - {sc} not long enough - {val}"
            print(msg)
            import pdb; pdb.set_trace()
            raise ValueError(msg)

    return parsed

def clean_parsed_article(parsed):
    #  data cleaning - replacing escaped html characters
    html_parser = html.parser.HTMLParser()
    parsed["body"] = html_parser.unescape(parsed["body"])
    parsed["headline"] = html_parser.unescape(parsed["headline"])
    return parsed


def save_parsed(parsed, logger, raw, final):
    article_id = parsed["article_id"]
    url = parsed['article_url']
    parsed = clean_parsed_article(parsed)
    logger.info(f"{url}, {article_id}, cleaned")

    raw.add(parsed)
    del parsed["html"]
    logger.info(f"{url}, {article_id}, raw saved")

    final.add(parsed)
    logger.info(f"{url}, {article_id}, final saved")



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()

    from climatedb.logger import make_logger
    main(args.url, logger=make_logger('climatedb.log'))
