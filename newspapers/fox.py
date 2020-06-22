import json

import requests
from bs4 import BeautifulSoup

from newspapers.guardian import check_match


def check_fox_url(url, logger):
    unwanted = ['category', 'video', 'radio', 'person']
    if not check_match(url, unwanted):
        logger.info(f'fox, {url}, check failed')
        return False
    return True


def parse_fox_html(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")

    table = soup.findAll('div', attrs={"class": "article-body"})
    if len(table) != 1:
        return {}

    #  info about published date
    scripts = soup.findAll('script', attrs={'type': 'application/ld+json'})
    assert len(scripts) == 2
    article_metadata = str(scripts[0].contents[0])
    article_metadata = article_metadata.replace('\n', '')
    article_metadata = json.loads(article_metadata)

    article = [p.text for p in table[0].findAll('p')]
    article = ''.join(article)

    #  hack for coronavirus tag that appears in later articles
    article = article.replace(
        'Get all the latest news on\xa0coronavirus\xa0and more delivered daily to your inbox.\xa0Sign up here.',
        ''
    )

    return {
        'newspaper': 'fox',
        'body': article,
        'html': html,
        'url': url,
        'id': url.split('/')[-1],
        'published': article_metadata['datePublished'],
        'modified': article_metadata['dateModified']
    }


if __name__ == '__main__':
    import requests

    url = 'https://www.foxnews.com/us/climate-change-tropical-cyclone-hurricane-typhoon-tropical-storm-noaa-study-weather-atlantic-pacific-indian-ocean'
    out = parse_fox_html(url)

    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")

