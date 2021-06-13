import re

from climatedb import utils


def check_url(url):
    if "theatlantic.com/video/" in url:
        return False
    if "theatlantic.com/sponsored/" in url:
        return False
    if "theatlantic.com/photo" in url:
        return False
    if "theatlantic.com/author" in url:
        return False
    if "theatlantic.com/author" in url:
        return False
    if "theatlantic.com/projects" in url:
        return False
    # https://www.theatlantic.com/notes/2016/04/climate-change-game-theory-models/479340/
    # actually looks useful, but a much different structure
    if "theatlantic.com/notes" in url:
        return False
    if url == "https://www.theatlantic.com/latest/":
        return False
    return url


def get_article_id(url):
    return utils.form_article_id(url, -1)


def parse_url(url):
    response = utils.request(url)
    soup = response['soup']
    html = response['html']

    try:
        body = utils.find_one_tag(soup, 'article')
        body = ''.join([p.text for p in body.findAll('p')])

    except utils.ParserError:
        body = utils.find_one_tag(
            soup,
            "div",
            {"class": "article-body js-article-container", "itemprop": "articleBody"}
        )
        body = body.findAll("p")
        body = "".join(p.text for p in body if "c-letters-cta__text" not in p.attrs.values())

    app = utils.find_application_json(soup, 'headline')

    headline = app['headline']
    #  sometimes can be "" in the ld+json
    if headline == "":
        headline = utils.find_one_tag(soup, "h1", {"class": "c-article-header__hed"}).text

    published = app['datePublished']

    return {
        **atlantic,
        "body": body,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": get_article_id(url),
        "date_published": published,
    }


atlantic = {
    "newspaper_id": "atlantic",
    "newspaper": "The Atlantic",
    "newspaper_url": "theatlantic.com",

    "checker": check_url,
    "parser": parse_url,
    "get_article_id": get_article_id,
    "color": "#FA9000",
}
