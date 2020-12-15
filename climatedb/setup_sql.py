from datetime import datetime

from climatedb.database import File, SQLiteDatabase

if __name__ == '__main__':
    fi = File('urls.data')
    data = fi.get(0)

    data = [{'url': d, 'search_time_UTC': datetime.now()} for d in data]

    db = SQLiteDatabase('urls', (('url', 'TEXT'), ('search_time_UTC', 'TEXT')))
    db.add(data)
