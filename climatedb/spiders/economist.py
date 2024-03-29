import datetime

from scrapy.http.response.html import HtmlResponse

from climatedb import parse
from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.spiders.base import BaseSpider


class EconomistSpider(BaseSpider):
    name = "economist"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url https://www.economist.com/leaders/2022/01/22/the-climate-issue
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        ld_json = parse.get_ld_json(response)

        body = ld_json["articleBody"]
        body = parse.clean_body(body)

        unwanted = [
            "For more coverage of climate change, register for The Climate Issue, our fortnightly newsletter, or visit our climate-change hub",
            'Sign up to our new fortnightly climate-change newsletter hereThis article appeared in the Leaders section of the print edition under the headline "The climate issue"',
        ]
        for unw in unwanted:
            body = body.replace(unw, "")

        headline = ld_json["headline"]
        date_published = ld_json["datePublished"]
        date_published = datetime.datetime.strptime(
            date_published, "%Y-%m-%dT%H:%M:%SZ"
        )

        return ArticleItem(
            body=body,
            html=response.text,
            headline=headline,
            date_published=date_published,
            article_url=response.url,
            article_name=create_article_name(response.url),
            article_start_url=find_start_url(response),
        )
