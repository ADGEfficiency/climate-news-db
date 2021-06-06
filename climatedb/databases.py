from itertools import chain

import pandas as pd

from climatedb.engines import JSONFolder, SQLiteEngine, JSONLinesFile
from climatedb.config import DBHOME


class AbstractDB():
    def get(self):
        pass
    def get_record_by_key(self, key, value):
        pass


class URLs():
    def __init__(
        self,
        name,
        key='url',
        schema=None,
        engine='jsonl'
    ):
        self.engine = JSONLinesFile(name, key, schema)

    def add(self, batch):
        for data in batch:
            if not self.engine.exists(data['url']):
                self.engine.add(batch)

    def get(self, num=0):
        data = self.engine.get()
        return data[-num:]

    def __len__(self):
        return len(self.engine)

    def exists(self, key):
        return self.engine.exists(key)


class ArticlesFolders():
    """nested folders of JSON files, one folder per newspaper"""
    def __init__(self):
        self.home = DBHOME / 'articles' / 'final'

        #  newspapers each live in their own folder
        papers = [p for p in self.home.iterdir() if p.is_dir()]

        self.papers = {
            p.name: JSONFolder(p, key='article_id') for p in papers
        }
        articles = list(chain(
            *[fldr.get() for fldr in self.papers.values()]
        ))

        self.articles = articles
        print(f' loaded {len(self.articles)} from {len(self.papers)} newspapers')

    def add(self, batch):
        if isinstance(batch, dict):
            batch = (batch,)
        for article in batch:
            paper = article['newspaper_id']
            self.papers[paper].add(article)

    def get(self):
        return self.articles

    def filter(self, key, value):
        return [r for r in self.articles if r[key] == value]


article_schema = [
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


class ArticlesSQLite():
    def __init__(self):
        self.engine = SQLiteEngine(
            table='final',
            schema=article_schema,
            db='climatedb.sqlite'
        )

    def get(self):
        return self.engine.get()

    def filter(self, key, value):
        return self.engine.filter(key, value)

    def add(self, batch):
        return self.engine.add(batch)


databases = {
    'folders': ArticlesFolders,
    'sqlite': ArticlesSQLite
}


if __name__ == '__main__':
    db = ArticlesSQLite()
    print(db.get())
