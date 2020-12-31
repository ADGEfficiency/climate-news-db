from datetime import datetime
import json

from climatedb import utils


def check_url(url):
    if "https://2600.skynews.com.au" in url:
        return False
    if "skynews.com.au/page/" in url:
        return False
    if url == "https://www.skynews.com.au/":
        return False
    return True


def get_article_id(url):
    return utils.form_article_id(url, -1)


def parse_url(url):
    response = utils.request(url)
    soup = response['soup']
    html = response['html']

    try:
        body = utils.find_one_tag(soup, "p", {"class": "description-text"})
        body = body.text
    except utils.ParserError:
        body = utils.find_one_tag(soup, "p", {"class": "article-text row"})
        body = "".join([p.text for p in body.findAll("p")])

    scripts = soup.findAll("script")
    for script in scripts:
        if script.string:
            if "publishedDate" in script.string:
                #  get_text() & .text not working
                data = script.string
                data = data.replace("window.__INITIAL_STATE__ = ", "")
                data = data.replace("\n", "")
                data = data.replace(";", "")
                data = data.split("window.__ENV__ =")[0]
                data = json.loads(data)
                data = data["items"]
                key = list(data.keys())[0]
                published = int(data[key]["content"]["attributes"]["publishedDate"])
                published = datetime.fromtimestamp(published / 1000).isoformat()
                break

            else:
                published = datetime.fromtimestamp(0).isoformat()

    headline = utils.find_one_tag(soup, 'title').text
    headline = headline.split("|")[0]

    return {
        **skyau,
        "body": body,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": get_article_id(url),
        "date_published": published,
    }


skyau = {
    "newspaper_id": "skyau",
    "newspaper": "Sky News Australia",
    "newspaper_url": "skynews.com.au",

    "checker": check_url,
    "parser": parse_url,
    "get_article_id": get_article_id,
    "color": "#93A681"
}
