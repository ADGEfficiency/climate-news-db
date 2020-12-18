from pathlib import Path

from climatedb.engines import engines

DBHOME = Path.home() / "climate-news-db-data"


class URLs():
    def __init__(
        self,
        name,
        key,
        schema=None,
        engine='jsonl'
    ):
        Engine = engines[engine]
        self.engine = Engine(name, key, schema)

    def add(self, batch):
        for data in batch:
            if not self.engine.exists(data['url']):
                self.engine.add(batch)

    def get(self, num=0):
        data = self.engine.get()
        return data[-num:]

    def __len__(self):
        return len(self.engine)


class RawArticles():
    def __init__(
        self,
        name='raw',
        key='article_id',
        value='html'
    ):
        self.engine = engines['html-folder'](name, key=key, value=value)
        self.key = key

    def add(self, batch):
        self.engine.add(batch)

    def get(self, value=None):
        data = self.engine.get()
        if value is None:
            return data

        for da in data:
            if da[self.key] == value:
                return da


class Articles():
    def __init__(
        self,
        name='final',
        engine='json-folder',
        key='article_id',
        schema=None,
    ):
        Engine = engines[engine]
        self.engine = Engine(name, key, schema)
        self.key = key

    def add(self, batch):
        for data in batch:
            if not self.engine.exists(data[self.key]):
                self.engine.add(batch)

    def get(self, value=None):
        data = self.engine.get()
        if value is None:
            return data

        for da in data:
            if da[self.key] == value:
                return da

    def __len__(self):
        return len(self.engine)
