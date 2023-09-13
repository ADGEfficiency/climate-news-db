from datetime import datetime

from rich import print
from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.http.response.html import HtmlResponse
from scrapy.settings import Settings
from scrapy.spiders import Spider
from twisted.python.failure import Failure

from climatedb import files
from climatedb.crawl import find_start_url

settings = Settings()
settings.setmodule("climatedb.settings")


class RejectRegister(object):
    @classmethod
    def from_crawler(cls, crawler: Crawler) -> "RejectRegister":
        ext = cls()
        crawler.signals.connect(ext.spider_error, signal=signals.spider_error)
        return ext

    def spider_error(
        self, failure: Failure, response: HtmlResponse, spider: Spider
    ) -> None:
        db = files.JSONLines(settings["DATA_HOME"] / "rejected.jsonl")
        pkg = {
            "article_url": response.url,
            "article_start_url": find_start_url(response),
            "error": str(failure.value),
            "search_time_utc": datetime.utcnow().isoformat(),
        }
        print(f"[red]REJECTED[/] {response.url} {failure}\n {pkg}")
        db.write([pkg])
