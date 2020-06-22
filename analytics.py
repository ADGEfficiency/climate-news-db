import pandas as pd


def create_article_df(articles):
    df = pd.DataFrame(articles)
    df.loc[:, 'published'] = pd.to_datetime(df.loc[:, 'published'], utc=True)  # hack!!!
    return df


def groupby_newspaper(df):
    df.loc[:, 'article-length'] = df.loc[:, 'body'].apply(lambda x: len(x.split(' ')))
    lens = df.groupby('newspaper').agg({'article-length': ['mean', 'count']})
    lens.columns = ['average_article_length', 'article_count']
    lens = lens.sort_values('article_count', ascending=False)
    return lens.reset_index()
