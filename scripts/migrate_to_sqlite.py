from config import data_home as h
from rich import print


def find_newspaper_from_url(url):
    if "www.theguardian.com" in url:
        return {"url": url, "newspaper_id": "guardian"}
    else:
        return {"url": url, "newspaper_id": "UNKNOWN"}


from multiprocessing import Pool

import pandas as pd

if __name__ == "__main__":
    fi = h / "urls.txt"
    urls = fi.read_text().split("\n")[:-1]
    print(f"loaded {len(urls)} urls")
    with Pool(4, maxtasksperchild=32) as pool:
        csv_data = pool.map(find_newspaper_from_url, urls)

    pd.DataFrame(csv_data).to_csv("./data-reworked/urls.csv", index=False)
# csv_data = [c for c in csv_data if c is not None]
