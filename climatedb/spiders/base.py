import datetime

import scrapy
from rich import print

from climatedb.databases import Article, find_start_url, save_html


class ClimateDBSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(
            f"[green]starting[/] [bold blue]{self.name}[/] [green]spider[/] - {len(self.start_urls)} urls"
        )

    def tail(self, response, meta):
        meta = Article(**meta).dict(exclude_unset=True)
        #  maybe a TODO here to bring these arguments into the Article type?
        meta["article_length"] = len(meta["body"])
        meta["date_uploaded"] = datetime.datetime.now().isoformat()
        meta["article_start_url"] = find_start_url(response)
        return meta
