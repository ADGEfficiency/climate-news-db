import datetime

import scrapy

from climatedb.crawl import find_start_url
from climatedb.models import ArticleItem
from climatedb.spiders.base import BaseSpider


class DailyNationSpider(BaseSpider):
    name = "daily_nation"

    def parse(self, response: scrapy.http.Response) -> ArticleItem:
        body = response.xpath(
            '//div[contains(@class, "paragraph-wrapper") and not(.//em)]'
        )
        body = " ".join(
            [paragraph.xpath("normalize-space(p//text())").get() for paragraph in body]
        )
        article_name = response.url.split("/")[-1].split(".")[0]
        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        date = response.xpath(
            '//meta[@property="og:article:published_time"]/@content'
        ).get()
        date = date.replace("Z", "+00:00")
        date = datetime.datetime.fromisoformat(date)

        return ArticleItem(
            body=body.strip(),
            html=response.text,
            headline=headline,
            date_published=date.date(),
            article_url=response.url,
            article_name=article_name,
            article_start_url=find_start_url(response),
        )
