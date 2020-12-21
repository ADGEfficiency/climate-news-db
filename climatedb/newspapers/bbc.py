import re
from urllib.parse import urlparse

from climatedb.utils import find_one_tag, form_article_id, request, find_application_json


def check_url(url, logger=None):
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
    r = request(url)
    if r['url'] != url:
        return check_url(r['url'])

    #  check to see if url ends with an integer
    matcher = re.compile('.*-\d*')
    if matcher.match(url):
        return True


def parse_url(url, logger=None):
    r = request(url)
    if 'error' in r.keys():
        return {
            'error': r['error']
        }
    html = r['html']
    soup = r['soup']

    body = find_one_tag(soup, 'article')
    body = body.findAll("p", attrs={'class': None})

    #  sometimes first tag has a `b` element in it
    deep_body = []
    for p_tag in body:
        if p_tag.find('b'):
            deep_body.append(p_tag.find('b').text)
        else:
            deep_body.append(p_tag.text)

    body = "".join(deep_body)

    app = find_application_json(soup)
    if 'error' in app.keys():
        import pdb; pdb.set_trace()

    return {
        "newspaper_id": "bbc",
        "body": body,
        "article_id": form_article_id(url, idx=-1),
        "headline": app['headline'],
        "article_url": url,
        "html": html,
        "date_published": app["datePublished"],
        "date_modified": app["dateModified"],
    }


bbc = {
    "newspaper_id": "bbc",
    "newspaper": "The BBC",
    "newspaper_url": "bbc.com",
    "checker": check_url,
    "parser": parse_url,
    "color": "#0098FF"
}


if __name__ == '__main__':
    url = 'https://www.bbc.com/news/election-us-2020-53785985'
    r = request(url)


    # parsed = parse_url(url)
