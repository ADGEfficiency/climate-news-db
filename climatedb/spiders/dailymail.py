from climatedb.databases_neu import get_urls_for_paper, save_html, Article
from climatedb.parsing_utils import get_body
from climatedb.spiders.base import ClimateDBSpider
from climatedb.utils import form_article_id


class DailyMailSpider(ClimateDBSpider):
    name = "dailymail"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):
        article_name = form_article_id(response.url, -1)
        body = get_body(response)

        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        subtitle = response.xpath('//meta[@property="og:description"]/@content').get()
        date = response.xpath('//meta[@itemprop="datePublished"]/@content').get()

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
