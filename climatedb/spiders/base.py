import pathlib

import scrapy

from climatedb.crawl import find_urls_to_crawl


class BaseSpider(scrapy.Spider):
    def start_requests(self) -> scrapy.Request:
        data_home = pathlib.Path(self.settings["DATA_HOME"])
        urls = find_urls_to_crawl(self.name, data_home=data_home)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
