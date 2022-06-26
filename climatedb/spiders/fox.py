from datetime import datetime
from climatedb.databases import get_urls_for_paper, save_html, Article
from climatedb.parsing_utils import get_body
from climatedb.spiders.base import ClimateDBSpider
from climatedb.parsing_utils import form_article_id


class FoxSpider(ClimateDBSpider):
    name = "fox"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):
        article_name = form_article_id(response.url, -1)
        body = get_body(response)

        body = response.xpath(
            '//div[@class="article-body"]/descendant-or-self::p/text()'
        ).getall()
        body = "".join(body)

        unwanted = [
            "Fox News Flash top headlines are here.",
            "Check out what's clicking on Foxnews.com.",
            "Fox News Flash top entertainment and celebrity headlines are here. Check out what's clicking today in entertainment.",
        ]
        for unw in unwanted:
            body = body.replace(
                unw,
                "",
            )

        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        subtitle = response.xpath('//meta[@property="og:description"]/@content').get()

        date = response.xpath('//meta[@itemprop="datePublished"]/@content').get()

        if date is None:
            date = response.xpath('//div[@class="article-date"]/time/text()').get()
            date = date.strip(" ")

            date = date.split(" ")[:3]
            date = " ".join(date)
            date = datetime.strptime(date, "%B %d, %Y")

        meta = {
            "headline": headline,
            "subtitle": subtitle,
            "body": body,
            "article_url": response.url,
            "date_published": date,
            "article_name": article_name,
        }
        return self.tail(response, meta)
