from datetime import datetime
import json

from bs4 import BeautifulSoup
import requests

from newspapers.utils import find_one_tag, form_article_id


def check_atlantic_url(url, logger=None):
    if "theatlantic.com/video/" in url:
        return False
    if "theatlantic.com/sponsored/" in url:
        return False
    if url == "https://www.theatlantic.com/latest/":
        return False
    return True


def parse_atlantic_url(url, logger=None):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")

    body = soup.findAll("div", {"class": "l-article__container js-article-container"})
    body = body[0].findAll("p")
    body = "".join(p.text for p in body if "c-letters-cta__text" not in p.attrs.values())

    apps = soup.findAll("script", {"type": "application/ld+json"})
    app = json.loads(apps[-1].text)

    return {
        "newspaper_id": "atlantic",
        "body": body,
        "article_id": form_atlantic_article_id(url),
        "headline": app["headline"],
        "article_url": url,
        "html": html,
        "date_published": app['datePublished'],
        "date_modified": app['dateModified']
    }


atlantic = {
    "newspaper_id": "atlantic",
    "newspaper": "The Atlantic",
    "newspaper_url": "theatlantic.com",
    "checker": check_atlantic_url,
    "parser": parse_atlantic_url,
    "color": "#FA9000",
}


def form_atlantic_article_id(url):
    # https://www.theatlantic.com/ideas/archive/2020/08/other-way-trump-could-destroy-next-presidency/615130/
    parts = url.split("/")
    return parts[-2]


if __name__ == "__main__":
    url = "https://www.theatlantic.com/science/archive/2019/02/david-wallace-wells-climate-change-interview/583360/"
    url = 'https://www.theatlantic.com/science/archive/2020/01/becoming-parent-age-climate-crisis/604372/'
    par = parse_atlantic_url(url)
