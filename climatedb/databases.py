from itertools import chain

import pandas as pd

from climatedb.engines import JSONFolder, SQLiteEngine, JSONLinesFile
from climatedb.config import DBHOME


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
    def __init__(
        self,
        name='final',
        folder_key='newspaper_id',
        file_key='article_id',
    ):
        self.folder_key = folder_key
        self.file_key = file_key

        self.home = DBHOME / 'articles' / name
        self.home.mkdir(exist_ok=True, parents=True)

        #  newspapers each live in their own folder
        folders = [p for p in self.home.iterdir() if p.is_dir()]

        self.folders = {
            p.name: JSONFolder(p, key=self.file_key)
            for p in folders
        }

    def add(self, batch):
        if isinstance(batch, dict):
            batch = (batch,)

        for article in batch:
            folder = article[self.folder_key]

            #  if we don't have folder for article yet
            if folder not in self.folders.keys():
                self.folders[folder] = JSONFolder(folder, key=self.file_key)

            self.folders[folder].add(article)

    def get(self):
        articles = list(chain(
            *[fldr.get() for fldr in self.folders.values()]
        ))
        print(f' loaded {len(articles)} from {len(self.folders)} folders')
        return articles

    def filter(self, key, value):
        articles = self.get()
        return [r for r in articles if r[key] == value]

    def exists(self, key, value):
        #  bool(0) -> False
        return bool(len(self.filter(key, value)))


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
    def __init__(
        self,
        db='climatedb.sqlite',
        schema=article_schema,
        index='article_id'
    ):
        self.engine = SQLiteEngine(
            table='final',
            schema=schema,
            db=db,
            index=index
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
