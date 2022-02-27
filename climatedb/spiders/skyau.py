from climatedb.databases_neu import get_urls_for_paper, JSONLines, save_html, Article
from climatedb.utils import form_article_id
from climatedb.spiders.base import ClimateDBSpider
from climatedb.parsing_utils import get_body


class SkyAUSpider(ClimateDBSpider):
    name = "skyau"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):
        article_name = form_article_id(response.url, -1)
        body = get_body(response)
        body = body.split("Read More")[0]

        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        subtitle = response.xpath('//meta[@property="og:description"]/@content').get()
        subtitle = subtitle.split("Image:")[0]
        date = response.xpath('//meta[@name="article:publicationdate"]/@content').get()

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
