from climatedb.spiders.china_daily import ChinaDailySpider
import scrapy
import datetime
import requests


def test_china_daily() -> None:
    spider = ChinaDailySpider()
    url = "https://www.chinadaily.com.cn/a/202301/19/WS63c8a4a8a31057c47ebaa8e4.html"
    request = scrapy.Request(url=url)
    #  get the response for this request
    response = scrapy.http.HtmlResponse(
        url=url,
        request=request,
        body=requests.get(url).content,
    )
    article = spider.parse(response)
    assert article.headline == "Companies moved to take action on climate change"
    assert article.date_published == datetime.date.fromisoformat("2023-01-19")
    assert article.datetime_uploaded

    assert article.body.startswith(
        "China will introduce more market mechanisms to encourage companies to accelerate their green, low-carbon transitions, according to the Ministry of Ecology and Environment."
    )
    assert article.body.endswith(
        "Operators of 66 thermal power generation units have voluntarily connected monitoring facilities to the ministry's network, making it possible to automatically obtain hourly emissions data, he said."
    )

    assert article.article_name == "WS63c8a4a8a31057c47ebaa8e4"
    assert article.article_url == url
