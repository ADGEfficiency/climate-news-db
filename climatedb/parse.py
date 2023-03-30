import json
import re
import unicodedata
from datetime import datetime

from scrapy.http.response.html import HtmlResponse

PUBLISHED_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def get_body(response: HtmlResponse) -> str:
    body = response.xpath("//p/descendant-or-self::*/text()").getall()
    body = " ".join(body)
    return clean_body(body)


def clean_body(body: str) -> str:
    body = body.replace("  ", " ")
    body = body.strip(" ")

    #  replace one or more whitespace characters with single space - removes '\xa0'
    body = re.sub(r"\s+", " ", body)
    body = unicodedata.normalize("NFKD", body).encode("ASCII", "ignore").decode()
    body = body.replace("&nbsp;", " ")
    body = body.replace("<em>", "")
    body = body.replace("</em>", "")
    body = body.strip(" ")
    return body


def clean_headline(headline: str) -> str:
    headline = headline.replace("&#8216;", "")
    headline = headline.replace("&#8217;", "")
    return headline


def get_ld_json(response: HtmlResponse, idx: int = 0) -> dict:
    ld_json = response.xpath('//script[@type="application/ld+json"]/text()')
    ld_json = ld_json.getall()[idx]

    assert ld_json is not None
    ld_json = ld_json.replace("\n", "")
    ld_json = ld_json.replace("\t", "")
    return json.loads(ld_json)
