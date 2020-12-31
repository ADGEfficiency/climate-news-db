from climatedb.databases import RawArticles, Articles
from climatedb.registry import find_newspaper_from_url
from climatedb.registry import check_parsed_article, clean_parsed_article
from climatedb.utils import form_article_id


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
        parsed = parse_url(url, paper, logger)

    if not exists:
        logger.info(f"{url}, not in final")
        parsed = parse_url(url, paper, logger)

    else:
        parsed = None

    if parsed:
        save_parsed(parsed, logger, raw, final)


def parse_url(url, paper, logger):
    newspaper_id = paper["newspaper_id"]
    logger.info(f"{url}, {newspaper_id}, parsing")

    try:
        parsed = paper['parser'](url)
    except AssertionError as error:
        logger.info(f"{url}, parsing error")
        return None
    try:
        parsed = check_parsed_article(parsed)
    except AssertionError as error:
        logger.info(f"{url}, check error")
        return None

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
