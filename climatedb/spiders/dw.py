import datetime

import scrapy

from climatedb import parse
from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.spiders.base import BaseSpider


class DWSpider(BaseSpider):
    name = "dw"

    def parse(self, response: scrapy.http.response.html.HtmlResponse) -> ArticleItem:
        """
        @url https://www.dw.com/en/sour-grapes-climate-change-pushing-wine-regions-farther-north/a-49894708
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        ld_json = parse.get_ld_json(response)
        headline = ld_json["headline"]
        body = parse.get_body(response)

        unwanted = [
            "Take a look at the beta version of dw.com.",
            "We're not done yet!",
            "Your opinion can help us make it better.",
            "We use cookies to improve our service for you.",
            "You can find more information in our data protection declaration.",
            "© 2022 Deutsche Welle",
            "| Privacy Policy | Accessibility Statement | Legal notice | Contact | Mobile version ",
            "rc/amp",
            "(AFP, Reuters)",
            "Each evening at 1830 UTC, DW's editors send out a selection of the day's hard news and quality feature journalism. You can sign up to receive it directly here.",
        ]
        for unw in unwanted:
            body = body.replace(unw, "")

        date_published = datetime.datetime.strptime(
            ld_json["datePublished"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).isoformat()

        return ArticleItem(
            body=body,
            html=response.text,
            headline=headline.split("|")[0].strip(),
            date_published=date_published,
            article_url=response.url,
            article_name=create_article_name(response.url),
            article_start_url=find_start_url(response),
        )
