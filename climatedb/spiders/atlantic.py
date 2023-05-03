import datetime

from scrapy.http.response.html import HtmlResponse

from climatedb import parse
from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.spiders.base import BaseSpider


class AtlanticSpider(BaseSpider):
    name = "atlantic"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url https://www.theatlantic.com/science/archive/2021/09/climate-change-hurricane-ida/620882/
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        ld_json = parse.get_ld_json(response, 2)
        body = parse.get_body(response)
        headline = parse.clean_headline(ld_json["headline"])
        date_published = ld_json["datePublished"]
        date_published = datetime.datetime.strptime(
            date_published, "%Y-%m-%dT%H:%M:%SZ"
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
