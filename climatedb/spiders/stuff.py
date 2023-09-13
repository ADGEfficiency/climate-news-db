import datetime
import re

from scrapy.http.response.html import HtmlResponse

from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.parse import PUBLISHED_FORMAT, clean_body, get_body, get_ld_json
from climatedb.spiders.base import BaseSpider


class StuffSpider(BaseSpider):
    name = "stuff"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url https://www.stuff.co.nz/environment/climate-news/300413080/why-the-uk-is-leading-the-world-in-climate-action
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        body = get_body(response)
        body = re.sub(r"\d{4} Stuff Limited", "", body)
        body = clean_body(body)

        try:
            date_published = get_ld_json(response)["datePublished"]
            date_published = datetime.datetime.strptime(
                date_published, PUBLISHED_FORMAT
            )
        #  TODO be specific
        except Exception:
            date_published = response.xpath(
                '//meta[@property="article:published_time"]/@content'
            ).get()
            assert date_published
            date_published = datetime.datetime.strptime(
                date_published, "%Y-%m-%dT%H:%M:%S.%fZ"
            )

        return ArticleItem(
            body=body,
            html=response.text,
            headline=response.xpath('//meta[@property="og:title"]/@content').get(),
            date_published=date_published,
            article_url=response.url,
            article_name=create_article_name(response.url),
            article_start_url=find_start_url(response),
        )
