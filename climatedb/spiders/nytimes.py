import datetime
import re
from pathlib import Path

import scrapy
from scrapy.http.response.html import HtmlResponse

from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem


class NYTimesSpider(scrapy.Spider):
    name = "nytimes"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        body = response.xpath("//p/text()").getall()

        neu_body = []
        unwanted = set(["Advertisement", "Supported by"])
        for b in body:
            if b not in unwanted:
                neu_body.append(b)

        body = "".join(neu_body[1:])

        headline = response.xpath("//h1/text()").get()
        headline = headline.replace(" - The New York Times", "")

        date_published = response.xpath("//time/@datetime")
        date_published = datetime.datetime.fromisoformat(date_published.get())

        article_name = create_article_name(response.url)

        return ArticleItem(
            body=body,
            html=response.text,
            headline=headline,
            date_published=date_published.date(),
            article_url=response.url,
            article_name=article_name,
            article_start_url=find_start_url(response),
        )
