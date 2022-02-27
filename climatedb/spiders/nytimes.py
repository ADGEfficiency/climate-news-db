import scrapy

from climatedb.databases_neu import get_urls_for_paper, save_html, Article
from climatedb.parsing_utils import get_app_json

from climatedb.utils import form_article_id


class NYTimesSpider(scrapy.Spider):
    name = "nytimes"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):
        article_name = form_article_id(response.url, -1)

        body = response.xpath("//p/text()").getall()

        neu_body = []
        unwanted = set(["Advertisement", "Supported by"])
        for b in body:
            if b not in unwanted:
                neu_body.append(b)

        subtitle = neu_body[0]
        body = neu_body[1:]
        body = "".join(body)

        app_json = get_app_json(response)
        date = app_json["datePublished"]
        headline = app_json["headline"]
        headline = headline.replace(" - The New York Times", "")

        #  one jsonline - saved by scrapy for us
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