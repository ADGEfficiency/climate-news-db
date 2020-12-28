import re
from urllib.parse import urlparse

from climatedb.utils import find_one_tag, form_article_id, request, find_application_json


def check_guardian_url(url):
    #  searching for a string like 2020/may/14
    expr = "\d{4}\/[a-z]{3}\/\d{2}"
    matches = re.findall(expr, url)
    if not matches:
        return False

    u = urlparse(url)
    unwanted = ["live", "gallery", "audio", "video", "ng-interactive", "interactive"]
    if u.path and u.path.split('/')[2] in unwanted:
        return False

    return True


def get_guardian_article_id(url):
    return form_article_id(url, idx=-1)


def parse_guardian_html(url):
    r = request(url)
    if 'error' in r.keys():
        return {'error': r['error']}

    html = r['html']
    soup = r['soup']

    body = find_one_tag(soup, 'div', {"itemprop": "articleBody"})
    body = "".join([p.text for p in body.findAll("p")])

    published = find_one_tag(soup, 'time', {"itemprop": "datePublished"})['datetime']
    headline = find_one_tag(soup, 'title').text

    return {
        "newspaper_id": "guardian",
        "body": body,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": get_guardian_article_id(url),
        "date_published": published,
    }


guardian = {
    "newspaper_id": "guardian",
    "newspaper": "The Guardian",
    "newspaper_url": "theguardian.com",
    "checker": check_guardian_url,
    "parser": parse_guardian_html,
    "get_article_id": get_guardian_article_id,
    "color": "#052962"
}
