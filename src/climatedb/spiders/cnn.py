import datetime

from scrapy.http.response.html import HtmlResponse

from climatedb import parse
from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.spiders.base import BaseSpider


class CNNSpider(BaseSpider):
    name = "cnn"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url https://www.cnn.com/2021/10/14/weather/california-wildfires-thursday/index.html
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        ld_json = parse.get_ld_json(response)
        headline = ld_json["headline"]

        body = response.xpath(
            '//*[contains(@class, "paragraph")]/descendant-or-self::*/text()'
        ).getall()

        for unwanted in [
            "The opinions expressed in this commentary are",
            "(CNN)",
            "contributed to this report",
        ]:
            body = [b for b in body if unwanted not in b]
        body = "".join(body)
        body = parse.clean_body(body)

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
            article_name=create_article_name(response.url, -2),
            article_start_url=find_start_url(response),
        )
