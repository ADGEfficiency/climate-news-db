from climatedb import parsing_utils
from climatedb.databases import Article, get_urls_for_paper, save_html
from climatedb.spiders.base import ClimateDBSpider


class AtlanticSpider(ClimateDBSpider):
    name = "atlantic"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):
        article_name = parsing_utils.form_article_id(response.url, -1)
        body = parsing_utils.get_body(response)

        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        subtitle = response.xpath('//meta[@property="og:description"]/@content').get()
        # date = response.xpath('//meta[@itemprop="datePublished"]/@content').get()

        app_json = parsing_utils.get_app_json(response, n=2)
        date = app_json["datePublished"]

        meta = {
            "headline": headline,
            "subtitle": subtitle,
            "body": body,
            "article_url": response.url,
            "date_published": date,
            "article_name": article_name,
        }
        meta = Article(**meta).dict()
        save_html(self.name, article_name, response)
        return self.tail(response, meta)
