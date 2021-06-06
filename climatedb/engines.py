import abc
import json

from climatedb.config import DBHOME

from collections import namedtuple
import sqlite3


class AbstractDB(abc.ABC):
    @abc.abstractmethod
    def add(self, batch):
        raise NotImplementedError()

    @abc.abstractmethod
    def get(self, reference):
        raise NotImplementedError()

    @abc.abstractmethod
    def exists(self, reference):
        raise NotImplementedError()


class JSONLinesFile(AbstractDB):
    """Single File, each row a JSON"""
    def __init__(self, name, key=None, schema=None):
        self.data = DBHOME / name
        self.data.parent.mkdir(exist_ok=True, parents=True)
        self.key = key

        self.unique_keys = set()
        if self.data.is_file():
            for d in self.get():
                self.unique_keys.add(d[self.key])

    def add(self, batch):
        if isinstance(batch, dict):
            batch = (batch,)

        new_batch = []
        for d in batch:
            self.unique_keys.add(d[self.key])
            new_batch.append(json.dumps(d) + "\n")
        batch = new_batch

        mode = 'a'
        if not self.data.is_file():
            mode = 'w'
        with open(self.data, mode) as fp:
            fp.writelines(batch)

    def get(self):
        if not self.data.is_file():
            print('empty')
            return []

        with open(self.data, "r") as fp:
            data = fp.read()
            data = data.split("\n")
            data.remove("")
        return [json.loads(d) for d in data]

    def exists(self, value):
        if not self.data.is_file():
            return False
        if value in self.unique_keys:
            return True
        return False

    def __len__(self):
        return len(self.get())


class HTMLFolder(AbstractDB):
    """Folder of HTML files"""
    def __init__(
        self,
        name,
        key,
        value
    ):
        self.fldr = DBHOME / name
        self.fldr.mkdir(exist_ok=True, parents=True)
        self.key = key
        self.value = value

    def add(self, batch):
        if isinstance(batch, dict):
            batch = (batch,)
        for data in batch:
            key = data[self.key]
            value = data[self.value]

            fi = (self.fldr / key).with_suffix('.html')
            with open(fi, 'w') as fi:
                fi.write(value)

    def get(self):
        data = []
        for f in self.fldr.iterdir():
            if f.is_file() and f.suffix == '.html':
                with open(f, 'r') as fi:
                    data.append(
                        {self.key: f.with_suffix('').name,
                         self.value: fi.read()}
                    )
        return data

    def exists(self, key):
        key += '.html'
        files = [f.name for f in self.fldr.iterdir()]
        if key in files:
            return True


class JSONFolder(AbstractDB):
    """Folder of JSON files"""
    def __init__(
        self,
        name,
        key,
        schema=None
    ):
        self.fldr = DBHOME / name
        self.fldr.mkdir(exist_ok=True, parents=True)
        self.key = key

    def add(self, batch):
        if isinstance(batch, dict):
            batch = (batch,)

        for data in batch:
            key = data[self.key]

            fi = (self.fldr / key).with_suffix('.json')
            with open(fi, 'w') as fi:
                fi.write(json.dumps(data))

    def get(self):
        data = []
        for f in self.fldr.iterdir():
            if f.is_file() and f.suffix == '.json':
                with open(f, 'r') as fi:
                    data.append(json.loads(fi.read()))
        return data

    def exists(self, key):
        key += '.json'
        files = [f.name for f in self.fldr.iterdir()]
        if key in files:
            return True

    def __len__(self):
        return len([f for f in self.fldr.iterdir() if f.suffix == '.json'])


def format_schema(schema):
    names = ''
    sql_schema = ''
    for name, dtype in schema:
        names += f'{name}, '
        sql_schema += f'{name} {dtype}, '

    names = names.strip(', ')
    sql_schema = sql_schema.strip(', ')
    print(names)
    print(sql_schema)
    return names, sql_schema


class SQLiteEngine(AbstractDB):
    def __init__(
        self,
        table,
        schema,
        db='climatedb.sqlite'
    ):
        self.table = table
        names, schema = format_schema(schema)
        self.record = namedtuple(table, names)
        self.schema = schema

        if db == 'test':
            self.c = sqlite3.connect(':memory:', check_same_thread=False)
        else:
            self.c = sqlite3.connect(DBHOME / db, check_same_thread=False)

        qry = f"CREATE TABLE IF NOT EXISTS {self.table} ({schema});"
        self.c.execute(qry)

    def add(self, batch):
        for data in batch:
            data = tuple(self.record(**data))
            rhs = '(' + ('?,' * (len(data)-1)) + '?)'
            qry = f'INSERT INTO {self.table} VALUES ' + rhs
            self.c.execute(qry, data)
        self.c.commit()

    def get(self):
        data = self.c.execute(f'SELECT * FROM {self.table}').fetchall()
        return [self.record(*d)._asdict() for d in data]

    def exists(self, key, value):
        data = self.c.execute(f'SELECT * FROM {self.table} WHERE {key}=?', (value, )).fetchall()
        if data:
            return True

    def filter(self, key, value):
        data = self.c.execute(f'SELECT * FROM {self.table} WHERE {key}=?', (value, )).fetchall()
        return [self.record(*d)._asdict() for d in data]


engines = {
    'jsonl': JSONLinesFile,
    'html-folder': HTMLFolder,
    'json-folder': JSONFolder,
    'sqlite': SQLiteEngine
}
