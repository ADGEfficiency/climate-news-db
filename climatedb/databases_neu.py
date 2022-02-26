import json
import pandas as pd
from typing import List
from rich import print
from pathlib import Path


def get_urls_for_paper(paper: str) -> List[str]:
    """
    load urls.csv
    - urls csv has url, newspaper_id

    this is made in add_newspaper_to_urls.py
    """
    raw = pd.read_csv("./datareworked/urls.csv")
    mask = raw["newspaper_id"] == paper
    data = raw[mask]
    urls = data["url"].values.tolist()

    #  here we can filter out what we already have
    existing = (
        Path.home()
        / "climate-news-db"
        / "datareworked"
        / "articles"
        / f"{paper}.jsonlines"
    )
    if existing.is_file():
        jl = JSONLines(existing)
        existing = jl.read()
        existing = [a["article_url"] for a in existing]

        #  last one is '' - TODO do this properly
        dispatch = set(urls).difference(set(existing))
    else:
        dispatch = urls
        existing = []

    print(
        f"all_urls {raw.shape[0]}, urls {len(urls)}, existing {len(existing)}, dispatch {len(dispatch)}"
    )

    return list(dispatch)


class JSONLines:
    def __init__(self, path):
        self.path = Path(path)

    def read(self):
        data = self.path.read_text().split("\n")[:-1]
        return [json.loads(a) for a in data]
        return data
