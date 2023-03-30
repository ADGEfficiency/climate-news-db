import datetime

from scrapy.http.response.html import HtmlResponse

from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.parse import get_body, get_ld_json
from climatedb.spiders.base import BaseSpider


class YomiuriSpider(BaseSpider):
    name = "yomiuri"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url https://japannews.yomiuri.co.jp/science-nature/climate-change/20230315-97397/
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        body = get_body(response)
        date_published = datetime.datetime.fromisoformat(
            response.xpath("//meta[@property='article:published_time']/@content").get(),
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
