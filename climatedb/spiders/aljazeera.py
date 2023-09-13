import datetime

from scrapy.http.response.html import HtmlResponse

from climatedb import parse
from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.spiders.base import BaseSpider


class AljazeeraSpider(BaseSpider):
    name = "aljazeera"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url https://www.aljazeera.com/news/2021/10/4/ukraine-accuses-russia-of-escalating-conflict-in-east
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        body = parse.get_body(response)
        body = body.replace("Follow Al Jazeera English:", "")

        try:
            ld_json = parse.get_ld_json(response)
            headline = ld_json["headline"]
            date_published = datetime.datetime.strptime(
                ld_json["datePublished"], "%Y-%m-%dT%H:%M:%SZ"
            )

        except Exception:
            headline = response.xpath('//meta[@property="og:title"]/@content').get()
            date = response.xpath('//span[@class="date"]/text()').get()
            time = response.xpath('//span[@class="time"]/text()').get()
            dt = date + " " + time
            dt = dt.replace(" ET", "")
            date_published = datetime.datetime.strptime(dt, "%B %d, %Y %I:%M%p")

        return ArticleItem(
            body=body,
            html=response.text,
            headline=headline,
            date_published=date_published,
            article_url=response.url,
            article_name=create_article_name(response.url, -1),
            article_start_url=find_start_url(response),
        )
