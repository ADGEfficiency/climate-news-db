import datetime

from rich import print
import scrapy

from climatedb.databases import Article, save_html


class ClimateDBSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(
            f"[green]starting[/] [bold blue]{self.name}[/] [green]spider[/] - {len(self.start_urls)} urls"
        )

    def tail(self, response, meta):
        meta = Article(**meta).dict(exclude_unset=True)
        meta["article_length"] = len(meta["body"])
        meta["date_uploaded"] = datetime.datetime.now().isoformat()
        return meta
