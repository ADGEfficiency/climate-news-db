from climatedb.newspapers.bbc import check_url, parse_url

parsing_errors = (
    # https://www.climate-news-db.com/article?article_id=world-europe-55273004
    'https://www.bbc.com/news/world-europe-55273004'

    # https://www.climate-news-db.com/article?article_id=uk-55179603
    'https://www.bbc.com/news/uk-55179603'
)

bad_urls = (
    "http://www.bbc.com",
    "http://www.bbc.com/mediaaction/",
    "http://www.bbc.com/travel/travel-53138178",
    "https://www.bbc.com/news/av/science-environment-51129250",
    "http://www.bbc.com/newsround/home"
)

bad_redirect_urls = (
    "https://www.bbc.com/news/science-environment-51129250",
)

from climatedb.utils import request
for u in bad_redirect_urls:
    r = request(u)
    res = r['response']
    assert not check_url(r['url'])
    assert not check_url(u)


good_urls = (
    'https://www.bbc.com/news/science-environment-53138178',
    'https://www.bbc.com/news/science-environment-53842626'
)


for u in good_urls:
    assert check_url(u)

for u in bad_urls:
    assert not check_url(u)


"""
parsing

body = find_one_tag(soup, 'div', {'property': 'articleBody'})
body = find_one_tag(soup, 'div', {'class':'story-body'})
"""


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
