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
    cls = 'article-body'
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")

    table = soup.findAll('div', attrs={"class": cls})
    if len(table) != 1:
        return {}

    #  info about published date
    scripts = soup.findAll('script', attrs={'type': 'application/ld+json'})
    assert len(scripts) == 2
    article_metadata = str(scripts[0].contents[0])
    article_metadata = article_metadata.replace('\n', '')
    article_metadata = json.loads(article_metadata)

    article = [p.text for p in table[0].findAll('p', attrs={"class": "speakable"})]
    article = ''.join(article)
    return {
        'body': article,
        'html': html,
        'url': url,
        'id': url.split('/')[-1].strip('.html'),
        'published': article_metadata['datePublished'],
        'modified': article_metadata['dateModified']
    }


if __name__ == '__main__':
    import requests

    url = 'https://www.foxnews.com/science/todays-climate-change-is-worse-than-anything-earth-has-experienced-in-the-past-2000-years?utm_referrer=https%3A%2F%2Fzen.yandex.com'

    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")


