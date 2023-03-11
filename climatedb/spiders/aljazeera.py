import json
from datetime import datetime
from pathlib import Path

from climatedb import parsing_utils
from climatedb import Article, get_urls_for_paper
from climatedb.parsing_utils import get_app_json, get_body
from climatedb.spiders.base import ClimateDBSpider


class AljazeeraSpider(ClimateDBSpider):
    name = "aljazeera"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):
        article_name = parsing_utils.form_article_id(response.url, -1)

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
        #  shouldnt need this!
        assert len(meta["article_name"]) > 4
        return self.tail(response, meta)
