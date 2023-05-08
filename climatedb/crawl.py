import pathlib
import typing

import pandas as pd
from rich import print
from scrapy.http.response.html import HtmlResponse

from climatedb import files
from climatedb.models import NewspaperMeta
from climatedb.utils import read_newspapers_json


def filter_urls(exclude_fi: files.JSONLines, urls: set) -> set:
    if exclude_fi.exists():
        exclude_urls = set()
        for article in exclude_fi.read():
            exclude_urls.add(article["article_url"])
            exclude_urls.add(article["article_start_url"])
        urls = urls - exclude_urls
    return urls


def find_urls_to_crawl(paper: str, data_home: pathlib.Path) -> list[str]:
    urls_fi = files.JSONLines(data_home / "urls.jsonl")
    urls = pd.DataFrame(urls_fi.read())
    print(f" {urls.shape} raw urls")

    papers = read_newspapers_json()

    urls["paper"] = urls["url"].apply(lambda x: find_newspaper_from_url(x, papers).name)

    #  drop urls where we couldn't find a newspaper
    urls = urls.dropna(subset="paper", axis=0)
    print(f" {urls.shape} urls after dropping no newspaper")

    #  drop duplicate urls
    urls = urls.drop_duplicates(subset="url")
    print(f" {urls.shape} urls after dropping duplicates")

    #  filter for this newspaper
    urls = urls[urls["paper"] == paper]
    print(f" {urls.shape} urls after filter for newspaper")

    urls = set(urls["url"].tolist())
    urls = filter_urls(files.JSONLines(data_home / "articles" / paper), urls)
    print(f" {len(urls)} urls after filter for article")
    urls = filter_urls(files.JSONLines(data_home / "rejected"), urls)
    print(f" {len(urls)} urls after filter for rejected")
    return list(urls)


def create_article_name(url: str, idx: int = -1) -> str:
    url = url.strip("/")
    url = url.split("?")[0]
    url = url.strip("/")
    article_id = url.split("/")
    article_id = [u for u in article_id if len(url) > 0]
    return article_id[idx].replace(".html", "")


def find_newspaper_from_url(url: str, papers: typing.Optional[list]=None) -> NewspaperMeta:
    if papers is None:
        papers = read_newspapers_json()

    for paper in papers:
        if paper.site in url:
            return paper

    raise ValueError(f"No paper found for {url}")


def find_start_url(response: HtmlResponse) -> str:
    #  if we get redirected, use the original url we search for
    url = response.request.headers.get("Referer", None)
    if url is None:
        return str(response.url)
    else:
        return str(url.decode("utf-8"))
