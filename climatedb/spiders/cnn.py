from climatedb.databases_neu import get_urls_for_paper, JSONLines, save_html, Article
from climatedb.utils import form_article_id
from climatedb.spiders.base import ClimateDBSpider


class CNNSpider(ClimateDBSpider):
    name = "cnn"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):

        article_name = form_article_id(response.url, -2)
        body = response.xpath(
            '//div[@itemprop="articleBody"]/descendant-or-self::*/text()'
        ).getall()

        for unwanted in [
            "The opinions expressed in this commentary are",
            "(CNN)",
            "contributed to this report",
        ]:
            body = [b for b in body if unwanted not in b]
        body = "".join(body)

        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        subtitle = response.xpath('//meta[@property="og:description"]/@content').get()
        date = response.xpath('//meta[@name="pubdate"]/@content').get()

        meta = {
            "headline": headline,
            "subtitle": subtitle,
            "body": body,
            "article_url": response.url,
            "date_published": date,
            "article_name": article_name,
        }
        return self.tail(response, meta)
