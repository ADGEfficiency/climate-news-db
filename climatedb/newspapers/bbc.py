from bs4 import BeautifulSoup
import requests

from climatedb.newspapers.utils import find_one_tag, form_article_id


def check_bbc_url(url, logger=None):
    #  should look for bbc.com/news ?

    if '/av/' in url:
        return False
    if '/topics/' in url:
        return False
    if '/tags/' in url:
        return False
    if '/programmes/' in url:
        return False

    #  TODO
    if '/future/' in url:
        return False
    #  TODO
    if '/culture/' in url:
        return False

    #  maybe
    if '/travel/' in url:
        return False

    if '/bitesize/' in url:
        return False
    if '/comments' in url:
        return False
    #  wierd redirect to /av/
    if url == 'https://www.bbc.com/news/science-environment-52926683':
        return False
    return True


def parse_bbc_url(url, logger=None):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")

    body = find_one_tag(soup, 'div', {'property': 'articleBody'})
    body = body.findAll("p")
    body = "".join(p.text for p in body)

    import json
    def find_app_json(soup):
        app = find_one_tag(soup, 'script', {'type': 'application/ld+json'}).text
        app = app.replace('\n', '')
        return json.loads(app)

    app = find_app_json(soup)

    return {
        "newspaper_id": "bbc",
        "body": body,
        "article_id": form_article_id(url, idx=-1),
        "headline": app['headline'],
        "article_url": url,
        "html": html,
        "date_published": app["datePublished"],
        "date_modified": app["dateModified"],
    }


bbc = {
    "newspaper_id": "bbc",
    "newspaper": "The BBC",
    "newspaper_url": "bbc.com",
    "checker": check_bbc_url,
    "parser": parse_bbc_url,
    "color": "#0098FF"
}


if __name__ == "__main__":
    url = 'https://www.bbc.com/news/science-environment-51134254'
    url = 'https://www.bbc.com/news/science-environment-53726487'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")
    out = parse_bbc_url(url)
