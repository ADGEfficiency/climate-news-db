from bs4 import BeautifulSoup
import requests

from climatedb.newspapers.utils import find_one_tag, form_article_id


def check_bbc_url(url, logger=None):
    #  should look for bbc.com/news ?
    #  could also look for the integer on the end

    # if url == 'https://www.bbc.com/food':
    #     return False
    # if url == 'https://www.bbc.com/weather':
        # return False

    #  check to see if url ends with an integer
    import re
    matcher = re.compile('.*-\d*')
    if not matcher.match(url):
        return False

    if '/pages.emails.bbc.com/' in url:
        return False
    if '/localnews/' in url:
        return False
    if '/indonesia/' in url:
        return False
    if '/av/' in url:
        return False
    if '/iplayer/' in url:
        return False
    if '/weather/' in url:
        return False
    if '/newsround/home' in url:
        return False
    if '/learningenglish/' in url:
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
    if 'magazine' in url:
        return False
    if '/culture/' in url:
        return False

    #  maybe
    if '/travel/' in url:
        return False

    if '/bitesize/' in url:
        return False
    if '/video/' in url:
        return False
    if '/mediaaction/' in url:
        return False
    if '/comments' in url:
        return False
    if '/live/' in url:
        return False


    #  wierd redirect to /av/
    if url == 'https://www.bbc.com/news/science-environment-52926683':
        return False
    #  `The papers` - just a list of images
    #  not sure how to check without parsing
    if url == 'https://www.bbc.com/news/uk-scotland-53961637':
        return False
    if url == 'https://www.bbc.com/news/science_and_environment':
        return False
    return True


def parse_bbc_url(url, logger=None):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")

    try:
        body = find_one_tag(soup, 'div', {'property': 'articleBody'})
        body = body.findAll("p")
    except AssertionError:
        #  TODO there must be a better way
        try:
            body = find_one_tag(soup, 'article')
            body = body.findAll("div")
        except AssertionError:
            #  https://www.bbc.com/news/uk-scotland-47746289
            body = find_one_tag(soup, 'div', {'class':'story-body'})
            body = body.findAll("div")

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
    url = 'https://www.bbc.com/news/world-australia-50341210'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")
    out = parse_bbc_url(url)
