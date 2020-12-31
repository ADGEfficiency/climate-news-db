import re
from urllib.parse import urlparse
from climatedb.utils import ParserError

from climatedb.utils import find_one_tag, form_article_id, request, find_single_application_json

from climatedb import utils


def check_guardian_url(url):
    #  many redirects
    if 'covid-19-what-kind-of-face-mask-gives-the-best-protection-against-coronavirus' in url:
        return False

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
    article_id = form_article_id(url, idx=-1)
    return article_id.split('|')[0]


def parse_guardian_html(url):
    r = request(url)

    html = r['html']
    soup = r['soup']

    try:
        body = find_one_tag(soup, 'div', {'class': 'article-body-commercial-selector css-79elbk article-body-viewer-selector'})

    except ParserError as error:
        body = find_one_tag(soup, 'div', {'itemprop': 'articleBody'})

    body = "".join([p.text for p in body.findAll("p")])

    headline = find_one_tag(soup, 'meta', {'property': 'og:title'})['content']
    published = find_one_tag(soup, 'meta', {'property': 'article:published_time'})['content']

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
