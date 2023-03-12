import typing
from pathlib import Path

import pandas as pd
from rich import print

from climatedb import files
from climatedb.config import data_home as home
from climatedb.databases import find_newspaper_from_url

assert home is not None


def get_urls_for_paper(
    paper: str, return_all: bool = False
) -> typing.Union[
    typing.List[str], typing.Tuple[typing.List[str], typing.List[str], typing.List[str]]
]:
    """Gets all urls for a newspaper from $(DATA_HOME) / urls.csv"""
    assert home is not None
    print(f"[blue]GET URLS[/] {paper}")
    raw = pd.read_csv(f"{home}/urls.csv")
    mask = raw["name"] == paper
    data = raw[mask]
    urls = [{"url": u} for u in data["url"].values.tolist()]
    urls = [a["url"] for a in urls if find_newspaper_from_url(a)["name"]]

    #  default dispatch on all urls
    dispatch = urls
    print(f"[green] FOUND[/] {len(dispatch)} urls for {paper} in urls.csv")

    #  filter out articles we already have successfully parsed
    #  already filtered by newspaper
    existing = files.JSONLines(Path(home) / "articles" / f"{paper}.jsonlines")
    if existing.exists():
        existing = existing.read()
        existing_urls = set()
        for a in existing:
            for k in ['article_start_url', 'article_url']:
                existing_urls.add(a.get[k])
        # existing_urls = [a.get("article_start_url", a["article_url"]) for a in existing.read()]
        existing_urls.remove(None)
        dispatch = set(urls).difference(set(existing_urls))
        print(f" {len(dispatch)} urls after removing {len(existing_urls)} existing")

    #  filter out articles we have already failed to parse
    rejected = files.JSONLines(Path(home) / "rejected.jsonlines")
    if rejected.exists():
        rejected_urls = [a for a in rejected.read()]
        rejected_urls = set(
            [
                a["url"]
                for a in rejected_urls
                if find_newspaper_from_url(a)["name"] == paper
            ]
        )
        print(f" {len(dispatch)} urls after removing {len(rejected_urls)} rejected")
        dispatch = set(dispatch).difference(rejected_urls)

    if return_all:
        return list(dispatch), list(existing_urls), list(rejected_urls)
    else:
        return list(dispatch)

if __name__ == "__main__":
    existing = files.JSONLines(Path(home) / "articles" / f"nzherald.jsonlines")
