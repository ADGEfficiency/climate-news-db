import re

from climatedb import utils


def check_url(url):
    return url


def get_article_id(url):
    return utils.form_article_id(url, -1)


def parse_url(url):
    response = utils.request(url)
    soup = response['soup']
    html = response['html']

    try:
        body = utils.find_one_tag(soup, "p", {"class": "description-text"})

    except utils.ParserError:
        body = utils.find_one_tag(soup, "p", {"class": "article-text row"})

    body = "".join([p.text for p in body.findAll("p")])

    app = utils.find_application_json(soup, 'headline')
    headline = app['headline']
    published = app['datePublished']

    return {
        **paper,
        "body": body,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": get_article_id(url),
        "date_published": published,
        "date_modified": updated,
    }


paper = {
    "newspaper_id": "",
    "newspaper": "",
    "newspaper_url": "",

    "checker": check_url,
    "parser": parse_url,
    "get_article_id": get_article_id,
    "color": ""
}
