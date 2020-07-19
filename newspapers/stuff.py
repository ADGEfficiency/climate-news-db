import requests
from bs4 import BeautifulSoup

import pytest


def check_stuff_url(url, logger=None):
    parts = url.split('/')
    if len(parts) < 7:
        if logger:
            logger.info(f'stuff, {url}, check failed, not long enough')
        return False

    return True



def parse_stuff_url(url, logger=None):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")

    body = soup.findAll("span", attrs={"class": "sics-component__story__body sics-component__story__body--nativform"})
    assert len(body) == 1
    body = ''.join([p.text for p in body[0].findAll('p')])

    modified = soup.findAll("span", attrs={"itemprop": "dateModified"})
    assert len(modified) == 1
    modified = modified[0]["content"]

    published = soup.findAll("meta", attrs={"itemprop": "datePublished"})
    assert len(published) == 1
    published = published[0]["content"]

    headline = soup.findAll('h1', attrs={"itemprop": "headline"})
    assert len(headline) == 1
    headline = headline[0].text

    return {
        'newspaper_id': 'stuff',
        'body': body,
        'headline': headline,
        'article_url': url,
        'html': html,
        'article_id': url.split('/')[-1],
        'date_published': published,
        'date_modified': modified,
    }


stuff = {
    "newspaper_id": "stuff",
    "newspaper": "Stuff.co.nz",
    "newspaper_url": "stuff.co.nz",
    "checker": check_stuff_url,
    "parser": parse_stuff_url
}
