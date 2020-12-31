import re

from climatedb import utils


def check_url(url):
    parts = url.split("/")
    if len(parts) < 7:
        return False

    for unw in ["events.stuff.co.nz", "interactives.stuff.co.nz"]:
        if unw in url:
            return False

    return url


def get_article_id(url):
    return utils.form_article_id(url, -1)


def parse_url(url):
    response = utils.request(url)
    soup = response['soup']
    html = response['html']

    body = utils.find_one_tag(soup, "span", {"class": "sics-component__story__body sics-component__story__body--nativform"})
    body = "".join([p.text for p in body.findAll("p")])

    published = soup.findAll("meta", attrs={"itemprop": "datePublished"})
    assert len(published) == 1
    published = published[0]["content"]

    headline = soup.findAll("h1", attrs={"itemprop": "headline"})
    assert len(headline) == 1
    headline = headline[0].text

    return {
        **stuff,
        "body": body,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": get_article_id(url),
        "date_published": published,
    }


stuff = {
    "newspaper_id": "stuff",
    "newspaper": "Stuff.co.nz",
    "newspaper_url": "stuff.co.nz",

    "checker": check_url,
    "parser": parse_url,
    "get_article_id": get_article_id,
    "color": "#00C386"
}
