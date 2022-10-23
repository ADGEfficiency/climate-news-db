import json
from multiprocessing import Pool
from pathlib import Path

import pandas as pd
from rich import print

from climatedb.config import data_home as home
from climatedb.databases import find_newspaper_from_url

if __name__ == "__main__":
    from pathlib import Path

    fi = Path(home) / "urls.jsonl"
    urls = fi.read_text().split("\n")[:-1]
    urls = [json.loads(u)["url"] for u in urls]
    print(f"loaded {len(urls)} urls")
    urls = set(urls)
    print(f"unique {len(urls)} urls")

    with Pool(4, maxtasksperchild=32) as pool:
        csv_data = pool.map(find_newspaper_from_url, list(urls))

    df = pd.DataFrame(csv_data)
    df.to_csv(f"{home}/urls.csv", index=False)
    print(f"saved urls.csv {df.shape[0]} urls")
