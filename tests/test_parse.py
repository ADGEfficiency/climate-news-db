from climatedb.collect import JSONLogger
from climatedb.logger import make_logger
from climatedb.parse import main
from climatedb.registry import find_newspaper_from_url

from climatedb.databases import ArticlesFolders


def test_parse_main():
    url = "https://www.bbc.com/news/world-us-canada-46351940"
    logger = JSONLogger("temp/logs.log")

    paper = find_newspaper_from_url(url)
    newspaper_id = paper["newspaper_id"]
    raw = ArticlesFolders(
        f"temp/raw/{newspaper_id}"
    )
    final = ArticlesFolders(
        f"temp/final/{newspaper_id}"
    )
    main(url, logger, replace=True, raw=raw, final=final)

    #  check raw & final are where they should be 
    #  rm temp
