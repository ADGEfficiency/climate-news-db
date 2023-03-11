import unicodedata
from datetime import datetime

from scrapy.http.response.html import HtmlResponse

from climatedb import parsing_utils
from climatedb import Article, get_urls_for_paper
from climatedb.parsing_utils import get_body
from climatedb.spiders.base import ClimateDBSpider


class DailyPostSpider(ClimateDBSpider):
    name = "daily_post"
    start_urls = get_urls_for_paper(name)

    def parse(self, response: HtmlResponse) -> dict:
        article_name = parsing_utils.form_article_id(response.url, -1)

        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        subtitle = response.xpath('//meta[@property="og:description"]/@content').get()

        date = response.xpath(
            '//meta[@property="article:published_time"]/@content'
        ).get()
        date = datetime.fromisoformat(date)

        """
        find all p tags below
        <div id="mvp-content-main" class="left relative">
        """
        div = response.xpath('//div[@id="mvp-content-main"]')
        p_tags = div.xpath(".//p/text()").getall()
        body = " ".join(p_tags)

        body = unicodedata.normalize("NFKD", body).encode("ASCII", "ignore").decode()

        meta = {
            "headline": headline,
            "subtitle": subtitle,
            "body": body,
            "article_url": response.url,
            "date_published": date,
            "article_name": article_name,
        }
        return self.tail(response, meta)
