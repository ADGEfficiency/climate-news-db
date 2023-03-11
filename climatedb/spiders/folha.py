from scrapy.http.response.html import HtmlResponse

from climatedb import get_urls_for_paper, parsing_utils
from climatedb.parsing_utils import clean_body, get_body
from climatedb.spiders.base import ClimateDBSpider


class FolhaSpider(ClimateDBSpider):
    name = "folha"
    start_urls = get_urls_for_paper(name)

    def parse(self, response: HtmlResponse) -> dict:
        article_name = parsing_utils.form_article_id(response.url, -1)

        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        subtitle = response.xpath('//meta[@property="og:description"]/@content').get()

        date = response.xpath(
            '//meta[@property="article:published_time"]/@content'
        ).get()
        body = get_body(response)

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
