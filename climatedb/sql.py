

class SQLiteDatabase():
    def __init(self):
        pass

    def get(self, table):
        #  return entire table
        pass

    def write(self, data, file, mode):
        #  what can data be
        #  file can also be table
        #  mode won't be needed (just check for if file exists)
        pass

    #  then you have the newspaper stuff
    #  get_all_articles() etc



from collections import namedtuple

URL = namedtuple('article_url', 'article_url, search_time_UTC')

if __name__ == '__main__':
    import sqlite3
    db = SQLiteDatabase()
    c = sqlite3.connect(':memory:')

    with open('urls-schema.sql') as fp:
        c.executescript(fp.read())

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


