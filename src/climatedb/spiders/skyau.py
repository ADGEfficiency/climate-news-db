import datetime

from scrapy.http.response.html import HtmlResponse

from climatedb import parse
from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.spiders.base import BaseSpider


class SkyAUSpider(BaseSpider):
    name = "skyau"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url https://www.skynews.com.au/details/_6216840001
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        ld_json = parse.get_ld_json(response)

        headline = ld_json["name"]
        headline = parse.clean_headline(headline)

        body = parse.get_body(response)

        date_published = ld_json["datePublished"]
        date_published = datetime.datetime.strptime(
            date_published, "%Y-%m-%dT%H:%M:%S.%fZ"
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
