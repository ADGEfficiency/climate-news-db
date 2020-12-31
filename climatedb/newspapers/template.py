import re


def check_url(url):
    if url[-4:] == ".pdf":
        return False
    if "video.cfm" in url:
        return False
    #  should check for the Sorry, seems like this page doesn't exist.
    if url == "https://www.nzherald.co.nz/climate-change/news/article.cfm?c_id=26&objectid=19970":
        return False
    return url


def get_article_id(url):
    if "article.cfm" in url:
        #  always the last integer
        reg = re.compile(r"\d+")
        return str(reg.findall(url)[-1])
    else:
        return url.strip('/').split('/')[-1]


from climatedb import utils
def parse_url(url):



    return {
        **newspaper_values,
        "body": body,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": get_article_id(url)
        "date_published": published,
        "date_modified": updated,
    }


newspaper_values = {
    "newspaper_id": "nzherald",
    "newspaper": "The New Zealand Herald",
    "newspaper_url": "nzherald.co.nz",
}


newspaper = {
    **newspaper_values,
    "checker": check_url,
    "parser": parse_url,
    "get_article_id": get_article_id,
    "color": "#052962"
}
