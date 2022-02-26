from config import data_home as home
from rich import print
from multiprocessing import Pool
import json
import pandas as pd


def find_newspaper_from_url(url):
    #  TODO drive this from newspapers.json
    if "www.theguardian.com" in url:
        return {"url": url, "newspaper_id": "guardian"}
    if "www.nytimes.com" in url:
        return {"url": url, "newspaper_id": "nytimes"}
    if "www.aljazeera.com" in url:
        return {"url": url, "newspaper_id": "aljazeera"}
    else:
        return {"url": url, "newspaper_id": "UNKNOWN"}


if __name__ == "__main__":
    fi = home / "urls.jsonl"
    urls = fi.read_text().split("\n")[:-1]
    urls = [json.loads(u)["url"] for u in urls]
    print(f"loaded {len(urls)} urls")

    with Pool(4, maxtasksperchild=32) as pool:
        csv_data = pool.map(find_newspaper_from_url, urls)

    pd.DataFrame(csv_data).to_csv(f"{home}/urls.csv", index=False)
    print(f"saved urls.csv {len(csv_data)} urls")
