import abc
from pathlib import Path
import json

from collections import namedtuple
import sqlite3

DBHOME = Path.home() / "climate-news-db-data"


class AbstractDB(abc.ABC):
    @abc.abstractmethod
    def add(self, batch):
        raise NotImplementedError()

    @abc.abstractmethod
    def get(self, reference):
        raise NotImplementedError()


class File(AbstractDB):
    """Single File"""
    def __init__(self, name):
        self.data = DBHOME / name

    def add(self, batch):
        if isinstance(batch, str):
            batch = (batch,)
        batch = [d + "\n" for d in batch]
        mode = 'a'
        if not self.data.is_file():
            mode = 'w'

        with open(self.data, mode) as fp:
            fp.writelines(batch)

    def get(self, reference=None):
        with open(self.data, "r") as fp:
            data = fp.read()
            data = data.split("\n")
            data.remove("")
            return data[-reference:]


class Folder(AbstractDB):
    """Folder of files"""
    def __init__(
        self,
        name,
        folder_key='newspaper_id',
        file_key='article_id'
    ):
        self.name = DBHOME / name
        self.folder_key = folder_key
        self.file_key = file_key
        self.data = {}

    def add(self, batch):
        for data in batch:
            key = data[self.folder_key]

            fldr = self.name / key
            fldr.mkdir(exist_ok=True, parents=True)

            fi = (fldr / str(data[self.file_key])).with_suffix('.json')
            with open(fi, 'w') as fi:
                fi.write(json.dumps(data))

    def get(self, reference):
        if reference is None:
            fldr = self.name
        else:
            fldr = self.name / reference

        articles = []
        for f in fldr.iterdir():
            if f.is_file():
                with open(f, "r") as fi:
                    articles.append(json.loads(fi.read()))
        return articles




class TextFiles:
    def __init__(self, root=None, logger=None):
        #  root is either raw or final
        if root:
            self.root = Path.home() / db_folder / root
            self.root.mkdir(parents=True, exist_ok=True)
            self.newspapers = {
                folder.name: NewspaperTextFiles(f"{root}/{folder.name}")
                for folder in self.root.iterdir()
                if folder.is_dir()
            }
        else:
            self.root = Path.home() / db_folder
            self.root.mkdir(parents=True, exist_ok=True)

        if logger:
            logger.info(f"init db at {self.root}")

    def get_all_articles(self):
        """searches all newspapers"""
        self.articles = []
        for paper in self.newspapers.keys():
            self.articles.extend(self.newspapers[paper].get_all_articles())
        return self.articles

    def get_article(self, article_id):
        """searches all newspapers"""
        for f in self.root.rglob("**/*.json"):
            if f.is_file() and article_id in f.name:
                with open(f, "r") as fi:
                    article = json.loads(fi.read())
        return article

    def get_articles_from_newspaper(self, paper):
        """all articles from one newspaper"""
        return self.newspapers[paper].get_all_articles()

    def get(self, fi):
        """single file"""
        fi = self.root / fi
        with open(fi, "r") as fp:
            return fp.read()

    def write(self, data, file, mode):
        """single file"""
        #  needs to be a list due to how we add the newline character /n
        if isinstance(data, str):
            data = (data,)
        data = [d + "\n" for d in data]

        fi = self.root / file
        with open(fi, mode) as fp:
            fp.writelines(data)


class NewspaperTextFiles(TextFiles):
    def __init__(self, root=None):
        super().__init__(root=root)

    def get_all_articles(self):
        #  todo precompute this list on init
        articles = []
        for f in self.root.iterdir():
            if f.is_file():
                with open(f, "r") as fi:
                    articles.append(json.loads(fi.read()))
        return articles

    def check(self, article_id):
        articles = self.get_all_articles()
        article_ids = set([a["article_id"] for a in articles])
        if article_id in article_ids:
            return True
        return False


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


class SQLiteDatabase(AbstractDB):
    def __init__(self, table, schema, db='climatedb.sqlite'):
        self.table = table
        names, schema = format_schema(schema)
        self.record = namedtuple(table, names)
        self.schema = schema

        self.c = sqlite3.connect(db)
        qry = f"CREATE TABLE IF NOT EXISTS {self.table} ({schema});"
        self.c.execute(qry)

    def add(self, batch):
        for data in batch:
            data = tuple(self.record(**data))
            rhs = '(' + ('?,' * (len(data)-1)) + '?)'
            qry = f'INSERT INTO {self.table} VALUES ' + rhs
            print(qry, data)
            self.c.execute(qry, data)
        self.c.commit()

    def get(self, reference=None):
        data = self.c.execute(f'SELECT * FROM {self.table}').fetchall()
        out = []
        for d in data:
            d = self.record(*d)
            out.append(d._asdict())
        return out
