import unicodedata

from climatedb import get_urls_for_paper
from climatedb.parsing_utils import form_article_id, get_body
from climatedb.spiders.base import ClimateDBSpider


class SkyAUSpider(ClimateDBSpider):
    name = "skyau"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):
        article_name = form_article_id(response.url, -1)
        body = get_body(response)
        body = body.split("Read More")[0]
        body = body.split("Image:")[0]

        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        headline = unicodedata.normalize("NFKD", headline)
        headline = headline.replace("&#8216;", "")
        headline = headline.replace("&#8217;", "")

        subtitle = response.xpath('//meta[@property="og:description"]/@content').get()
        subtitle = subtitle.split("Image:")[0]
        subtitle = unicodedata.normalize("NFKD", subtitle)

        date = response.xpath('//meta[@name="article:publicationdate"]/@content').get()

        meta = {
            "headline": headline,
            "subtitle": subtitle,
            "body": body,
            "article_url": response.url,
            "date_published": date,
            "article_name": article_name,
        }
        return self.tail(response, meta)
