from datetime import datetime
import json

from bs4 import BeautifulSoup
import requests

from climatedb.newspapers.utils import find_one_tag, form_article_id


def application_json_helper(soup):
    app = soup.findAll("script", {"type": "application/ld+json"})
    for a in app:
        try:
            print(a["type"])
        except KeyError:
            pass


def strip_aljazzera_dt(date_str):
    date = datetime.strptime(date_str, "%d %b %Y %H:%M GMT")
    return date.isoformat() + "Z"


def check_aljazzera_url(url, logger=None):
    #  https://www.aljazeera.com/topics/issues/climate-sos.html
    #  http://america.aljazeera.com/topics/topic/issue/climate-change.html
    if (
        ".com/topics/" in url
        or ".com/programmes" in url
        or "inpictures" in url
        or "aljazeera.com/profile" in url
        or "aljazeera.com/podcasts/" in url
    ):
        return False

    if url == "https://www.aljazeera.com/":
        return False
    return True


def parse_aljazzera_url(url, logger=None):
    response = requests.get(url)
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
    url = "https://www.aljazeera.com/ajimpact/davos-world-prepare-millions-climate-refugees-200121175217520.html"
    url = "http://america.aljazeera.com/articles/2015/4/2/UN-climate-change-emissions.html"

    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")
    par = parse_aljazzera_url(url)
