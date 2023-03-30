import datetime

from scrapy.http.response.html import HtmlResponse

from climatedb import parse
from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.spiders.base import BaseSpider


class GuardianSpider(BaseSpider):
    name = "guardian"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url https://www.theguardian.com/environment/2021/sep/22/climate-crisis-uk-should-prepare-for-impact-of-7c-of-global-heating-says-cabinet-office
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        ld_json = parse.get_ld_json(response)[0]
        headline = ld_json["headline"]
        body = parse.get_body(response)
        date_published = datetime.datetime.strptime(
            ld_json["datePublished"], "%Y-%m-%dT%H:%M:%S.%fZ"
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
