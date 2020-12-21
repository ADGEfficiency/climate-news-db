
import json

from bs4 import BeautifulSoup
import requests

from climatedb.utils import find_one_tag, form_article_id


def check_cnn_url(url, logger=None):
    if "/gallery/" in url:
        return False
    if "/videos/" in url:
        return False
    if "/travel/" in url:
        return False
    if url == "https://www.cnn.com/weather":
        return False
    if url == "https://edition.cnn.com/specials/opinions/two-degrees":
        return False
    if "/interactive/" in url:
        return False
    if "/live-news/" in url:
        return False
    if "/profiles/" in url:
        return False
    if "rss.cnn.com" in url:
        return False
    if "lite.cnn.com" in url:
        return False
    if "/videos/" in url:
        return False
    if "edition.cnn.com" in url:
        return False
    if "/specials/" in url:
        return False
    if "e.newsletters.cnn.com" in url:
        return False
    if url == "https://www.cnn.com/2009/WORLD/europe/07/05/oxfam.climate.change.human.cost/index.html":
        return False
    if url == "https://www.cnn.com/2008/TECH/science/03/31/Intro.timeline/index.html":
        return False
    if url == "https://www.cnn.com/2009/WORLD/europe/05/29/annan.climate.change.human/index.html":
        return False
    if url == "https://www.cnn.com/world":
        return False
    if url == "https://www.cnn.com/audio":
        return False
    if "/2009/" in url:
        return False
    if "/2008/" in url:
        return False
    return True


def parse_cnn_url(url, logger=None):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")

    body = find_one_tag(soup, "div", {"itemprop": "articleBody"})
    body = body.findAll("p")
    body = "".join(p.text for p in body)

    if len(body) == 0:
        body = find_one_tag(soup, "div", {"itemprop": "articleBody"})
        body = body.findAll("div")
        body = "".join(p.text for p in body)

    headline = find_one_tag(soup, 'title', {"id": None}).text.strip(" - CNN")

    date_published = find_one_tag(soup, 'meta', {'itemprop': 'datePublished'})
    date_published = date_published['content']

    return {
        "newspaper_id": "cnn",
        "body": body,
        "article_id": form_article_id(url, idx=-2),
        "headline": headline,
        "article_url": url,
        "html": html,
        "date_published": date_published,
    }


cnn = {
    "newspaper_id": "cnn",
    "newspaper": "CNN",
    "newspaper_url": "cnn.com",
    "checker": check_cnn_url,
    "parser": parse_cnn_url,
    "color": "#CC0000"
}


if __name__ == "__main__":
    url = "https://edition.cnn.com/2020/08/13/world/state-of-climate-report-2019-intl-hnk-scn/index.html"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")
    out = parse_cnn_url(url)
