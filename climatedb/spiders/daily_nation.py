from datetime import datetime

from scrapy.http.response.html import HtmlResponse

from climatedb import get_urls_for_paper, parsing_utils
from climatedb.parsing_utils import clean_body
from climatedb.spiders.base import ClimateDBSpider


class DailyNationSpider(ClimateDBSpider):
    name = "daily_nation"
    start_urls = get_urls_for_paper(name)

    def parse(self, response: HtmlResponse) -> dict:
        article_name = parsing_utils.form_article_id(response.url, -1)

        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        subtitle = response.xpath('//meta[@property="og:description"]/@content').get()

        date = response.xpath(
            '//meta[@property="og:article:published_time"]/@content'
        ).get()
        date = date.replace("Z", "+00:00")
        date = datetime.fromisoformat(date)

        body = response.xpath(
            '//div[contains(@class, "paragraph-wrapper") and not(.//em)]'
        )
        body = " ".join(
            [paragraph.xpath("normalize-space(p//text())").get() for paragraph in body]
        )
        body = clean_body(body)

        meta = {
            "headline": headline,
            "subtitle": subtitle,
            "body": body,
            "article_url": response.url,
            "date_published": date,
            "article_name": article_name,
        }
        return self.tail(response, meta)
