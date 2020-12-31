import re

from climatedb import utils


def check_url(url):
    if "/gallery/" in url:
        return False
    if "/videos/" in url:
        return False
    if "/travel/" in url:
        return False
    if url == "https://www.cnn.com/weather":
        return False
    if url == "https://edition.cnn.com/specials/opinions/two-degrees":
        return False
    if "/interactive/" in url:
        return False
    if "/live-news/" in url:
        return False
    if "/profiles/" in url:
        return False
    if "rss.cnn.com" in url:
        return False
    if "lite.cnn.com" in url:
        return False
    if "/videos/" in url:
        return False
    if "edition.cnn.com" in url:
        return False
    if "/specials/" in url:
        return False
    if "e.newsletters.cnn.com" in url:
        return False
    if url == "https://www.cnn.com/2009/WORLD/europe/07/05/oxfam.climate.change.human.cost/index.html":
        return False
    if url == "https://www.cnn.com/2008/TECH/science/03/31/Intro.timeline/index.html":
        return False
    if url == "https://www.cnn.com/2009/WORLD/europe/05/29/annan.climate.change.human/index.html":
        return False
    if url == "https://www.cnn.com/world":
        return False
    if url == "https://www.cnn.com/audio":
        return False
    if "/2009/" in url:
        return False
    if "/2008/" in url:
        return False
    return url


def get_article_id(url):
    return utils.form_article_id(url, -2)


def parse_url(url):
    response = utils.request(url)
    soup = response['soup']
    html = response['html']

    body = utils.find_one_tag(soup, "div", {"itemprop": "articleBody"})
    body = "".join([p.text for p in body.findAll("p")])
    import pdb; pdb.set_trace()

    if len(body) == 0:
        body = utils.find_one_tag(soup, "div", {"itemprop": "articleBody"})
        body = body.findAll("div")[0]
        body = "".join([p.text for p in body.findAll("p")])

    headline = utils.find_one_tag(soup, 'title', {"id": None}).text.replace(" - CNN", "")
    published = utils.find_one_tag(soup, 'meta', {'itemprop': 'datePublished'})
    published = published['content']

    return {
        **cnn,
        "body": body,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": get_article_id(url),
        "date_published": published
    }


cnn = {
    "newspaper_id": "cnn",
    "newspaper": "CNN",
    "newspaper_url": "cnn.com",

    "checker": check_url,
    "parser": parse_url,
    "get_article_id": get_article_id,
    "color": "#CC0000"
}
