import scrapy
from rich import print
from scrapy.statscollectors import StatsCollector
from scrapy.utils.serialize import ScrapyJSONEncoder


class StatCollector(StatsCollector):
    def _persist_stats(self, stats: dict, spider: scrapy.Spider) -> None:
        encoder = ScrapyJSONEncoder()
        with open("stats.json", "w") as file:
            data = encoder.encode(stats)
            file.write(data)
        print(stats)
