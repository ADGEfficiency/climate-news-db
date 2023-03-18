"""Test that everything is working"""
import pathlib
import subprocess

from climatedb import database, files


def test_integration(base_dir: pathlib.Path) -> None:
    #  create a dummy jsonlines urls file
    urls = [
        {
            "url": "https://www.chinadaily.com.cn/a/202301/19/WS63c8a4a8a31057c47ebaa8e4.html",
            "search_time_utc": "2023-03-11T13:50:13.931516",
        }
    ]
    fi = files.JSONLines(base_dir / "urls.jsonl")
    fi.write(urls)

    #  the output where our articles go
    articles_fi = files.JSONLines(base_dir / "articles" / "china_daily.jsonl")
    assert not articles_fi.exists()

    #  run the scraping
    result = subprocess.run(
        [
            "scrapy",
            "crawl",
            "china_daily",
            "-o",
            articles_fi.path,
            "-s",
            f"DB_URI=sqlite:///{base_dir}/db.sqlite",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print(result.stdout.decode())
    print(result.stderr.decode())

    #  check we saved articles to jsonlines
    assert files.JSONLines(base_dir / "articles" / "china_daily.jsonl").exists()
    data = articles_fi.read()
    assert len(data) == len(urls)
    assert data[0]["headline"] == "Companies moved to take action on climate change"

    #  check we saved to database
    db = pathlib.Path(base_dir / "db.sqlite")
    assert db.exists()
    articles = database.read_all_articles(db_uri=f"sqlite:///{base_dir}/db.sqlite")
    assert len(articles) == 1

    #  check we don't duplicate articles
    result = subprocess.run(
        [
            "scrapy",
            "crawl",
            "china_daily",
            "-o",
            articles_fi.path,
            "-s",
            f"DB_URI=sqlite:///{base_dir}/db.sqlite",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # print(result.stdout.decode())
    # print(result.stderr.decode())
    articles = database.read_all_articles(db_uri=f"sqlite:///{base_dir}/db.sqlite")
    assert len(articles) == 1
