import datetime

from scrapy.http.response.html import HtmlResponse

from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.parse import clean_body, get_ld_json
from climatedb.spiders.base import BaseSpider


class NYTimesSpider(BaseSpider):
    name = "nytimes"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url https://www.nytimes.com/2021/10/14/climate/energy-bills-reconciliation.html
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        headline = response.xpath("//h1/text()").get().strip()
        article_name = create_article_name(response.url)
        body = response.xpath("//p/text()").getall()

        neu_body = []
        unwanted = set(
            [
                "Advertisement",
                "Supported by",
                "As a subscriber, you have to give each month. Anyone can read what you share. The editorial board represents the opinions of the board, its editor and the publisher. It is separate from the newsroom and the Op-Ed section.",
                "As a subscriber, you have to give each month.",
                "Anyone can read what you share.",
                "Anyone can read what you share. and ",
            ]
        )
        for b in body:
            if b not in unwanted:
                neu_body.append(b)

        body = neu_body[1:]
        body = " ".join(body)
        body = clean_body(body)

        try:
            ld = get_ld_json(response)
            date_published = datetime.datetime.strptime(
                ld["datePublished"],
                "%Y-%m-%dT%H:%M:%S.%fZ",
            )
        except Exception:
            date_published = datetime.datetime.strptime(
                response.xpath(
                    '//meta[@property="article:published_time"]/@content'
                ).get(),
                "%Y-%m-%dT%H:%M:%S.%fZ",
            )

        return ArticleItem(
            body=body,
            html=response.text,
            headline=headline,
            date_published=date_published,
            article_url=response.url,
            article_name=article_name,
            article_start_url=find_start_url(response),
        )
