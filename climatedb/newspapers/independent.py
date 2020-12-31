import re

from climatedb import utils


def check_url(url):
    if len(url.split('/')) != 5:
        return False
    if "independent.co.uk/topic/" in url:
        return False
    if url == "https://www.independent.co.uk/environment/climate-change":
        return False
    return url


def get_article_id(url):
    return utils.form_article_id(url, -1)


def parse_url(url):
    headers = {'User-Agent':'Mozilla/5.0'}
    response = utils.request(url, headers=headers)
    soup = response['soup']
    html = response['html']

    body = utils.find_one_tag(soup, 'div', {'id': 'main'})
    body = [p.text for p in body.findAll('p') if p.attrs == {} or p.attrs == {'dir': 'ltr'}]
    body = ''.join(body)

    app = utils.find_application_json(soup, 'headline')
    headline = app['headline']
    published = app['datePublished']

    return {
        **independent,
        "body": body,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": get_article_id(url),
        "date_published": published,
    }


independent = {
    "newspaper_id": "independent",
    "newspaper": "The Independent",
    "newspaper_url": "independent.co.uk",

    "checker": check_url,
    "parser": parse_url,
    "get_article_id": get_article_id,
    "color": "#E30D24"
}
