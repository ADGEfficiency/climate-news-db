import pytz
from datetime import datetime
import json


def get_title(response) -> str:
    return response.css("title::text").get()


def get_date(response) -> datetime:
    date = response.xpath('//meta[@property="article:published_time"]/@content').get()
    assert date[-1] == "Z"
    date = date.split(".")[0]
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    tz = pytz.timezone("UTC")
    date = tz.localize(date)
    return date


def get_app_json(response, n=0) -> dict:
    app_json = response.xpath("//script[@type='application/ld+json']/text()").getall()
    return json.loads(app_json[n])


def get_body(response):
    body = response.xpath("//p/descendant-or-self::*/text()").getall()
    return " ".join(body)


def form_article_id(url, idx=-1):
    url = url.strip("/")
    url = url.split("?")[0]
    article_id = url.split("/")[idx]
    return article_id.replace(".html", "")


def strip_embedded_json(body):

    return body
