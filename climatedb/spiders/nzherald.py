from climatedb import parsing_utils
from climatedb.databases import Article, get_urls_for_paper, save_html
from climatedb.parsing_utils import get_body
from climatedb.spiders.base import ClimateDBSpider


class NZHeraldSpider(ClimateDBSpider):
    name = "nzherald"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):
        article_name = parsing_utils.form_article_id(response.url, -1)
        body = get_body(response)

        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        subtitle = response.xpath('//meta[@property="og:description"]/@content').get()

        app_json = parsing_utils.get_app_json(response, n=0)
        date = app_json["datePublished"]

        meta = {
            "headline": headline,
            "subtitle": subtitle,
            "body": body,
            "article_url": response.url,
            "date_published": date,
            "article_name": article_name,
        }
        return self.tail(response, meta)
