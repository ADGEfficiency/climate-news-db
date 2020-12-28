from climatedb.config import DBHOME
from climatedb.databases import URLs
from climatedb.registry import get_newspaper
from climatedb.collect_urls import collect_from_google, now
from climatedb.logger import make_logger
from climatedb.tests.test_databases import setup

#  maybe should mock test data here, instead of calling collect google
#  mock newspaper registry, urls, mock newspaper checker etc


def test_collect_components(setup):
    logger = make_logger('temp/logger.log')
    paper = get_newspaper('bbc')
    urls = [
        'https://www.bbc.com/news/science-environment-24021772',
        'https://www.bbc.com/news/science-environment-55416013'
    ]
    check = True
    if check:
        urls = [u for u in urls if paper['checker'](u, logger=logger)]
    urls = [{'url': u, 'search_time_UTC': now()} for u in urls]

    db = URLs('temp/urls.json')
    db.add(urls)
    before = len(db)

    #  don't add duplicates
    db.add(urls)
    assert before == len(db)
