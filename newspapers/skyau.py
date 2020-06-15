from bs4 import BeautifulSoup
import requests


def check_sky_au_url(url, logger=None):
    return True


def parse_sky_au_url(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")
    article = ''.join([p.text for p in soup.findAll('p', attrs={"class": "description-text"})])

    date = soup.findAll('span', attrs={'class': 'metadata-date'})[0].text
    return {
        'newspaper': 'skyau',
        'body': article,
        'html': html,
        'url': url,
        'id': url.split('/')[-1],
        'published': date
    }
