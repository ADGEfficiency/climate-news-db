import re
import json

from climatedb import utils


def check_for_strong_link(p):
    """Looking for a strong tag inside a link"""
    for child in p.children:
        if child.name == "strong":
            print(f"not taking {child.text}")
            return True

        if child.name == "a":
            for child in child.children:
                if child.name == "strong":
                    print(f"not taking {child.text}")
                    return True


def check_url(url):
    unwanted = ["category", "video", "radio", "person"]
    if not utils.check_match(url, unwanted):
        return False
    return url


def get_article_id(url):
    return utils.form_article_id(url, -1)


def parse_url(url):
    response = utils.request(url)
    soup = response['soup']
    html = response['html']

    body = utils.find_one_tag(soup, "div", {"class": "article-body"})
    body = "".join([p.text for p in body.findAll("p") if not check_for_strong_link(p)])

    unwanted = [
        "Fox News Flash top headlines are here. Check out what's clicking on Foxnews.com.",
        "Get all the latest news on\xa0coronavirus\xa0and more delivered daily to your inbox.\xa0Sign up here.",
    ]
    #  hack for coronavirus tag that appears in later articles
    for unw in unwanted:
        body.replace(unw, "")

    #  TODO
    scripts = soup.findAll("script", attrs={"type": "application/ld+json"})
    assert len(scripts) == 2
    app = str(scripts[0].contents[0])
    app = app.replace("\n", "")
    app = json.loads(app)
    headline = app['headline']
    published = app['datePublished']

    return {
        **fox,
        "body": body,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": get_article_id(url),
        "date_published": published,
    }


fox = {
    "newspaper_id": "fox",
    "newspaper": "Fox News",
    "newspaper_url": "foxnews.com",

    "checker": check_url,
    "parser": parse_url,
    "get_article_id": get_article_id,
    "color": "#003366"
}
