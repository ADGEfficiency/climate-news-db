import requests
from bs4 import BeautifulSoup
import json

from climatedb.newspapers.utils import find_one_tag, form_article_id


def check_economist_url(url, logger):
    parts = url.split("/")
    if parts[3] == "1843":
        return False

    #  page not found error
    if (
        url
        == "https://www.economist.com/prospero/2020/01/09/how-to-save-culture-from-climate-change"
    ):
        return False

    #  not an article
    if url == "https://www.economist.com/news/2020/04/24/the-economists-coverage-of-climate-change":
        return False

    import re

    pattern = re.compile("\/\d{4}\/\d{2}\/\d{2}\/")
    match = pattern.findall(url)
    if len(match) == 1:
        return True
    return False


def clean_string(string, unwanted):
    for unw in unwanted:
        string = string.replace(unw, "")
    return string


def parse_economist_url(url, logger=None):
    import time

    #  error without the sleep
    time.sleep(1)
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")

    headline = find_one_tag(
        soup, "span", {"class": "article__headline", "itemprop": "headline"}
    ).text

    body = find_one_tag(
        soup,
        "div",
        {
            "itemprop": "text",
            "class": "ds-layout-grid ds-layout-grid--edged layout-article-body",
        },
    )
    body = body.findAll("p")
    body = "".join(p.text for p in body)

    unwanted = [
        "For more coverage of climate change, register for The Climate Issue, our fortnightly newsletter, or visit our climate-change hub",
        'Sign up to our new fortnightly climate-change newsletter hereThis article appeared in the Leaders section of the print edition under the headline "The climate issue"',
    ]
    body = clean_string(body, unwanted)

    app = find_one_tag(soup, "script", {"type": "application/json"})
    app = json.loads(app.text)
    meta = app["props"]["pageProps"]["metadata"]
    published = meta["datePublished"]
    modified = meta["dateModified"]

    return {
        "newspaper_id": "economist",
        "body": body,
        "article_id": form_article_id(url),
        "headline": headline,
        "article_url": url,
        "html": html,
        "date_published": published,
        "date_modified": modified,
    }


economist = {
    "newspaper_id": "economist",
    "newspaper": "The Economist",
    "newspaper_url": "economist.com",
    "checker": check_economist_url,
    "parser": parse_economist_url,
}


if __name__ == "__main__":
    url = "https://www.economist.com/briefing/2010/11/25/facing-the-consequences"
    url = "https://www.economist.com/books-and-arts/2019/05/16/climate-change-strikes-the-venice-biennale"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")

    headline = find_one_tag(
        soup, "span", {"class": "article__headline", "itemprop": "headline"}
    ).text
