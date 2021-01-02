import pandas as pd


def create_article_df(articles):
    df = pd.DataFrame(articles)
    df.loc[:, "date_published"] = pd.to_datetime(
        df.loc[:, "date_published"], utc=True
    )
    nice_dates = [
        pd.to_datetime(d)
        for d in df.loc[:, 'date_published'].values
    ]
    df.loc[:, "date_published_nice"] = nice_dates
    return df



def groupby_newspaper(df):
    df.loc[:, "article-length"] = df.loc[:, "body"].apply(lambda x: len(x.split(" ")))
    lens = df.groupby("newspaper_id").agg({"article-length": ["mean", "count"]})
    lens.columns = ["average_article_length", "article_count"]
    lens = lens.sort_values("article_count", ascending=False)
    return lens.reset_index()


def groupby_years_and_newspaper(df):
    g = (
        df.groupby([df.loc[:, "newspaper_id"], df.loc[:, "date_published"].dt.year])
        .count()
        .loc[:, "newspaper"]
    )

    g = g.reset_index()
    # g = g.set_index('date_published')

    years = sorted(list(set(g.loc[:, "date_published"])))

    papers = list(set(g.loc[:, "newspaper_id"]))

    paper_json = {}
    for paper in papers:
        counts = []
        for year in years:
            mask = (g.loc[:, "newspaper_id"] == paper) & (
                g.loc[:, "date_published"] == year
            )
            count = g.loc[mask, :]

            if count.values.size == 0:
                counts.append(0.0)
            else:
                counts.append(float(count.loc[:, "newspaper"]))

        paper_json[paper] = counts

    check = None
    for k, v in paper_json.items():
        if not check:
            check = len(v)
        else:
            assert len(v) == check

    return {
        **paper_json,
        "years": years,
    }
