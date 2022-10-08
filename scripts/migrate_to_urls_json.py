"""Migrates from urls.data list to urls.json"""
from datetime import datetime
from multiprocessing import Pool

import tqdm

from climatedb.config import DBHOME
from climatedb.databases import URLs
from climatedb.registry import find_newspaper_from_url


def check_data(url):
    try:
        paper = find_newspaper_from_url(url)
        checker = paper["checker"]
        if checker(url):
            # print(f'checked {url}')
            return url
        else:
            # print(f'reject {url}')
            pass
    except TypeError:  # sometimes can't find paper because of times urls
        pass


if __name__ == "__main__":
    start_fresh = True
    check_urls = False

    with open(DBHOME / "urls" / "urls.data", "r") as fi:
        data = fi.readlines()
        data = [d.strip("\n") for d in data]

    print(f"read {len(data)} from urls/urls.data")
    data = list(set(data))
    print(f"uniques {len(data)}")

    print("starting checking in parallel")
    with Pool(8) as pool:
        pool = Pool(processes=8)
        for _ in tqdm.tqdm(pool.imap_unordered(check_data, data), total=len(data)):
            pass

    print(f"new_data {len(data)} samples after running all checkers")
    data = [
        {"url": d, "search_time_UTC": datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S")}
        for d in data
    ]
    print(f"added timestamps")

    urls = URLs("urls/urls.jsonl", engine="jsonl", key="url")
    if start_fresh and len(urls):
        urls.engine.data.unlink()

    print(f"adding urls to {urls.name}")
    print(f"  before {len(urls)}")
    urls.add(data)
    print(f"  after {len(urls)}")
