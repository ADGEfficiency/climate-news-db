import re

from climatedb import utils


def check_url(url):
    if ".washingtonpost.com/graphics" in url:
        return False
    if "washingtonpost.com/video/" in url:
        return False
    if "washingtonpost.com/wp-srv/nation/interactives/" in url:
        return False
    if url == "https://www.washingtonpost.com/climate-solutions/":
        return False
    if (
        url
        == "https://www.washingtonpost.com/wp-srv/inatl/longterm/climate/background.htm"
    ):
        return False
    if url == "https://www.washingtonpost.com/climate-environment/":
        return False
    if (
        url
        == "https://www.washingtonpost.com/news/energy-environment/wp/category/climate-change/"
    ):
        return False
    if url.endswith(".pdf"):
        return False
    if url == "washingtonpost.com/wp-srv/inatl/longterm/climate/overview.htm":
        return False
    if (
        url
        == "https://www.washingtonpost.com/wp-srv/inatl/longterm/climate/overview.htm"
    ):
        return False
    if url == "https://www.washingtonpost.com/energy-policy/":
        return False
    return True


def get_article_id(url):
    return utils.form_article_id(url, -1)


def parse_url(url):
    response = utils.request(url)
    soup = response["soup"]
    html = response["html"]

    try:
        body = utils.find_one_tag(soup, "div", {"class": "article-body"})

    except utils.ParserError:
        body = utils.find_one_tag(
            soup, "div", {"class": "ent-article-body ent-layout-centered"}
        )

    new_body = []
    for p in body.findAll("p"):

        if "data-elm-loc" in p.attrs.keys():
            new_body.append(p.text)

        if "class" in p.attrs.keys():
            if "font--body" in p.attrs["class"]:
                new_body.append(p.text)

    body = "".join(new_body)
    app = utils.find_application_json(soup, "headline")
    headline = app["headline"]
    published = app["datePublished"]

    return {
        **washington_post,
        "body": body,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": get_article_id(url),
        "date_published": published,
    }


washington_post = {
    "newspaper_id": "washington_post",
    "newspaper": "The Washington Post",
    "newspaper_url": "washingtonpost.com",
    "checker": check_url,
    "parser": parse_url,
    "get_article_id": get_article_id,
    "color": "#000000",
}
