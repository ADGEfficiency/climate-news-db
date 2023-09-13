import datetime

import scrapy

from climatedb import parse
from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.spiders.base import BaseSpider


class FoxSpider(BaseSpider):
    name = "fox"

    def parse(self, response: scrapy.http.Response) -> ArticleItem:
        """
        @url https://www.foxnews.com/media/aoc-choked-up-climate-change-motherhood
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        ld_json = parse.get_ld_json(response)
        headline = ld_json["headline"]
        body = ld_json["articleBody"]
        body = parse.clean_body(body)

        unwanted = [
            "Fox News Flash top headlines are here.",
            "Check out what's clicking on Foxnews.com.",
            "Fox News Flash top entertainment and celebrity headlines are here. Check out what's clicking today in entertainment.",
            "CLICK HERE TO GET THE FOX NEWS APP",
        ]
        for unw in unwanted:
            body = body.replace(
                unw,
                "",
            )

        date_published = datetime.datetime.strptime(
            ld_json["datePublished"], "%Y-%m-%dT%H:%M:%S%z"
        )

        return ArticleItem(
            body=body,
            html=response.text,
            headline=headline,
            date_published=date_published,
            article_url=response.url,
            article_name=create_article_name(response.url, -1),
            article_start_url=find_start_url(response),
        )
