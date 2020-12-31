from datetime import datetime
import re

import requests

from climatedb import utils


def strip_aljazzera_dt(date_str):
    try:
        date = datetime.strptime(date_str, "%d %b %Y %H:%M GMT")
    except ValueError:
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
    return date.isoformat()


def check_url(url):
    return url
    res = requests.get(url, allow_redirects=True)
    url = res.url

    if (
        "aljazeera.com/programmes/" in url
        or "aljazeera.com/inpictures/" in url
        or "aljazeera.com/topics/" in url
        or "aljazeera.com/profile/" in url
        or "aljazeera.com/videos/" in url
        or "aljazeera.com/podcasts/" in url
        or "aljazeera.com/program/" in url
        or "aljazeera.com/features/" in url
    ):
        return False

    if "/tag/" in url:
        return False
    if url == "https://www.aljazeera.com/":
        return False
    if url == "https://www.aljazeera.com/news/":
        return False
    if url == "https://www.aljazeera.com/tag/climate-change/":
        return False

    return url


def get_article_id(url):
    return utils.form_article_id(url, -1)


def parse_url(url):
    response = utils.request(url)
    soup = response['soup']
    html = response['html']

    try:
        body = utils.find_one_tag(soup, "div", {"class": "main-article-body"})
        body = body.findAll("p")

    except utils.ParserError:
        #  possible to have multiple 'text section' divs
        body = soup.findAll("div", {"class": "text section"})
        p_tags = []
        for b in body:
            p_tags.extend(b.findAll("p"))
        body = p_tags

    if len(body) == 0:
        body = utils.find_one_tag(soup, "div", {"class": "wysiwyg wysiwyg--all-content"})
        body = body.findAll("p")

    body = "".join([p.text for p in body])

    app = utils.find_application_json(soup, 'headline')
    headline = app['headline']
    published = app['datePublished']

    return {
        **aljazeera,
        "body": body,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": get_article_id(url),
        "date_published": strip_aljazzera_dt(app["datePublished"]),
    }


aljazeera = {
    "newspaper_id": "aljazeera",
    "newspaper": "Al Jazeera",
    "newspaper_url": "aljazeera.com",

    "checker": check_url,
    "parser": parse_url,
    "get_article_id": get_article_id,
    "color": "#FA9000",
}
