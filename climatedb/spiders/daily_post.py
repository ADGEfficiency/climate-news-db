import datetime
import re

import scrapy
from scrapy.http.response.html import HtmlResponse

from climatedb import parse
from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.spiders.base import BaseSpider


class DailyPostSpider(BaseSpider):
    name = "daily_post"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url https://www.dailypost.co.uk/news/north-wales-news/anglesey-wind-farm-plans-could-19906408
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        ld_json = parse.get_ld_json(response)[0]

        body = ld_json["articleBody"]
        body = parse.clean_body(body)

        headline = ld_json["headline"]
        date_published = ld_json["datePublished"]
        date_published = datetime.datetime.strptime(
            date_published, "%Y-%m-%dT%H:%M:%S%z"
        )

        return ArticleItem(
            body=body,
            html=response.text,
            headline=headline,
            date_published=date_published,
            article_url=response.url,
            article_name=create_article_name(response.url),
            article_start_url=find_start_url(response),
        )
