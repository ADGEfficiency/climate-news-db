from datetime import datetime, timezone

from climatedb.files import JSONLines
from climatedb.search import format_timestamp

urls_jsonl = JSONLines("./data-neu/urls.jsonl").read()
import pandas as pd

clean = []
for url in urls_jsonl:
    if "search_time_utc" in url.keys():
        dt = datetime.fromisoformat(url["search_time_utc"])
        dt = dt.replace(microsecond=0)
        dt = format_timestamp(dt)
        clean.append({"url": url["url"], "search_time_utc": dt})
    elif "search_time_UTC" in url.keys():
        dt = pd.to_datetime(url["search_time_UTC"])
        dt = format_timestamp(dt)
        clean.append({"url": url["url"], "search_time_utc": dt})

assert len(clean) == len(urls_jsonl)
JSONLines("./data-neu/urls.jsonl").write(clean)
