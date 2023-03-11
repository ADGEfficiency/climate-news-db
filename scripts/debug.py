import datetime
from datetime import datetime

import pandas as pd

from climatedb import databases
from climatedb.files import JSONLines

urls = JSONLines("./data-neu/urls.jsonl").read()
newspapers = databases.load_newspapers_json()
paper = newspapers["newshub"]

urls = [u for u in urls if paper["newspaper_url"] in u["url"]]
print(f" {len(urls)} urls for {paper['name']}")
start_date = datetime.fromisoformat("2022-12-15T00:00:00")
urls = [u for u in urls if start_date < datetime.fromisoformat(u["search_time_utc"])]
print(f" {len(urls)} urls for {paper['name']} after filter on {start_date}")

#  let's first see how many of these urls end up in urls.csv
import pandas as pd

urls_csv = pd.read_csv("./data-neu/urls.csv")
assert all([u["url"] in urls_csv["url"].values for u in urls])
print(" all are in urls.csv")

paper_urls, existing, rejected = databases.get_urls_for_paper(
    paper["name"], return_all=True
)
for u in urls:
    print(u["url"])
    print(f" in dispatch {u['url'] in paper_urls}")
    print(f" in existing {u['url'] in existing}")
    print(f" in rejected {u['url'] in rejected}")

    """
https://www.dw.com/en/energy-crisis-puts-global-climate-measures-to-the-test/a-63729426
    """
