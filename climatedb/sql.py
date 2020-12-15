from collections import namedtuple

from database import AbstractDB


class SQLiteDatabase(AbstractDB):
    def __init__(self, name, schema):
        self.name = name

    def add(self, reference):
        pass

    def get(self, reference=None):
        if reference is None:
            # get all
            pass

    def write(self, data, file, mode):
        #  what can data be = JSON or TUPLE
        #  file can also be table
        #  mode won't be needed (just check for if file exists)

        record = Newspaper
        if data is dict:
            data = record(**data)


class Newspapers:
    """Business logic"""
    def __init__(self, db, papers):
        self.papers = {}
        for paper in papers:
            self.papers[paper] = db(paper)

    def get_all_articles(self):
        data = []
        for paper, db in self.papers.items():
            data.append(db.get())
        return data


if __name__ == '__main__':
    import sqlite3
    db = SQLiteDatabase('test')
    c = sqlite3.connect(':memory:')

    URL = namedtuple('article_url', 'article_url, search_time_UTC')

    qry = "CREATE TABLE IF NOT EXISTS urls (article_url TEXT, created_at TEXT );"
    c.execute(qry)

    urls = [
        URL('article.html', '2020-01-01T00:00:00'),
        URL('other-article.html', '2020-01-01T00:05:00')
    ]
    for url in urls:
        qry = f'''INSERT INTO urls VALUES {tuple(url)}'''
        c.execute(qry)

    data = c.execute('SELECT * FROM urls').fetchall()
    assert urls == data

    url = {
        'article_url': 'other-article.html',
        'search_time_UTC': '2020-01-01T00:05:00'
    }


    newspaper_schema = [
        ('body', 'TEXT'),
        ('article_url', 'TEXT'),
        ('article_id', 'INT'),
        ('newspaper_id', 'TEXT'),
        ('search_time_UTC', 'TEXT')
    ]

    names = ''
    sql_schema = ''
    for name, dtype in newspaper_schema:
        names += f'{name}, '
        sql_schema += f'{name} {dtype}, '

    names = names.strip(', ')
    sql_schema = sql_schema.strip(', ')
    print(names)
    print(sql_schema)

    Newspaper = namedtuple('newpaper', names)
    newspapers = [Newspaper(**n) for n in newspapers]

    for paper in newspapers:
        newspaper_id = paper.newspaper_id
        qry = f'CREATE TABLE IF NOT EXISTS {newspaper_id} ({sql_schema}) ;'
        c.execute(qry)
        qry = f'INSERT INTO {newspaper_id} VALUES {tuple(paper)}'
        c.execute(qry)

    for paper in newspapers:
        newspaper_id = paper.newspaper_id
        data = c.execute(f'SELECT * FROM {newspaper_id}').fetchall()
        paper = [tuple(paper), ]
        assert paper == data
