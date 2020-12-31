from datetime import datetime
import re

from bs4 import BeautifulSoup
import requests

from climatedb import utils


def check_dw_metadata(url):
    """
    Can't figure out if the url is for an article, video or pictures

    This solution involves parsing the HTML, which is slow

    A faster soln may be to
    """
    soup = BeautifulSoup(requests.get(url).text, features="html5lib")
    col = soup.findAll('div', {'class': 'col1 dim'})
    if col:
        lis = col[0].findAll('li')

        for li in lis:
            st = li.findAll('strong')
            if st:
                if st[0].text == 'Duration':
                    return False
                if st[0].text == 'Number of pictures':
                    return False
                if st[0].text == 'Life Links container':
                    return False
        return url
    else:
        return False


def check_url(url):
    if "/top-stories/" in url:
        return False
    if url == "https://www.dw.com/en/climate-change-are-we-trapped-in-a-vicious-circle/g-51944184":
        return False
    if url == "https://www.dw.com/en/nature/t-19027552":
        return False
    if url == "https://www.dw.com/en/antarctic/t-38775585":
        return False
    if 'https://www.dw.com/en/environment/t-18971817' in url:
        return False
    if 'https://www.dw.com/en/nature/t-1902755' in url:
        return False
    if 'https://www.dw.com/en/biodiversity/t-17359056' in url:
        return False
    if not check_dw_metadata(url):
        return False
    if url == "https://www.dw.com/en/climate-change/t-18614374":
        return False
    return url


def get_article_id(url):
    return utils.form_article_id(url, -2)


def parse_url(url):
    response = utils.request(url)
    soup = response['soup']
    html = response['html']

    #  hope it's going to be the first one :)
    body = soup.findAll("div", {"class": "longText"})[0]
    body = "".join([p.text for p in body.findAll("p", recursive=False) if not p.attrs])

    headline = utils.find_one_tag(soup, 'title', {"id": None}).text.split('|')[0].strip(' ')

    date = soup.findAll('div', {'class': 'col1 dim'})[0].findAll('li')
    for li in date:
        st = li.findAll('strong')
        if st[0].text == 'Date':
            date = li.text
            break

    date = date.split('\n')[1]
    published = datetime.strptime(date, '%d.%m.%Y').isoformat()

    return {
        **dw,
        "body": body,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": get_article_id(url),
        "date_published": published,
    }


dw = {
    "newspaper_id": "dw",
    "newspaper": "Deutsche Welle",
    "newspaper_url": "dw.com/en",

    "checker": check_url,
    "parser": parse_url,
    "get_article_id": get_article_id,
    "color": "#0098FF"
}
