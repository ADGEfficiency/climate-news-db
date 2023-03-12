from climatedb import Article, get_urls_for_paper
from climatedb.parsing_utils import form_article_id, get_app_json
from climatedb.spiders.base import ClimateDBSpider


class NYTimesSpider(ClimateDBSpider):
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
        return self.tail(response, meta)
