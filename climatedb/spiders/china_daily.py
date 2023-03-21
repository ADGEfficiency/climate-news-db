import datetime
import re

import scrapy
from scrapy.http.response.html import HtmlResponse

from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.spiders.base import BaseSpider


class ChinaDailySpider(scrapy.Spider):
    name = "china_daily"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url https://www.chinadaily.com.cn/a/202301/19/WS63c8a4a8a31057c47ebaa8e4.html
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        #  article body
        body = response.xpath('//div[@id="Content"]/p[not(@class="email")]/text()')
        body = " ".join(body.getall())

        #  replace one or more whitespace characters with single space - removes '\xa0'
        body = re.sub(r"\s+", " ", body)

        #  strip whitespace
        body = body.strip("")

        return ArticleItem(
            body=body,
            html=response.text,
            headline=response.xpath('//meta[@property="og:title"]/@content').get(),
            date_published=datetime.date.fromisoformat(
                response.xpath('//meta[@name="publishdate"]/@content').get()
            ),
            article_url=response.url,
            article_name=create_article_name(response.url),
            article_start_url=find_start_url(response),
        )
