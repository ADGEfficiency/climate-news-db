from pathlib import Path

import scrapy
from rich import print

from climatedb.databases_neu import get_urls_for_paper, JSONLines
from climatedb.types import ArticleModel
from climatedb.parsing_utils import get_title, get_date


class GuardianSpider(scrapy.Spider):
    name = "guardian"

    #  these aren't actually used (overwritten by get_urls_for_paper)
    #  more included as reference
    start_urls = [
        "https://www.theguardian.com/commentisfree/2018/oct/30/climate-change-action-effective-ipcc-report-fossil-fuels",
        #  tough to know what to do with the first p element here
        "https://www.theguardian.com/environment/2020/jun/17/climate-crisis-alarm-at-record-breaking-heatwave-in-siberia",
    ]
    start_urls = get_urls_for_paper(name)

    def __init__(self, *args, **kwargs):
        super(GuardianSpider, self).__init__(*args, **kwargs)

        #  use the -a start_url="some/url" CLI argument if we pass it
        if "start_url" in kwargs.keys():
            self.start_urls = [kwargs.get("start_url")]

    def parse(self, response):
        article_name = response.url.split("/")[-1]

        #  title
        title = get_title(response)

        #  body
        body = response.xpath(
            '//p[not(contains(.,"Last modified") or contains(.,"First published"))]/text()'
        ).getall()

        #  filtering out the subtitle
        #  subtile dosen't usually have a . at the end
        if body[0][-1] != ".":
            subtitle = body[0]
            body = body[1:]
        else:
            subtitle = None

        body = "".join(body)

        #  published date

        #  https://www.theguardian.com/commentisfree/2018/oct/30/climate-change-action-effective-ipcc-report-fossil-fuels
        #  <label for="dateToggle" class="dcr-hn0k3p">Tue 30 Oct 2018 14.58 GMT</label>
        #  this strategy doesn't work
        date = response.xpath('//label[@for="dateToggle"]//text()').get()

        #  https://www.theguardian.com/global-development/2013/sep/27/climate-change-poor-countries-ipcc
        #  can also have
        #  <div class="dcr-km9fgb">Fri 27 Sep 2013 09.01 BST</div>

        #  soln is to -> find GMT or BST
        #  using .get here is a bit cowboy - this will return 2 things - second is last modified
        #  this doesn't work - this fails on
        #  https://www.theguardian.com/environment/2014/mar/31/climate-change-report-ipcc-governments-unprepared-live-coverage
        #  has two bits for the date (BST in separate tag)
        date = response.xpath(
            '//*[contains(text(), "GMT") or contains(text(), "BST")]//text()'
        ).get()

        # date = date.replace("BST", "+0100")
        # date = date.replace("GMT", "+0000")
        # date = datetime.strptime(date, "%a %d %b %Y %H.%M %z")

        #  instead try to find
        #  <meta property="article:published_time" content="2014-03-31T10:16:33.000Z" />
        #  <meta property="article:published_time" content="2018-10-30T14:58:39.000Z"/>

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

        fi.with_suffix(".html").write_bytes(response.body)
        self.log(f" saved to {fi}.html")

        return meta
