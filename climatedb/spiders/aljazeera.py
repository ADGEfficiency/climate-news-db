import scrapy
from climatedb.databases_neu import get_urls_for_paper, JSONLines
from pathlib import Path

from climatedb.parsing_utils import get_title, get_date
from climatedb.types import ArticleModel


class AljazeeraSpider(scrapy.Spider):
    name = "aljazeera"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):
        article_name = response.url.strip("/").split("/")[-1]

        #  TODO
        unwanted = set(["Follow Al Jazeera English:"])
        body = response.xpath("//p/text()").getall()
        body = "".join(body)

        title = get_title(response)
        breakpoint()
        #   prob need to use application json hdere!
        date = get_date(response)
