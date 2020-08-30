from datetime import datetime

from bs4 import BeautifulSoup
import requests

from climatedb.newspapers.utils import find_one_tag, form_article_id



def check_dw_metadata(url):
    soup = BeautifulSoup(requests.get(url).text, features="html5lib")
    col = soup.findAll('div', {'class': 'col1 dim'})[0]
    lis = col.findAll('li')

    for li in lis:
        st = li.findAll('strong')
        if st:
            if st[0].text == 'Duration':
                return False
            if st[0].text == 'Number of pictures':
                return False
    return True


def check_dw_url(url, logger=None):
    if "/top-stories/" in url:
        return False
    if url == "https://www.dw.com/en/climate-change-are-we-trapped-in-a-vicious-circle/g-51944184":
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
    return True


def parse_dw_url(url, logger=None):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")

    #  hope it's going to be the first one :)
    body = soup.findAll("div", {"class": "longText"})[0]
    body = body.findAll("p")
    body = "".join(p.text for p in body)

    headline = find_one_tag(soup, 'title', {"id": None}).text.split('|')[0].strip(' ')
    #  description is there as meta

    #  hoping the right table is first
    date = soup.findAll('div', {'class': 'col1 dim'})[0].findAll('li')

    for li in date:
        st = li.findAll('strong')
        if st[0].text == 'Date':
            date = li.text
            break

    date = date.split('\n')[1]
    date = datetime.strptime(date, '%d.%m.%Y').isoformat()

    return {
        "newspaper_id": "dw",
        "body": body,
        "article_id": form_article_id(url, idx=-2),
        "headline": headline,
        "article_url": url,
        "html": html,
        "date_published": date
    }


dw = {
    "newspaper_id": "dw",
    "newspaper": "Deutsche Welle",
    "newspaper_url": "dw.com/en",
    "checker": check_dw_url,
    "parser": parse_dw_url,
    "color": "#0098FF"
}


if __name__ == "__main__":
    url = 'https://www.dw.com/en/2019-the-year-of-climate-consciousness-wildfires-fridays-for-future-climate-emergency-a-51719968/a-51719968'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")
    out = parse_dw_url(url)
