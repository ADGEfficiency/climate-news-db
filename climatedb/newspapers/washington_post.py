import json

from bs4 import BeautifulSoup
import requests

from climatedb.newspapers.utils import find_one_tag, form_article_id


def check_washington_post_url(url, logger=None):
    if ".washingtonpost.com/graphics" in url:
        return False
    if "washingtonpost.com/video/" in url:
        return False
    if "washingtonpost.com/wp-srv/nation/interactives/" in url:
        return False
    if url == "https://www.washingtonpost.com/climate-solutions/":
        return False
    if (
        url
        == "https://www.washingtonpost.com/wp-srv/inatl/longterm/climate/background.htm"
    ):
        return False
    if url == "https://www.washingtonpost.com/climate-environment/":
        return False
    if url == "https://www.washingtonpost.com/news/energy-environment/wp/category/climate-change/":
        return False
    if url.endswith('.pdf'):
        return False
    if url == "washingtonpost.com/wp-srv/inatl/longterm/climate/overview.htm":
        return False
    if url == "https://www.washingtonpost.com/wp-srv/inatl/longterm/climate/overview.htm":
        return False
    return True


def parse_washington_post_url(url, logger=None):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")

    try:
        body = find_one_tag(soup, "div", {"class": "article-body"})
    except AssertionError:
        body = find_one_tag(soup, "div", {"class": "ent-article-body ent-layout-centered"})

    body = body.findAll("p")
    body = "".join(p.text for p in body)

    #  <script type="application/ld+json" data-qa="schema">
    app = find_one_tag(soup, "script", {"type": "application/ld+json"})
    app = json.loads(app.text)

    return {
        "newspaper_id": "washington_post",
        "body": body,
        "article_id": form_article_id(url),
        "headline": app["headline"],
        "article_url": url,
        "html": html,
        "date_published": app["datePublished"]
    }


washington_post = {
    "newspaper_id": "washington_post",
    "newspaper": "The Washington Post",
    "newspaper_url": "washingtonpost.com",
    "checker": check_washington_post_url,
    "parser": parse_washington_post_url,
    "color": "#000000",
}


if __name__ == "__main__":
    url = "https://www.washingtonpost.com/climate-solutions/2020/02/24/can-you-pass-this-10-question-climate-quiz/"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")
    out = parse_washington_post_url(url)
    app = find_one_tag(soup, "script", {"type": "application/ld+json"})
    app = json.loads(app.text)
