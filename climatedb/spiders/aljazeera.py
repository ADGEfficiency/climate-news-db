import json
import scrapy
from climatedb.databases_neu import get_urls_for_paper, JSONLines, save_html
from pathlib import Path

from climatedb.parsing_utils import get_title, get_date
from climatedb.databases_neu import Article


class AljazeeraSpider(scrapy.Spider):
    name = "aljazeera"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):
        article_name = response.url.strip("/").split("/")[-1]

        #  TODO
        unwanted = set(["Follow Al Jazeera English:"])
        body = response.xpath("//p/text()").getall()
        subtitle = response.xpath("//p/em//text()").get()

        app_json = response.xpath("//script[@type='application/ld+json']/text()").get()
        app_json = json.loads(app_json)
        date = app_json["datePublished"]
        headline = app_json["headline"]

        #  one jsonline - saved by scrapy for us
        meta = {
            "headline": headline,
            "subtitle": subtitle,
            "body": body,
            "article_url": response.url,
            "article_id": article_name,
            "date_published": date,
        }
        meta = Article(**meta).dict()
        save_html(self.name, article_name, response)
        return meta
