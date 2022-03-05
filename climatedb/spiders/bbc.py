from climatedb.databases_neu import get_urls_for_paper, JSONLines, save_html, Article
from climatedb.utils import form_article_id
from climatedb.spiders.base import ClimateDBSpider

from climatedb import parsing_utils


class BBCSpider(ClimateDBSpider):
    name = "bbc"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):

        article_name = form_article_id(response.url, -2)
        # body = response.xpath(
        #     '//div[@itemprop="articleBody"]/descendant-or-self::*/text()'
        # ).getall()
        # body = "".join(body)
        body = parsing_utils.get_body(response)

        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        subtitle = response.xpath('//meta[@property="og:description"]/@content').get()

        app = parsing_utils.get_app_json(response)
        date = app["datePublished"]

        meta = {
            "headline": headline,
            "subtitle": subtitle,
            "body": body,
            "article_url": response.url,
            "date_published": date,
            "article_name": article_name,
        }
        return self.tail(response, meta)
