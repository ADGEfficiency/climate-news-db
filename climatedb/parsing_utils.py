import pytz
from datetime import datetime


def get_title(response) -> str:
    return response.css("title::text").get()


def get_date(response) -> datetime:
    date = response.xpath('//meta[@property="article:published_time"]/@content').get()
    assert date[-1] == "Z"
    date = date.split(".")[0]
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    tz = pytz.timezone("UTC")
    date = tz.localize(date)
    return date
