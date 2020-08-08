from datetime import datetime
import json

from bs4 import BeautifulSoup
import requests

from newspapers.utils import find_one_tag, form_article_id


def strip_aljazzera_dt(date_str):
    date = datetime.strptime(date_str, "%d %b %Y %H:%M GMT")
    return date.isoformat() + "Z"


def check_aljazzera_url(url, logger=None):
    #  https://www.aljazeera.com/topics/issues/climate-sos.html
    #  http://america.aljazeera.com/topics/topic/issue/climate-change.html
    if '.com/topics/' in url or '.com/programmes' in url or 'inpictures' in url:
        return False
    return True


def parse_aljazzera_url(url, logger=None):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")

    body = find_one_tag(soup, 'div', {'class': 'article-p-wrapper'})
    body = body.findAll('p')
    body = ''.join(p.text for p in body)

    app = soup.findAll('script', {'type': 'application/ld+json'})
    assert len(app) <= 2
    app = json.loads(app[0].text)

    return {
        "newspaper_id": "aljazeera",
        'body': body,
        'article_id': form_article_id(url),
        'headline': app['headline'],
        'article_url': url,
        'html': html,
        'date_published': strip_aljazzera_dt(app['datePublished']),
        'date_modified': strip_aljazzera_dt(app['dateModified'])
    }


aljazeera = {
    "newspaper_id": "aljazeera",
    "newspaper": "Al Jazeera",
    "newspaper_url": "aljazeera.com",
    "checker": check_aljazzera_url,
    "parser": parse_aljazzera_url,
    'color': '#FA9000'
}
if __name__ == '__main__':
    url = 'https://www.aljazeera.com/news/2020/03/climate-change-state-atmosphere-200311123221535.html'

    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")
    par = parse_aljazzera_url(url)
