import scrapy
from climatedb.databases_neu import get_urls_for_paper, JSONLines
from pathlib import Path

from climatedb.parsing_utils import get_title, get_date
from climatedb.types import ArticleModel


class NYTimesSpider(scrapy.Spider):
    name = "nytimes"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):
        article_name = response.url.split("/")[-1]

        body = response.xpath("//p/text()").getall()

        neu_body = []
        unwanted = set(["Advertisement", "Supported by"])
        for b in body:
            if b not in unwanted:
                neu_body.append(b)

        subtitle = neu_body[0]
        body = neu_body[1:]
        body = "".join(body)

        title = get_title(response)
        title = title.replace(" - The New York Times", "")

        date = get_date(response)

        #  one jsonline - saved by scrapy for us
        meta = {
            "title": title,
            "subtitle": subtitle,
            "body": body,
            "article_url": response.url,
            "article_id": article_name,
            "date_published": date,
        }
        #  here we ensure this type is what we want!
        meta = dict(ArticleModel(**meta))

        #  save html ourselves
        fi = (
            Path.home()
            / "climate-news-db"
            / "data-reworked"
            / "articles"
            / self.name
            / article_name
        )
        fi.parent.mkdir(exist_ok=True, parents=True)
        fi = fi.with_suffix(".html")
        fi.write_bytes(response.body)
        self.log(f" saved to {fi}")
        return meta
