from config import data_home as home
from rich import print
from multiprocessing import Pool
import json
import pandas as pd

from climatedb.databases_neu import JSONFile


def find_newspaper_from_url(url):

    papers = JSONFile(home / "newspapers.json").read()

    for paper in papers.values():
        if paper["newspaper_url"] in url:
            return {"url": url, **paper}

    return {"name": "UNKNOWN"}


if __name__ == "__main__":
    fi = home / "urls.jsonl"
    urls = fi.read_text().split("\n")[:-1]
    urls = [json.loads(u)["url"] for u in urls]
    print(f"loaded {len(urls)} urls")

    with Pool(4, maxtasksperchild=32) as pool:
        csv_data = pool.map(find_newspaper_from_url, urls)

    df = pd.DataFrame(csv_data)
    df.to_csv(f"{home}/urls.csv", index=False)
    print(f"saved urls.csv {df.shape[0]} urls")
