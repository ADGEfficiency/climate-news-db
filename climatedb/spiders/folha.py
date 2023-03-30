import datetime

from scrapy.http.response.html import HtmlResponse

from climatedb import parse
from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.spiders.base import BaseSpider


class FolhaSpider(BaseSpider):
    name = "folha"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url https://www1.folha.uol.com.br/internacional/en/business/2021/01/tax-crisis-and-conflict-between-cutting-down-and-spending-are-challenges-in-2021.shtml
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        date_published = datetime.datetime.strptime(
            response.xpath("//time/@datetime").get(), "%Y-%m-%d %H:%M:%S"
        )
        headline = response.xpath("//title/text()").get()
        if "Folha de S.Paulo - Internacional - En" in headline:
            raise ValueError("not an article")

        headline = headline.split("-")[0]
        headline = headline.strip(" ")
        assert headline is not None

        body = response.xpath('//div[@class="c-news__body"]/p/text()')
        body = " ".join(body.getall())
        body = parse.clean_body(body)

        return ArticleItem(
            body=body,
            html=response.text,
            headline=headline,
            date_published=date_published,
            article_url=response.url,
            article_name=create_article_name(response.url, -1),
            article_start_url=find_start_url(response),
        )
