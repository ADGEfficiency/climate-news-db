import json
import re
import unicodedata
from datetime import datetime

from scrapy.http.response.html import HtmlResponse


def get_body(response: HtmlResponse) -> str:
    body = response.xpath("//p/descendant-or-self::*/text()").getall()
    body = " ".join(body)
    return clean_body(body)


def clean_body(body: str) -> str:
    body = body.replace("  ", " ")
    body = body.strip(" ")
    body = re.sub(r"\s+", " ", body).strip()
    body = unicodedata.normalize("NFKD", body).encode("ASCII", "ignore").decode()
    return body


def get_ld_json(response: HtmlResponse) -> dict:
    ld_json = response.xpath('//script[@type="application/ld+json"]/text()')
    return json.loads(ld_json.get())
