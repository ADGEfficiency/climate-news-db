import datetime

from scrapy.http.response.html import HtmlResponse

from climatedb import parse
from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.spiders.base import BaseSpider


class NewsHubSpider(BaseSpider):
    name = "newshub"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url https://www.newshub.co.nz/home/new-zealand/2021/09/climate-change-activists-blockade-auckland-skytower.html
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        body = response.xpath("//article//p//text()").getall()

        noise = [
            "This article is republished from The Conversation under a Creative Commons license. Read the original article here. ",
        ]
        for n in noise:
            body = [b.replace(n, "") for b in body]
        body = " ".join(body)

        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        date_published = datetime.datetime.strptime(
            response.xpath('//meta[@itemprop="datePublished"]/@content')
            .get()
            .split("+")[0],
            "%Y-%m-%dT%H:%M:%S",
        )

        return ArticleItem(
            body=body,
            html=response.text,
            headline=headline,
            date_published=date_published,
            article_url=response.url,
            article_name=create_article_name(response.url, -1),
            article_start_url=find_start_url(response),
        )
