import matplotlib.pyplot as plt
import pandas as pd
from scrapy.settings import Settings

from climatedb import database

settings = Settings()
settings.setmodule("climatedb.settings")
articles = database.get_all_articles_with_opinions(settings["DB_URI"], n=100000)
print(len(articles))


data = pd.DataFrame(articles)
data = data[~data["topics"].isnull()]

cols = [c for c in data.columns if "_score" in c]
data[cols] = data[cols].astype(float)
for col in cols:
    data = data[data[col] >= 0]

grp = data.groupby("newspaper_name").agg(
    count=pd.NamedAgg(column="newspaper_name", aggfunc="count"),
    scientific_accuracy_score=pd.NamedAgg(
        column="scientific_accuracy_score", aggfunc="mean"
    ),
    article_tone_score=pd.NamedAgg(column="article_tone_score", aggfunc="mean"),
)
grp = grp.sort_values("article_tone_score", ascending=False)
print(grp)


fig, axes = plt.subplots(nrows=2)
grp.index.name = "newspaper_name"
grp = grp.reset_index()

grp.plot(kind="bar", ax=axes[0], x="newspaper_name", y="scientific_accuracy_score")
grp.plot(kind="bar", ax=axes[1], x="newspaper_name", y="article_tone_score")
fig.savefig("gpt-opinion.png")
