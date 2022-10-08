from climatedb.databases import ArticlesFolders
from climatedb.registry import newspapers

db = ArticlesFolders()
articles = db.get()

fmt = "%Y-%m-%dT%H:%M:%S"

from datetime import datetime

for article in articles[:]:
    paper = newspapers[article["newspaper_id"]]

    for date in ["date_published", "date_uploaded"]:
        fmt = paper.get(date + "_fmt", fmt)

        dt = article[date]
        try:
            #  19 to avoid nonsense with timezones
            article[date] = datetime.strptime(dt[:19], fmt).isoformat()[:19]
        except ValueError:
            print(dt, date, paper["newspaper_id"])
            import pdb

            pdb.set_trace()

    db.add(article)
