import pandas as pd

from climatedb import databases
from rich import print

print("\n[red]urls.jsonl[/]")
"""
how many, how many duplicates
"""

print("\n[red]urls.csv[/]")
"""
how many, how many duplicates
"""

print("\n[red]apptable[/]")

raw = databases.read_app_table()
data = pd.DataFrame([d.dict() for d in raw])
print(list(data.columns))
print(f"[green]articles in apptable[/]: {data.shape[0]}")

nulls = data["date_published"].isnull()
print(f"[green]nulls in datetime[/]: {nulls.sum()}")

nulls = data[nulls]
grp = nulls.groupby("fancy_name").count().loc[:, "body"]
print(f"[green]nulls by newspaper[/]:")
print(grp.sort_values())