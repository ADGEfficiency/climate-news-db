import re
from urllib.parse import urlparse

from climatedb.utils import find_one_tag, form_article_id, request, find_single_application_json


def check_url(url):
    #  wierd redirect to /av/
    if url == 'https://www.bbc.com/news/science-environment-52926683':
        return False
    #  `The papers` - just a list of images - not sure how to check without parsing
    if url == 'https://www.bbc.com/news/uk-scotland-53961637':
        return False
    if url == 'https://www.bbc.com/news/science_and_environment':
        return False

    #  check to see if it is news section
    u = urlparse(url)
    if u.path and u.path.split('/')[1] != "news":
        return False

    if len(u.path.split('/')) > 3:
        return False

    #  check to see if it redirects
    res = request(url)
    if res['response'].status_code == 404:
        return False
    elif res['url'] != url:
        return check_url(res['url'])

    #  check to see if url ends with an integer
    matcher = re.compile('.*-\d*')
    if matcher.match(url):
        return url


def parse_url(url):
    r = request(url)
    if 'error' in r.keys():
        return {
            'error': r['error']
        }
    html = r['html']
    soup = r['soup']

    body = find_one_tag(soup, 'article')
    text_blocks = body.findAll("div", attrs={'data-component': 'text-block'})

    body = []
    for block in text_blocks:
        body.extend(block.findAll("p", attrs={'class': None}))

    deep_body = []
    for p_tag in body:
        #  style tags were slipping into the p tag
        for s in p_tag('style'):
            s.decompose()

        text = p_tag.get_text()
        #  last link tag, often a link to Twitter or Read more here
        if p_tag.find('a') and p_tag is body[-1]:
            pass
        else:
            deep_body.append(text)

    body = "".join(deep_body)

    app = find_single_application_json(soup)
    if 'error' in app.keys():
        import pdb; pdb.set_trace()

    return {
        "newspaper_id": "bbc",
        "body": body,
        "article_id": get_bbc_article_id(url),
        "headline": app['headline'],
        "article_url": url,
        "html": html,
        "date_published": app["datePublished"],
    }


def get_bbc_article_id(url):
    return form_article_id(url, idx=-1)


bbc = {
    "newspaper_id": "bbc",
    "newspaper": "The BBC",
    "newspaper_url": "bbc.com",
    "checker": check_url,
    "parser": parse_url,
    "get_article_id": get_bbc_article_id,
    "color": "#0098FF"
}


if __name__ == '__main__':

    parsed = parse_url('https://www.bbc.com/news/world-europe-48221080')
