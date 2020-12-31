import re

from climatedb import utils


def check_url(url):
    if len(url.split('/')) != 6:
        return False
    return url


def get_article_id(url):
    return utils.form_article_id(url, -1)


def parse_url(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = utils.request(url, headers=headers)
    soup = response['soup']
    html = response['html']

    body = utils.find_one_tag(soup, "div", {"itemprop": "articleBody"})
    body = "".join([p.text for p in body.findAll("p")[:-1]])

    headline = utils.find_one_tag(soup, 'title').text.split('|')[0]

    published = utils.find_one_tag(soup, 'meta', {'property': 'article:published_time'})['content']

    return {
        **dailymail,
        "body": body,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": get_article_id(url),
        "date_published": published,
    }


dailymail = {
    "newspaper_id": "dailymail",
    "newspaper": "The Daily Mail",
    "newspaper_url": "https://www.dailymail.co.uk",

    "checker": check_url,
    "parser": parse_url,
    "get_article_id": get_article_id,
    "color": "#004DB3"
}
