from datetime import datetime
import json
import logging

from bs4 import BeautifulSoup
import requests

from climatedb.utils import find_one_tag, form_article_id



def application_json_helper(soup):
    app = soup.findAll("script", {"type": "application/ld+json"})
    for a in app:
        try:
            print(a["type"])
        except KeyError:
            pass


def strip_aljazzera_dt(date_str):
    try:
        date = datetime.strptime(date_str, "%d %b %Y %H:%M GMT")
    except ValueError:
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
    return date.isoformat() 


def check_aljazzera_url(url, logger=None):
    res = requests.get(url, allow_redirects=True)
    logger.info(f"newspaper=aljazeera, url={url}, redirect={res.url}")
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
    return True


def parse_aljazzera_url(url, logger=None):
    logger = logging.getLogger("climatedb")
    response = requests.get(url, allow_redirects=True)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")

    try:
        body = find_one_tag(soup, "div", {"class": "main-article-body"})
        body = body.findAll("p")
    except AssertionError:
        #  possible to have multiple 'text section' divs
        body = soup.findAll("div", {"class": "text section"})
        p_tags = []
        for b in body:
            p_tags.extend(b.findAll("p"))
        body = p_tags

    if len(body) == 0:
        body = find_one_tag(soup, "div", {"class": "wysiwyg wysiwyg--all-content"})
        body = body.findAll("p")

    body = "".join(p.text for p in body)

    #  hoping it is the firstone
    #  there are usually 2/3 ld/json
    app = soup.findAll("script", {"type": "application/ld+json"})
    if len(app) == 0:
        return {"error": "no application/ld+json"}

    assert len(app) >= 1
    app = app[0].text.replace("\n", "")
    app = json.loads(app)

    return {
        "newspaper_id": "aljazeera",
        "body": body,
        "article_id": form_article_id(url),
        "headline": app["headline"],
        "article_url": url,
        "html": html,
        "date_published": strip_aljazzera_dt(app["datePublished"]),
        "date_modified": strip_aljazzera_dt(app["dateModified"]),
    }


aljazeera = {
    "newspaper_id": "aljazeera",
    "newspaper": "Al Jazeera",
    "newspaper_url": "aljazeera.com",
    "checker": check_aljazzera_url,
    "parser": parse_aljazzera_url,
    "color": "#FA9000",
}
if __name__ == "__main__":
    url = "http://www.aljazeera.com/news/europe/2007/02/2008525144121633730.html"
    response = requests.get(url, allow_redirects=False)

    par = parse_aljazzera_url(url)
