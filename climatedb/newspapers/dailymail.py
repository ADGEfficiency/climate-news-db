from bs4 import BeautifulSoup
import requests

from climatedb.newspapers.utils import find_one_tag, form_article_id, find_application_json



def check_dailymail_url(url, logger=None):
    if len(url.split('/')) != 6:
        return False
    return True


def parse_dailymail_url(url, logger=None):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")

    body = find_one_tag(soup, 'div', {'itemprop': 'articleBody'})
    body = [p.text for p in body.findAll('p')]
    body = ''.join(body)

    app = find_application_json(soup)

    date_published = app["datePublished"]
    date_modified = app["dateModified"]

    #  one article has "" date_published
    #  https://www.dailymail.co.uk/news/article-1232412/Director-climate-change-centre-accused-manipulating-data-stands-dismisses-claims-complete-rubbish.html
    if date_published == "":
        date_published = date_modified

    return {
        "newspaper_id": "dailymail",
        "body": body,
        "article_id": form_article_id(url, idx=-1),
        "headline": app['headline'],
        "article_url": url,
        "html": html,
        "date_published": date_published,
        "date_modified": date_modified
    }


dailymail = {
    "newspaper_id": "dailymail",
    "newspaper": "The Daily Mail",
    "newspaper_url": "https://www.dailymail.co.uk",
    "checker": check_dailymail_url,
    "parser": parse_dailymail_url,
    "color": "#004DB3"
}


if __name__ == "__main__":
    url = "https://www.dailymail.co.uk/news/article-1232412/Director-climate-change-centre-accused-manipulating-data-stands-dismisses-claims-complete-rubbish.html"
    parsed = parse_dailymail_url(url)
