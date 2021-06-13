from climatedb.engines import JSONFolder
from climatedb.registry import find_newspaper_from_url, get_newspaper
from climatedb.utils import form_article_id

from datetime import datetime
import html.parser

from climatedb.utils import ParserError
from requests.exceptions import TooManyRedirects
from requests import HTTPError


def get_article_id(url, paper):
    if "get_article_id" in paper.keys():
        return paper["get_article_id"](url)
    else:
        return form_article_id(url, idx=-1)


def main(
    url,
    lgr,
    replace=True,
    raw=None,
    final=None
):
    paper = find_newspaper_from_url(url)
    newspaper_id = paper["newspaper_id"]

    if not raw:
        raw = JSONFolder(
            f"articles/raw/{newspaper_id}",
            key='article_id'
        )
    if not final:
        final = JSONFolder(
            f"articles/final/{newspaper_id}",
            key='article_id'
        )

    def dispatch(exists, replace):

        #  always parse if replace
        if replace:
            return 'parse'

        #  exists but we don't want to replace it
        if exists and not replace:
            return 'no-parse'

        #  doesn't exist, we must make it
        if not exists and not replace:
            return 'parse'

    def test_parse_dispatch():

        #  exists, replace, expected
        data = (
            (True, False, 'no-parse'),
            (True, True, 'parse'),
            (False, False, 'parse')
        )

        for exists, replace, expected in data:
            assert dispatch(exists, replace) == expected

    test_parse_dispatch()

    article_id = get_article_id(url, paper)
    exists = final.exists('article_id', article_id)

    action = dispatch(exists, replace)
    parsed = {}
    if action == 'parse':
        parsed = parse_url(url, paper)
        if 'error' in parsed.keys():
            lgr({
                'url': url,
                'msg': f'{url}, error: {parsed["error"]}'
            })
        else:
            lgr({
                'url': parsed['article_url'],
                'msg': 'parse_url success',
            })

    if parsed:
        if 'error' not in parsed.keys():
            save_parsed(parsed, lgr, raw, final)
            lgr({
                'url': url,
                'msg': "save articles/raw and articles/final success",
            })


def parse_url(url, paper):
    try:
        parsed = paper['parser'](url)
    except (HTTPError, ParserError, TooManyRedirects) as error:
        msg = f"parse_url error, {error}\n"
        return {'error': msg}

    try:
        parsed = check_parsed_article(parsed)
    except ParserError as error:
        msg = f"check_parsed_article error, {error}\n"
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
            raise ParserError(msg)

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
    raw.add(parsed)
    del parsed["html"]
    final.add(parsed)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()

    from climatedb.logger import make_logger
    main(args.url, logger=make_logger('climatedb.log'))
