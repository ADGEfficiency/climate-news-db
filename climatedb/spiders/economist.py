from climatedb.databases_neu import get_urls_for_paper, save_html, Article
from climatedb.parsing_utils import get_body
from climatedb.spiders.base import ClimateDBSpider
from climatedb.utils import form_article_id


class EconomistSpider(ClimateDBSpider):
    name = "economist"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):
        article_name = form_article_id(response.url, -1)
        body = get_body(response)

        unwanted = [
            "For more coverage of climate change, register for The Climate Issue, our fortnightly newsletter, or visit our climate-change hub",
            'Sign up to our new fortnightly climate-change newsletter hereThis article appeared in the Leaders section of the print edition under the headline "The climate issue"',
        ]
        for unw in unwanted:
            body = body.replace(unw, "")

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
        return meta
