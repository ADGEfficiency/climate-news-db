import requests
from bs4 import BeautifulSoup

from climatedb.utils import find_one_tag


def check_newshub_url(url, logger=None):
    if "storytag.:storyTag=newshub:tag-library" in url:
        return False
    if 'https://www.newshub.co.nz/home/world/environment.html' in url:
        return False
    if url == "https://www.newshub.co.nz/home/world/2020/09/climate-change-richest-1-percent-of-world-s-population-driving-heating-emissions-research.html":
        return False
    return True


def parse_newshub_url(url, logger=None):
    print(url)
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")

    body = find_one_tag(soup, "div", {"itemprop": "articleBody"})
    body = body.findAll("p")
    body = "".join(p.text for p in body)

    noise = [
        "This article is republished from The Conversation under a Creative Commons license. Read the original article here. ",
    ]
    for n in noise:
        body = body.replace(n, "")

    headline = find_one_tag(soup, "title").text
    published = find_one_tag(soup, "meta", {"itemprop": "datePublished"})["content"]
    modified = find_one_tag(soup, "meta", {"itemprop": "dateModified"})["content"]

    return {
        "newspaper_id": "newshub",
        "body": body,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": url.split("/")[-1],
        "date_published": published,
        "date_modified": modified,
    }


newshub = {
    "newspaper_id": "newshub",
    "newspaper": "NewsHub.co.nz",
    "newspaper_url": "newshub.co.nz",
    "checker": check_newshub_url,
    "parser": parse_newshub_url,
}
