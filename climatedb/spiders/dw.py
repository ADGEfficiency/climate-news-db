from datetime import datetime

from climatedb import parsing_utils
from climatedb.databases import Article, get_urls_for_paper, save_html
from climatedb.parsing_utils import get_body
from climatedb.spiders.base import ClimateDBSpider


class DWSpider(ClimateDBSpider):
    name = "dw"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):
        article_name = parsing_utils.form_article_id(response.url, -2)

        title = response.xpath('//meta[@property="og:title"]/@content').get()
        #  Sour grapes: Climate change pushing wine regions farther north | DW | 01.08.2019'
        headline = title.split("|")[0].strip()

        subtitle = response.xpath('//meta[@property="og:description"]/@content').get()

        body = get_body(response)

        #  <p class="accesstobeta__text">Take a look at the <strong>beta</strong> version of dw.com. We're not done yet! Your opinion can help us make it better.</p>

        unwanted = [
            "Take a look at the beta version of dw.com.",
            "We're not done yet!",
            "Your opinion can help us make it better.",
            "We use cookies to improve our service for you.",
            "You can find more information in our data protection declaration.",
            "© 2022 Deutsche Welle",
            "| Privacy Policy | Accessibility Statement | Legal notice | Contact | Mobile version ",
        ]
        for unw in unwanted:
            body = body.replace(unw, "")

        #  <span class="date">11.07.2017</span>
        try:
            date = response.xpath('//span[@class="date"]/text()').get()
            date = datetime.strptime(date, "%d.%m.%Y")
        except:
            date = None

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

        #  <time aria-hidden="true">06/13/2021</time>
        if date is None:
            try:
                date = response.xpath("//time/text()").get()
                if isinstance(date, str):
                    date = datetime.strptime(date, "%d/%M/%Y")
                else:
                    date = datetime.strptime(date[0], "%d/%M/%Y")
            except:
                date = None

        date = date.isoformat()

        meta = {
            "headline": headline,
            "subtitle": subtitle,
            "body": body,
            "article_url": response.url,
            "date_published": date,
            "article_name": article_name,
        }
        return self.tail(response, meta)
