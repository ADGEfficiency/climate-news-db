import re

from climatedb import utils


def check_url(url):
    if "storytag.:storyTag=newshub:tag-library" in url:
        return False
    if 'https://www.newshub.co.nz/home/world/environment.html' in url:
        return False
    if url == "https://www.newshub.co.nz/home/world/2020/09/climate-change-richest-1-percent-of-world-s-population-driving-heating-emissions-research.html":
        return False
    return url


def get_article_id(url):
    return utils.form_article_id(url, -1).split('|')[0]


def parse_url(url):
    response = utils.request(url)
    soup = response['soup']
    html = response['html']

    body = utils.find_one_tag(soup, "div", {"itemprop": "articleBody"})
    body = "".join([p.text for p in body.findAll("p")[:-1]])

    noise = [
        "This article is republished from The Conversation under a Creative Commons license. Read the original article here. ",
    ]
    for n in noise:
        body = body.replace(n, "")

    headline = utils.find_one_tag(soup, "title").text
    published = utils.find_one_tag(soup, "meta", {"itemprop": "datePublished"})["content"]

    return {
        **newshub,
        "body": body,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": get_article_id(url),
        "date_published": published,
    }


newshub = {
    "newspaper_id": "newshub",
    "newspaper": "NewsHub.co.nz",
    "newspaper_url": "newshub.co.nz",

    "checker": check_url,
    "parser": parse_url,
    "get_article_id": get_article_id,
    "color": ""
}
