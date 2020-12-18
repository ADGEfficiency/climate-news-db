from datetime import datetime

from climatedb.databases import *


if __name__ == '__main__':
    #  convert old urls.data file to urls.jsonl

    with open(DBHOME / 'urls.data', 'r') as fi:
        data = fi.readlines()
        data = [d.strip('\n') for d in data][:100]

    print(f'read {len(data)} from urls.data')
    data = [{'url': d, 'search_time_UTC': datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S')} for d in data]

    urls = URLs('urls.jsonl', engine='jsonl', key='url')
    urls.add(data)
    print(f'wrote {len(urls)} to urls.jsonl')

    #  setup urls in sqlite

    url_schema = (
        ('url', 'TEXT'),
        ('search_time_UTC', 'TEXT')
    )

    urls = URLs('urls', engine='sqlite', key='url', schema=url_schema)
    urls.add(data)

    #  articles
    schema = [
        ("newspaper", "TEXT"),
        ("newspaper_id", "TEXT"),
        ("newspaper_url", "TEXT"),
        ("body", "TEXT"),
        ("headline", "TEXT"),
        ("html", "TEXT"),
        ("article_url", "TEXT"),
        ("article_id", "TEXT"),
        ("date_published", "TEXT"),
        ("date_uploaded", "TEXT"),
    ]

    #  need to process the json article schema here


    json_db = Articles('final/bbc', engine='json-folder', key='article_id', schema=schema)

    sql_db = Articles('final', engine='sqlite', key='article_id', schema=schema)

    print(f'{len(json_db)} JSON articles')
    json_articles = json_db.get()

    sql_db.add(json_articles)


