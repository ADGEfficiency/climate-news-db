import json

# from climatedb.collect_urls import main as collect_urls
from climatedb.database import NewspaperTextFiles
from climatedb.logger import make_logger
from climatedb.newspapers.registry import find_newspaper_from_url
from climatedb.newspapers.registry import check_parsed_article, clean_parsed_article


def parse_url(url, rewrite, logger):
    newspaper = find_newspaper_from_url(url)

    logger.info(f"{url}, parsing")
    newspaper_id = newspaper["newspaper_id"]
    raw = NewspaperTextFiles(f"raw/{newspaper_id}")
    final = NewspaperTextFiles(f"final/{newspaper_id}")

    #  run the parsing
    parsed = newspaper["parser"](url)

    #  check if already in database
    #  bit silly as we have already parsed it!
    #  means we need to get the article ID before parsing
    # check = final.check(parsed['article_id'])

    #  cant check if we get an error there!

    # if not rewrite and check:
    #     logger.info(r'{url}, {article_id} already exists - not parsing')

    if "error" in parsed.keys():
        error = parsed["error"]
        logger.info(f"{url}, error, {error}")

    else:
        parsed = check_parsed_article(parsed)
        if not parsed:
            logger.info(f"{url}, error, failed check_parsed_article")

        else:
            parsed = clean_parsed_article(parsed)

            article_id = parsed["article_id"]
            logger.info(f"{url}, saving, article_id={article_id}")
            raw.write(parsed["html"], article_id + ".html", "w")
            del parsed["html"]
            try:
                final.write(json.dumps(parsed), article_id + ".json", "w")
            except TypeError:
                logger.info(f"{url}, type error")


# def main(newspapers, rewrite=True):
#     #  reads from urls.data, writes to database
#     #  check if html exists

#     #  get all urls from urls.data
#     urls = collect_urls(num=-1, newspapers=newspapers, source="urls.data", parse=False)

#     for url in urls:
#         parse_url(url, rewrite=rewrite, logger=logger)
