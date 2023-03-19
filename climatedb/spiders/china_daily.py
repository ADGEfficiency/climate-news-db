import datetime
import pathlib
import re

import scrapy
from scrapy.http.response.html import HtmlResponse

from climatedb.crawl import (create_article_name, find_start_url,
                             find_urls_to_crawl)
from climatedb.models import ArticleItem


class ChinaDailySpider(scrapy.Spider):
    name = "china_daily"

    def start_requests(self) -> scrapy.Request:
        data_home = pathlib.Path(self.settings["DATA_HOME"])
        urls = find_urls_to_crawl(self.name, data_home=data_home)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url https://www.chinadaily.com.cn/a/202301/19/WS63c8a4a8a31057c47ebaa8e4.html
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        date_published = datetime.date.fromisoformat(
            response.xpath('//meta[@name="publishdate"]/@content').get()
        )

        body = response.xpath('//div[@id="Content"]/p[not(@class="email")]/text()')
        body = " ".join(body.getall())

        #  replace one or more whitespace characters with single space - removes '\xa0'
        body = re.sub(r"\s+", " ", body)

        #  remove whitespace from start and end
        body = body.strip(" ")

        return ArticleItem(
            headline=response.xpath('//meta[@property="og:title"]/@content').get(),
            date_published=date_published,
            body=body,
            article_name=create_article_name(response.url),
            article_url=response.url,
            article_start_url=find_start_url(response),
            html=response.text,
        )
