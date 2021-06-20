"""runs checker on each url"""
import climatedb.databases as db
from climatedb.registry import find_newspaper_from_url

from shutil import move

import os

fi = db.URLs("urls/urls.jsonl")
urls = fi.get()

try:
    move("data/urls/urls.jsonl", "data/urls/urls.jsonl.bak")
except FileNotFoundError:
    pass

urls_so_far = set()

clean_urls = []
dirty_urls = []
for n, url in enumerate(urls, 1):

    paper = find_newspaper_from_url(url["url"])

    try:
        if paper and paper["checker"](url["url"]) and url["url"] not in urls_so_far:
            print(f" keep {url}")
            clean_urls.append(url)
            urls_so_far.add(url["url"])
        else:
            print(f" not keep {url}")
            dirty_urls.append(url)

        print(f" pct kept {100 * len(clean_urls) / n}%, {n}/{len(urls)}\n")
    except TypeError:
        print(url)
        breakpoint()

fi = db.URLs("urls/urls.jsonl")
fi.add(clean_urls)
