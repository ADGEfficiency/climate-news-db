import datetime

from scrapy.http.response.html import HtmlResponse

from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.parse import get_body, get_ld_json
from climatedb.spiders.base import BaseSpider


class YomiuriSpider(BaseSpider):
    name = "yomiuri"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url https://japannews.yomiuri.co.jp/science-nature/climate-change/20230315-97397/
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        body = get_body(response)
        unwanted = [
            "Please disable the ad blocking feature. To use this site, please disable the ad blocking feature and reload the page. This website uses cookies to collect information about your visit for purposes such as showing you personalized ads and content, and analyzing our website traffic. By clicking Accept all, you will allow the use of these cookies. Users accessing this site from EEA countries and UK are unable to view this site without your consent. We apologize for any inconvenience caused.",
            "JN ACCESS RANKING The Japan News / Weekly Edition Our weekly ePaper presents the most noteworthy recent topics in an exciting, readable fomat. Read more 2023 The Japan News - by The Yomiuri Shimbun",
        ]
        body = body.replace(unwanted, "")
        date_published = datetime.datetime.fromisoformat(
            response.xpath("//meta[@property='article:published_time']/@content").get(),
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
