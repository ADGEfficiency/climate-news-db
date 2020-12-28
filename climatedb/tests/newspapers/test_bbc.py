from climatedb.newspapers.bbc import bbc

from climatedb.utils import request

check_url = bbc['checker']
parse_url = bbc['parser']
get_article_id = bbc['get_article_id']


def test_bbc_bad_redirects():
    bad_redirect_urls = (
        "https://www.bbc.com/news/science-environment-51129250",
)
    for u in bad_redirect_urls:
        r = request(u)
        res = r['response']
        assert not check_url(r['url'])
        assert not check_url(u)


parsing_errors = (
    # https://www.climate-news-db.com/article?article_id=world-europe-55273004
    'https://www.bbc.com/news/world-europe-55273004'

    # https://www.climate-news-db.com/article?article_id=uk-55179603
    'https://www.bbc.com/news/uk-55179603'
)


def test_bbc_good_urls():
    good_urls = (
        'https://www.bbc.com/news/science-environment-53138178',
        'https://www.bbc.com/news/science-environment-53842626'
    )
    for u in good_urls:
        assert check_url(u)


def test_bad_urls():
    bad_urls = (
        "http://www.bbc.com",
        "http://www.bbc.com/mediaaction/",
        "http://www.bbc.com/travel/travel-53138178",
        "https://www.bbc.com/news/av/science-environment-51129250",
        "http://www.bbc.com/newsround/home",
        "http://www.bbc.com/earth/tags/climatechange",
        "https://www.bbc.com/iplayer/schedules/bbcnews",
        "https://www.bbc.com/news/world/asia"
    )
    for u in bad_urls:
        assert not check_url(u)


"""
parsing

body = find_one_tag(soup, 'div', {'property': 'articleBody'})
body = find_one_tag(soup, 'div', {'class':'story-body'})
"""


def test_bbc_parsing():
    parse_test_urls = (
        'https://www.bbc.com/news/world-europe-55273004',
        'https://www.bbc.com/news/science-environment-51134254',
        'https://www.bbc.com/news/science-environment-53726487',
        'https://www.bbc.com/news/world-australia-50341210',
        'https://www.bbc.com/news/uk-scotland-47746289'
    )

    for url in parse_test_urls:
        parsed = parse_url(url)
        assert 'error' not in parsed.keys()
        assert len(parsed['body']) > 50

        assert 'Read more here' not in parsed['body']
        twitter = ' on Twitter'
        assert parsed['body'][-len(twitter):] != twitter


def test_bbc_get_article_id():
    article_id_checks = [
        ('https://www.bbc.com/news/uk-politics-53992500?intlink_from_url=https://www.bbc.com/news/explainers&link_location=live-reporting-story', 'uk-politics-53992500')
    ]

    for url, expected in article_id_checks:
        aid = get_article_id(url)
        assert expected == aid
