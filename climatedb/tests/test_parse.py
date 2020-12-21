from climatedb.logger import make_logger
from climatedb.parse_urls import main
from climatedb.registry import find_newspaper_from_url

from climatedb.databases import RawArticles, Articles


def test_parse_main():
    url = "https://www.bbc.com/news/world-us-canada-46351940"
    logger = make_logger("temp/logger.log")

    paper = find_newspaper_from_url(url)
    newspaper_id = paper["newspaper_id"]
    raw = RawArticles(f"temp/raw/{newspaper_id}")
    final = Articles(
        f"temp/final/{newspaper_id}",
        engine="json-folder",
        key='article_id'
    )
    main(url, logger, replace=True, raw=raw, final=final)

    #  check raw & final are where they should be 
    #  rm temp


test_parse_main()
