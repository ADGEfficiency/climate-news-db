import json
import scrapy
from climatedb.databases_neu import get_urls_for_paper, JSONLines, save_html
from pathlib import Path

from climatedb.parsing_utils import get_app_json, get_body
from climatedb.databases_neu import Article


class AljazeeraSpider(scrapy.Spider):
    name = "aljazeera"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):
        article_name = response.url.strip("/").split("/")[-1]

        body = get_body(response)
        body = body.replace("Follow Al Jazeera English:", "")

        subtitle = response.xpath("//p/em//text()").get()

        app_json = get_app_json(response)
        date = app_json["datePublished"]
        headline = app_json["headline"]

        #  one jsonline - saved by scrapy for us
        meta = {
            "headline": headline,
            "subtitle": subtitle,
            "body": body,
            "article_url": response.url,
            "date_published": date,
            "article_name": article_name,
        }
        meta = Article(**meta).dict()
        save_html(self.name, article_name, response)
        return meta
