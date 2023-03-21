import datetime
import re
from typing import List

from scrapy.http.response.html import HtmlResponse

from climatedb.crawl import find_start_url
from climatedb.models import ArticleItem
from climatedb.parse import get_body
from climatedb.spiders.base import BaseSpider


class WashingtonPostSpider(BaseSpider):
    name = "washington_post"

    def parse_article(self, response: HtmlResponse) -> ArticleItem:
        """
        @url
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        article_name = response.url.split("/")[-2]
        body = get_body()

        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        headline = headline.split("|")[-1]

        date_published = response.xpath(
            '//meta[@property="article:published_time"]/@content'
        ).get()
        date_published = datetime.datetime.fromisoformat(date_published).date()

        return ArticleItem(
            body=body,
            html=response.text,
            headline=headline,
            date_published=date_published,
            article_url=response.url,
            article_name=article_name,
            article_start_url=find_start_url(response),
        )
