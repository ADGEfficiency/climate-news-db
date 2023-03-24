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
    return body


def get_ld_json(response: HtmlResponse) -> dict:
    ld_json = response.xpath('//script[@type="application/ld+json"]/text()')
    return json.loads(ld_json.get())
