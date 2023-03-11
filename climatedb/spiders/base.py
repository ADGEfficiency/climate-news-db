import datetime
from pathlib import Path

import scrapy
from rich import print

from climatedb.config import data_home as home
from climatedb.databases import (
    Article,
    find_newspaper_from_url,
    find_start_url,
    save_html,
)
from climatedb.files import HTMLFile


class ClimateDBSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(
            f"[green]starting[/] [bold blue]{self.name}[/] [green]spider[/] - {len(self.start_urls)} urls"
        )

    def tail(self, response, meta: dict) -> dict:
        meta = Article(**meta).dict(exclude_unset=True)
        #  maybe a TODO here to bring these arguments into the Article type?
        meta["article_length"] = len(meta["body"])
        meta["date_uploaded"] = datetime.datetime.now().isoformat()
        meta["article_start_url"] = find_start_url(response)

        paper = find_newspaper_from_url({"url": meta["article_url"]})
        fi = HTMLFile(Path(home) / "html" / paper["name"] / meta["article_name"])
        fi.write(response.text)
        return meta
