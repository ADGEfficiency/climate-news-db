import datetime

from scrapy.http.response.html import HtmlResponse

from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.parse import get_body, get_ld_json
from climatedb.spiders.base import BaseSpider


class BBCSpider(BaseSpider):
    name = "bbc"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url https://www.bbc.com/news/science-environment-58640453
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        ld_json = get_ld_json(response)
        body = get_body(response)
        headline = response.xpath("//title/text()").get()
        headline = headline.replace(" - BBC News", "")
        date_published = datetime.datetime.strptime(
            ld_json["datePublished"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )

        body = body.replace(
            "The BBC is not responsible for the content of external sites. Read about our approach to external linking.",
            "",
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
