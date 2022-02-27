import json
import scrapy
from climatedb.databases_neu import get_urls_for_paper, JSONLines, save_html
from pathlib import Path

from climatedb.parsing_utils import get_app_json, get_body
from climatedb.databases_neu import Article
from climatedb.utils import form_article_id


class AljazeeraSpider(scrapy.Spider):
    name = "aljazeera"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):
        article_name = form_article_id(response.url, -1)

        body = get_body(response)
        body = body.replace("Follow Al Jazeera English:", "")

        subtitle = response.xpath("//p/em//text()").get()

        try:
            app_json = get_app_json(response)
            date = app_json["datePublished"]
            headline = app_json["headline"]
        except TypeError:
            #  maybe always do this ??? idk
            headline = response.xpath('//meta[@property="og:title"]/@content').get()
            date = response.xpath('//span[@class="date"]/text()').get()
            from datetime import datetime

            # <span class="date">September 6, 2013</span>
            date = datetime.strptime(date, "%B %d, %Y")
            date = date.isoformat()

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
