import re

from climatedb import utils


def check_url(url):
    return url


def get_article_id(url):
    return article_id


def parse_url(url):
    response = utils.request(url)
    soup = response['soup']
    html = response['html']


    body = utils.find_one_tag(soup, "section", {"name": "articleBody"})
    body = "".join([p.text for p in body.findAll("p")])

    app = utils.find_application_json(soup, 'headline')
    headline = app['headline']
    published = app['datePublished']

    return {
        **fox,
        "body": body,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": get_article_id(url)
        "date_published": published,
        "date_modified": updated,
    }


fox = {
    "newspaper_id": "fox",
    "newspaper": "Fox News",
    "newspaper_url": "foxnews.com",

    "checker": check_url,
    "parser": parse_url,
    "get_article_id": get_article_id,
    "color": ""
}
