from datetime import datetime
import json

from bs4 import BeautifulSoup
import requests


def check_sky_au_url(url, logger=None):
    if "https://2600.skynews.com.au" in url:
        return False
    if "skynews.com.au/page/" in url:
        return False
    if url == "https://www.skynews.com.au/":
        return False
    return True


def parse_sky_au_url(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")
    try:
        body = soup.findAll('p', attrs={"class": "description-text"})
        assert len(body) == 1
        body = body[0].text
    except AssertionError:
        body = soup.findAll('div', attrs={"class": "article-text row"})
        assert len(body) == 1
        body = "".join(p.text for p in body[0].findAll('p'))

    from json.decoder import JSONDecodeError
    scripts = soup.findAll('script')
    for script in scripts:
        if script.string:
            if 'publishedDate' in script.string:
                #  get_text() & .text not working
                data = script.string
                data = data.replace('window.__INITIAL_STATE__ = ', '')
                data = data.replace('\n', '')
                data = data.replace(';', '')
                data = data.split('window.__ENV__ =')[0]
                data = json.loads(data)
                data = data['items']
                key = list(data.keys())[0]
                pub = int(data[key]['content']['attributes']['publishedDate'])
                pub = datetime.fromtimestamp(pub/1000).isoformat()

            else:
                pub = datetime.fromtimestamp(0).isoformat()

    headline = soup.findAll('title')
    assert len(headline) == 1
    headline = headline[0].getText()
    headline = headline.split('|')[0]

    return {
        'newspaper_id': 'skyau',
        'body': body,
        'html': html,
        'headline': headline,
        'article_url': url,
        'article_id': url.split('/')[-1],
        'date_published': pub
    }


if __name__ == '__main__':
    url = 'https://www.skynews.com.au/details/_6173853418001'
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")
    par = parse_sky_au_url(url)
