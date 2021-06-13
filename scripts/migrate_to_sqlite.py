from datetime import datetime
from climatedb.databases import ArticlesSQLite, ArticlesFolders
from climatedb.config import DBHOME

import pandas as pd

class TextFileFolder():
    """Folder of .txt files"""
    def __init__(
        self,
        name,
        file_key='article_id',
        folder_key='article_body',
        text_key='body'
    ):
        self.folder = DBHOME / name
        self.folder.mkdir(exist_ok=True, parents=True)
        self.file_key = file_key
        self.folder_key = folder_key
        self.text_key = text_key

    def add(self, batch):
        for article in batch:
            fi = self.folder / article[self.file_key]
            fi.with_suffix('.txt').write_text(
                article[self.text_key]
            )


class ArticlesCSV():
    def __init__(self):
        self.name = './data/climate-news-db-dataset.csv'

    def add(self, batch):
        batch = pd.DataFrame(batch)
        batch.drop(['body', 'color'], axis=1).to_csv(self.name, index=False)
        #  add one file per body
        db = TextFileFolder('article_body')
        bodies = batch[['article_id', 'body']].to_dict('records')
        db.add(bodies)



def add_articles_to_sqlite():
    schema = [
        ("newspaper", "TEXT"),
        ("newspaper_id", "TEXT"),
        ("newspaper_url", "TEXT"),
        ("body", "TEXT"),
        ("headline", "TEXT"),
        ("article_url", "TEXT"),
        ("article_id", "TEXT"),
        ("date_published", "TEXT"),
        ("date_uploaded", "TEXT"),
        ("color", "TEXT"),
    ]

    json_db = ArticlesFolders()
    sql_db = ArticlesSQLite()
    csv_db = ArticlesCSV()

    articles = json_db.get()

    print(len(articles))
    #  remove articles from early times (1970 year)
    for article in articles[1:]:
        dt = datetime.fromisoformat(
            article['date_published'][:19]
        )
        if dt.year < 1980:
            articles.remove(article)

    print(len(articles))

    sql_db.add(articles)
    csv_db.add(articles)


if __name__ == '__main__':
    add_articles_to_sqlite()
