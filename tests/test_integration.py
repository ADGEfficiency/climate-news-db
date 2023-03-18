"""Test that everything is working"""
import pathlib
import subprocess

from climatedb import files


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
    articles = files.JSONLines(base_dir / "articles" / "china_daily.jsonl")
    assert not articles.exists()

    #  run the scraping
    result = subprocess.run(
        [
            "scrapy",
            "crawl",
            "china_daily",
            "-o",
            articles.path,
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
    data = articles.read()
    assert len(data) == len(urls)
    assert data[0]["headline"] == "Companies moved to take action on climate change"

    db = pathlib.Path(base_dir / "db.sqlite")
    assert db.exists()
