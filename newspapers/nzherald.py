import json

from json.decoder import JSONDecodeError

from bs4 import BeautifulSoup
import requests


def check_nzherald_url(url, logger=None):
    if url[-4:] == '.pdf':
        return False
    if 'video.cfm' in url:
        return False
    return True


def parse_nzherald_url(url):
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, features="html5lib")

    try:
        table = soup.findAll('div', attrs={'id': 'article-body'})
        article = ''.join([p.text for p in table[0].findAll('p')])
        ld = soup.findAll('script', attrs={'type': 'application/ld+json'})
        ld = ld[0].getText()
        ld = ld.replace('\n', '')
    except IndexError as e:
        return {'error': repr(e)}

    try:
        ld = json.loads(ld)
    except JSONDecodeError as e:
        print('decode error')
        return {'error': repr(e)}

    return {
        'newspaper_id': 'nzherald',
        'body': article,
        'headline': ld['headline'],
        'article_url': url,
        'article_id': url.split('/')[-1],
        'html': html,
        'article_id': url.split('/')[-1],
        'date_published': ld['datePublished'],
        'date_modified': ld['dateModified'],
    }


nzherald = {
    "newspaper_id": "nzherald",
    "newspaper": "The New Zealand Herald",
    "newspaper_url": "nzherald.co.nz",
    "checker": check_nzherald_url,
    "parser": parse_nzherald_url
}


if __name__ == '__main__':

    urls = ('https://www.nzherald.co.nz/nz/news/article.cfm?c_id=1&objectid=12270976',
           'https://www.nzherald.co.nz/nz/news/article.cfm?c_id=1&objectid=199698')

    print(urls)
    url = urls[0]


"""
<html class="articlestory"><head> <script type="application/ld+json">

"""

