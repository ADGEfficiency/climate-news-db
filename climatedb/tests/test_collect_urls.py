from climatedb.databases import URLs
from climatedb.registry import get_newspapers_from_registry
from climatedb.collect_urls import collect_from_google, now
from climatedb.logger import make_logger
from climatedb.tests.test_databases import setup

#  maybe should mock test data here, instead of calling collect google
#  mock newspaper registry, urls, mock newspaper checker etc


def test_collect_components(setup):
    db = URLs('temp/urls.jsonl', engine='jsonl')
    #  this fails - should it? (no data in file)
    #start_data = urls_db.get()

    newspapers = get_newspapers_from_registry()
    logger = make_logger('temp/logger.log')
    paper = newspapers[0]
    num = 1
    urls = collect_from_google(num, paper)

    check = False
    if check:
        urls = [u for u in urls if paper['checker'](u, logger=logger)]

    urls = [{'url': u, 'search_time_UTC': now()} for u in urls]

    db.add(urls)
    before = len(db)

    #  don't add duplicates
    db.add(urls)
    assert before == len(db)
