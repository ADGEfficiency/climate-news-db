import re
import json
from json.decoder import JSONDecodeError


from bs4 import BeautifulSoup
import requests


def get_nzherald_article_id(url):
    #  always the last integer
    reg = re.compile(r"\d+")
    return str(reg.findall(url)[-1])


def check_nzherald_url(url, logger=None):
    if url[-4:] == ".pdf":
        return False
    if "video.cfm" in url:
        return False
    #  should check for the Sorry, seems like this page doesn't exist.
    if url == "https://www.nzherald.co.nz/climate-change/news/article.cfm?c_id=26&objectid=19970":
        return False
    return True


def parse_nzherald_url(url):
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, features="html5lib")

    try:
        table = soup.findAll("div", attrs={"id": "article-body"})
        article = "".join([p.text for p in table[0].findAll("p")])

        ld = soup.findAll("script", attrs={"type": "application/ld+json"})
        ld = ld[0].getText()
        ld = ld.replace("\n", "")
    except IndexError as e:
        return {"error": repr(e)}

    try:
        ld = json.loads(ld)
    except JSONDecodeError as e:
        print("decode error")
        return {"error": repr(e)}

    return {
        "newspaper_id": "nzherald",
        "body": article,
        "headline": ld["headline"],
        "article_url": url,
        "article_id": get_nzherald_article_id(url),
        "html": html,
        "date_published": ld["datePublished"],
        "date_modified": ld["dateModified"],
    }


nzherald = {
    "newspaper_id": "nzherald",
    "newspaper": "The New Zealand Herald",
    "newspaper_url": "nzherald.co.nz",
    "checker": check_nzherald_url,
    "parser": parse_nzherald_url,
}


if __name__ == "__main__":

    urls = (
        "https://www.nzherald.co.nz/nz/news/article.cfm?c_id=1&objectid=12270976",
        "https://www.nzherald.co.nz/nz/news/article.cfm?c_id=1&objectid=199698",
    )

    print(urls)
    url = urls[0]


"""
<html class="articlestory"><head> <script type="application/ld+json">

"""
