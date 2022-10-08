from datetime import datetime

from rich import print
from scrapy import signals

from climatedb import files
from climatedb.config import data_home


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

        #  if we get redirected, use the original url we search for
        url = response.request.headers.get("Referer", None)

        if url is None:
            url = response.url
        else:
            url = url.decode("utf-8")

        pkg = {
            "url": url,
            "error": str(failure.value),
            "search_time_utc": datetime.utcnow().isoformat(),
        }
        print(f"[red]REJECTED[/] {response.url} {failure}\n {pkg}")
        db.write([pkg])
