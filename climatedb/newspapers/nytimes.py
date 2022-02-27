import re
from urllib.parse import urlparse

from climatedb import utils


def check_url(url):
    #  TODO TEST
    u = urlparse(url)
    unwanted = set(
        [
            "interactive",
            "topic",
            "spotlight",
            "times-journeys",
            "freakonomics.blogs.nytimes.com",
            "newsletters",
            "ask",
            "video",
        ]
    )

    if u.path and u.path.split("/")[1] in unwanted:
        return False
    return url


def get_article_id(url):
    return utils.form_article_id(url, -1)


def parse_url(url):
    response = utils.request(url)
    soup = response["soup"]
    html = response["html"]

    body = utils.find_one_tag(soup, "section", {"name": "articleBody"})
    body = "".join([p.text for p in body.findAll("p")])
    noise = [
        "The Times is committed to publishing a diversity of letters to the editor. We’d like to hear what you think about this or any of our articles. Here are some tips. And here’s our email: letters@nytimes.com.Follow The New York Times Opinion section on Facebook, Twitter (@NYTopinion) and Instagram.",
        "Want climate news in your inbox? Sign up here for Climate Fwd:, our email newsletter.",
        "For more news on climate and the environment, follow @NYTClimate on Twitter.",
    ]
    for n in body:
        body.replace(n, "")

    app = utils.find_application_json(soup, "headline")
    headline = app["headline"]
    published = app["datePublished"]

    return {
        **nytimes,
        "body": body,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": get_article_id(url),
        "date_published": published,
    }


nytimes = {
    "newspaper_id": "nytimes",
    "newspaper": "The New York Times",
    "newspaper_url": "nytimes.com",
    "checker": check_url,
    "parser": parse_url,
    "get_article_id": get_article_id,
    "color": "#FFFFFF",
}
