from bs4 import BeautifulSoup
import requests


def check_match(url, unwanted):
    for unw in unwanted:
        if unw in url:
            return False
    return True


def find_one_tag(soup, name, attrs={}):
    """find a single tag (and only one tag) in bs4"""
    data = soup.findAll(name, attrs)
    if len(data) != 1:
        print(soup.url, name, attrs, len(data))
    assert len(data) == 1
    return data[0]


def form_article_id(url, idx=-1):
    url = url.strip("/")
    url = url.split("?")[0]
    article_id = url.split("/")[idx]
    return article_id.replace(".html", "")


def find_application_json(soup, find='headline'):
    import json
    apps = soup.findAll('script', {'type': 'application/ld+json'})
    for app in apps:
        app = json.loads(app.text)
        if find in app:
            return app

    return {
        'error': 'no application JSON'
    }

#  from bbc
# import json#
# def find_application_json(soup):
#     app = find_one_tag(soup, 'script', {'type': 'application/ld+json'}).text
#     app = app.replace('\n', '')
#     return json.loads(app)

import time
import random
def request(url):
    time.sleep(random.randint(0, 2))
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")
    if response.status_code == 200:
        return {
            'response': response,
            'html': html,
            'soup': soup,
            'url': response.url
        }

    return {
        'error': response.status_code
    }
