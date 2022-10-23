from climatedb.databases import Article, get_urls_for_paper, save_html
from climatedb.parsing_utils import form_article_id, get_body
from climatedb.spiders.base import ClimateDBSpider


class NewsHubSpider(ClimateDBSpider):
    name = "newshub"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):
        article_name = form_article_id(response.url, -1)
        body = get_body(response)

        noise = [
            "This article is republished from The Conversation under a Creative Commons license. Read the original article here. ",
        ]
        for n in noise:
            body = body.replace(n, "")

        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        subtitle = response.xpath('//meta[@property="og:description"]/@content').get()
        date = response.xpath('//meta[@itemprop="datePublished"]/@content').get()

        meta = {
            "headline": headline,
            "subtitle": subtitle,
            "body": body,
            "article_url": response.url,
            "date_published": date,
            "article_name": article_name,
        }
        meta = Article(**meta).dict()
        save_html(self.name, article_name, response)
        return self.tail(response, meta)
