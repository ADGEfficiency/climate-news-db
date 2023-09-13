import pathlib
from datetime import date, datetime, timezone

from climatedb import files, models
from climatedb.crawl import find_urls_to_crawl


def format_timestamp(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")


def get_timestamp() -> str:
    stamp = datetime.now(timezone.utc)
    return format_timestamp(stamp)


def test_find_urls_to_scrape(base_dir: pathlib.Path) -> None:
    urls_fi = files.JSONLines(base_dir / "urls.jsonl")

    #  setup stub urls.jsonl with duplicates
    raw_urls = [
        models.RawURL(
            url="https://www.chinadaily.com.cn/a/202301/19/WS63c8a4a8a31057c47ebaa8e4.html",
            search_time_utc=get_timestamp(),
        ),
        models.RawURL(
            url="https://www.chinadaily.com.cn/a/202301/19/WS63c8a4a8a31057c47ebaa8e4.html",
            search_time_utc=get_timestamp(),
        ),
    ]
    urls_fi.write([u.__dict__ for u in raw_urls])

    #  tests that we drop the duplicate
    urls = find_urls_to_crawl("china_daily", data_home=base_dir)
    assert len(urls) == 1

    #  simulate that we have already crawled this url
    article_fi = files.JSONLines(base_dir / "articles" / "china_daily.jsonl")

    article_fi.write(
        [
            models.ArticleMeta(
                headline="",
                body="",
                date_published=date.fromisoformat("2020-01-01"),
                article_name="",
                article_url="https://www.chinadaily.com.cn/a/202301/19/WS63c8a4a8a31057c47ebaa8e4.html",
                article_start_url="https://www.chinadaily.com.cn/a/202301/19/WS63c8a4a8a31057c47ebaa8e4.html",
                datetime_crawled_utc=datetime.now(timezone.utc),
            ).__dict__
        ]
    )
    urls = find_urls_to_crawl("china_daily", data_home=base_dir)
    assert len(urls) == 0

    #  simulate urls we have already rejected
    urls_fi.write(
        [
            models.RawURL(
                url="https://www.chinadaily.com.cn/a/202302/21/WS63f4aea4a31057c47ebb004e.html",
                search_time_utc=get_timestamp(),
            ).__dict__
        ]
    )
    urls = find_urls_to_crawl("china_daily", data_home=base_dir)
    assert len(urls) == 1

    reject_fi = files.JSONLines(base_dir / "rejected")
    reject_fi.write(
        [
            models.RejectedURL(
                article_url="https://www.chinadaily.com.cn/a/202302/21/WS63f4aea4a31057c47ebb004e.html",
                article_start_url="https://www.chinadaily.com.cn/a/202302/21/WS63f4aea4a31057c47ebb004e.html",
                datetime_rejected_utc=get_timestamp(),
            ).__dict__
        ]
    )
    urls = find_urls_to_crawl("china_daily", data_home=base_dir)
    assert len(urls) == 0
