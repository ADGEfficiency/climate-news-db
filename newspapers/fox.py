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

    article = [p.text for p in table[0].findAll('p', attrs={"class": "speakable"})]
    article = ''.join(article)
    return {
        'body': article,
        'html': html,
        'url': url,
        'id': url.split('/')[-1]
    }
