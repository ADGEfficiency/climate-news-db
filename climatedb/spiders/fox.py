from climatedb.databases_neu import get_urls_for_paper, JSONLines, save_html, Article
from climatedb.utils import form_article_id
from climatedb.spiders.base import ClimateDBSpider


class FoxSpider(ClimateDBSpider):
    name = "fox"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):

        article_name = form_article_id(response.url, -1)
        body = response.xpath(
            '//div[@itemprop="articleBody"]/descendant-or-self::*/text()'
        ).getall()

        unwanted = []
        for unwanted in [
            "Fox News Flash top headlines are here. Check out what's clicking on Foxnews.com.",
            "Get all the latest news on\xa0coronavirus\xa0and more delivered daily to your inbox.\xa0Sign up here.",
        ]:
            body = [b for b in body if unwanted not in b]

        body = "".join(body)

        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        subtitle = response.xpath('//meta[@property="og:description"]/@content').get()
        date = response.xpath('//meta[@name="pubdate"]/@content').get()

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
        return meta
