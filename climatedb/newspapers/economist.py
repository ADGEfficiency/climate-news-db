import json
import re

from climatedb import utils

def clean_string(string, unwanted):
    for unw in unwanted:
        string = string.replace(unw, "")
    return string


def check_url(url):
    parts = url.split("/")
    if parts[3] == "1843":
        return False

    #  page not found error
    if (url== "https://www.economist.com/prospero/2020/01/09/how-to-save-culture-from-climate-change"):
        return False

    #  not an article
    if url == "https://www.economist.com/news/2020/04/24/the-economists-coverage-of-climate-change":
        return False

    pattern = re.compile("\/\d{4}\/\d{2}\/\d{2}\/")
    match = pattern.findall(url)

    if len(match) == 1:
        return url
    return False


def get_article_id(url):
    return utils.form_article_id(url, -1)


def parse_url(url):
    response = utils.request(url)
    soup = response['soup']
    html = response['html']

    body = utils.find_one_tag(soup, "div", {"itemprop": "text", "class": "ds-layout-grid ds-layout-grid--edged layout-article-body"})


    new_body = []
    for p_tag in body.findAll("p"):
        if 'class' in p_tag.attrs.keys():
            if 'article__body' in p_tag.attrs['class'][0]:
                new_body.append(p_tag.text)

    body = new_body
    body = "".join(body)
    unwanted = [
        "For more coverage of climate change, register for The Climate Issue, our fortnightly newsletter, or visit our climate-change hub",
        'Sign up to our new fortnightly climate-change newsletter hereThis article appeared in the Leaders section of the print edition under the headline "The climate issue"',
    ]
    body = clean_string(body, unwanted)

    headline = utils.find_one_tag(soup, "span", {"class": "article__headline", "itemprop": "headline"}).text

    app = utils.find_one_tag(soup, "script", {"type": "application/json"})
    app = json.loads(app.text)

    if 'metadata' in app["props"]["pageProps"].keys():
        meta = app["props"]["pageProps"]["metadata"]
        published = meta["datePublished"]
    else:
        published = app['props']['pageProps']['content'][0]['datePublished']

    return {
        **economist,
        "body": body,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": get_article_id(url),
        "date_published": published,
    }


economist = {
    "newspaper_id": "economist",
    "newspaper": "The Economist",
    "newspaper_url": "economist.com",

    "checker": check_url,
    "parser": parse_url,
    "get_article_id": get_article_id,
    "color": "#E3120B"
}
