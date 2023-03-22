import datetime
import re

from scrapy.http.response.html import HtmlResponse

from climatedb.crawl import find_start_url
from climatedb.models import ArticleItem
from climatedb.parse import get_body
from climatedb.spiders.base import BaseSpider


class WashingtonPostSpider(BaseSpider):
    name = "washington_post"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        article_name = response.url.split("/")[-2]
        body = get_body(response)

        patterns = [
            r"Sign in",
            r"This article was published more than\s*\d+\s*years\s+ago",
            r"Want smart analysis of the most important news in your inbox every weekday, along with other global reads, interesting ideas and opinions to know\? Sign up for the Todays WorldView newsletter",
            r"For the latest news, sign up for our free newsletter",
        ]
        for pattern in patterns:
            body = re.sub(pattern, "", body)

        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        headline = headline.split("|")[-1]

        date_published = response.xpath(
            '//meta[@property="article:published_time"]/@content'
        ).get()
        date_published = datetime.datetime.strptime(
            date_published, "%Y-%m-%dT%H:%M:%S.%fZ"
        )

        return ArticleItem(
            body=body,
            html=response.text,
            headline=headline,
            date_published=date_published,
            article_url=response.url,
            article_name=article_name,
            article_start_url=find_start_url(response),
        )
