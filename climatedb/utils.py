from bs4 import BeautifulSoup
import requests
import json
import time
import random


def check_match(url, unwanted):
    for unw in unwanted:
        if unw in url:
            return False
    return True


class ParserError(Exception):
    pass


def find_one_tag(soup, name, attrs={}):
    """find a single tag (and only one tag) in bs4"""
    data = soup.findAll(name, attrs)
    if len(data) != 1:
        raise ParserError(name, attrs, len(data))
    return data[0]


def form_article_id(url, idx=-1):
    url = url.strip("/")
    url = url.split("?")[0]
    article_id = url.split("/")[idx]
    article_id = article_id.replace(".html", "")
    article_id = article_id.split("|")[0]
    return article_id


def find_single_application_json(soup):
    app = soup.findAll("script", {"type": "application/ld+json"})

    if len(app) != 1:
        raise ParserError(f"app-json {len(app)}")
    app = json.loads(app[0].text)

    if isinstance(app, list):
        return app[0]
    return app


def find_application_json(soup=None, find="headline"):
    apps = soup.findAll("script", {"type": "application/ld+json"})
    for app in apps:
        app = json.loads(app.text)
        if find in app.keys():
            return app
    raise ParserError(f"no application JSON with {find} in {len(apps)}")


def request(url, headers=None):
    time.sleep(random.randint(1, 3))

    if headers:
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url)

    html = response.text
    soup = BeautifulSoup(html, features="html5lib")
    if response.status_code == 200:
        return {"response": response, "html": html, "soup": soup, "url": response.url}

    response.raise_for_status()
