import scrapy

from climatedb.databases_neu import get_urls_for_paper, save_html, Article
from climatedb.parsing_utils import get_body

from climatedb.utils import form_article_id
from datetime import datetime


class DWSpider(scrapy.Spider):
    name = "dw"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):
        article_name = form_article_id(response.url, -2)

        title = response.xpath('//meta[@property="og:title"]/@content').get()
        #  Sour grapes: Climate change pushing wine regions farther north | DW | 01.08.2019'
        headline = title.split("|")[0].strip()

        subtitle = response.xpath('//meta[@property="og:description"]/@content').get()

        body = get_body(response)

        #  <span class="date">11.07.2017</span>
        date = response.xpath('//span[@class="date"]/text()').get()
        # <li><strong>Date</strong>
        # 13.04.2014
        # </li>
        if date is None:
            lis = response.xpath("//li/text()").getall()
            for li in lis:
                li = li.replace("\n", "")
                try:
                    date = datetime.strptime(li, "%d.%m.%Y")
                except:
                    pass

        date = date.isoformat()

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
