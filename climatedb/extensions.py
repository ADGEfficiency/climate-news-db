from scrapy import signals
from datetime import datetime
from climatedb import files
from climatedb.config import data_home


class RejectRegister(object):
    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        crawler.signals.connect(ext.spider_error, signal=signals.spider_error)
        return ext

    def spider_error(self, failure, response, spider):
        print(f"[red]failed[/] {response.url} {failure}")
        #  now want to append this to a rejected file
        #  which means next time we won't try to
        #  reprocess them again
        db = files.JSONLines(f"{data_home}/rejected.jsonlines")
        pkg = {
            "url": response.url,
            "error": str(failure.value),
            "search_time_utc": datetime.utcnow().isoformat(),
        }
        print(pkg)
        #  TODO - files.JSONLines should be able to take a single dict as input
        db.write(
            [
                pkg,
            ]
        )
