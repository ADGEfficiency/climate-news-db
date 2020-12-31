import re

from climatedb import utils


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
    response = utils.request(url)
    soup = response['soup']
    html = response['html']

    try:
        body = utils.find_one_tag(soup, 'div', {'id': 'article-body'})
    except utils.ParserError as error:
        body = utils.find_one_tag(soup, 'section', {"class": "article__main"})

    body = "".join([p.text for p in body.findAll("p")])

    app = utils.find_single_application_json(soup)

    if 'headline' not in app.keys():
        raise utils.ParserError(f'{url}, headline not in application json')
    headline = app['headline']
    published = app['datePublished']

    return {
        **nzherald,
        "body": body,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": get_article_id(url),
        "date_published": published,
    }

nzherald = {
    "newspaper_id": "nzherald",
    "newspaper": "The New Zealand Herald",
    "newspaper_url": "nzherald.co.nz",
    "checker": check_url,
    "parser": parse_url,
    "get_article_id": get_article_id,
    "color": "#052962"
}
