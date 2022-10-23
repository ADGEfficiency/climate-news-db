from datetime import datetime

from rich import print
from scrapy import signals

from climatedb import files
from climatedb.config import data_home
from climatedb.databases import find_start_url


class RejectRegister(object):
    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        crawler.signals.connect(ext.spider_error, signal=signals.spider_error)
        return ext

    def spider_error(self, failure, response, spider):
        """
        Append failed URL to a `rejected.jsonlines` file so we don't try to parse again
        """
        db = files.JSONLines(f"{data_home}/rejected.jsonlines")

        url = find_start_url(response)

        pkg = {
            "url": url,
            "error": str(failure.value),
            "search_time_utc": datetime.utcnow().isoformat(),
        }
        print(f"[red]REJECTED[/] {response.url} {failure}\n {pkg}")
        db.write([pkg])
