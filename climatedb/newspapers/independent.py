from bs4 import BeautifulSoup
import requests

from climatedb.newspapers.utils import find_one_tag, form_article_id, find_application_json



def check_independent_url(url, logger=None):
    if len(url.split('/')) != 5:
        return False
    if "independent.co.uk/topic/" in url:
        return False
    return True


def parse_independent_url(url, logger=None):
    headers = {'User-Agent':'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")
    body = find_one_tag(soup, 'div', {'id': 'main'})
    body = [p.text for p in body.findAll('p') if p.attrs == {} or p.attrs == {'dir': 'ltr'}]
    body = ''.join(body)
    #out = parse_independent_url(url)

    app = find_application_json(soup)

    return {
        "newspaper_id": "independent",
        "body": body,
        "article_id": form_article_id(url, idx=-1),
        "headline": app['headline'],
        "article_url": url,
        "html": html,
        "date_published": app["datePublished"],
        "date_modified": app["dateModified"],
    }


independent = {
    "newspaper_id": "independent",
    "newspaper": "The Independent",
    "newspaper_url": "independent.co.uk",
    "checker": check_independent_url,
    "parser": parse_independent_url,
    "color": "#E30D24"
}


if __name__ == "__main__":
    url = "https://www.independent.co.uk/environment/climate-change-decade-record-temperature-fridays-future-environment-crisis-a9267601.html"
    out = parse_independent_url(url)
