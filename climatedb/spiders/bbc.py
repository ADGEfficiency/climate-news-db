import datetime

from scrapy.http.response.html import HtmlResponse

from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.parse import get_ld_json
from climatedb.spiders.base import BaseSpider


class BBCSpider(BaseSpider):
    name = "bbc"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url https://www.bbc.com/news/science-environment-58640453
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        article_name = create_article_name(response.url)

        body = response.xpath(
            '//div[@itemprop="articleBody"]/descendant-or-self::*/text()'
        ).getall()
        body = "".join(body)

        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        date = get_ld_json(response)["datePublished"]
        date_published = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

        return ArticleItem(
            body=body,
            html=response.text,
            headline=headline,
            date_published=date_published,
            article_url=response.url,
            article_name=article_name,
            article_start_url=find_start_url(response),
        )
