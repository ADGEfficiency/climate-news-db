import datetime

from scrapy.http.response.html import HtmlResponse

from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.spiders.base import BaseSpider


class BATimesSpider(BaseSpider):
    name = "batimes"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url https://www.batimes.com.ar/news/environment/climate-change-is-here-and-now.phtml
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        body = response.xpath('//div[@id="news-body"]/p/text()')
        body = " ".join([p.get() for p in body])
        date_published = response.xpath(
            '//meta[@property="article:published_time"]/@content'
        ).get()
        date_published = datetime.datetime.strptime(
            date_published, "%Y-%m-%dT%H:%M:%S%z"
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
