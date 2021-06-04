from climatedb.databases import URLs, Articles

if __name__ == '__main__':

    #  setup urls in sqlite
    url_schema = (
        ('url', 'TEXT'),
        ('search_time_UTC', 'TEXT')
    )

    urls = URLs('urls', engine='sqlite', key='url', schema=url_schema)
    #  get urls from urls.json, put into sqlite db
    data = URLs('urls/urls.jsonl', engine='jsonl').get()
    urls.add(data)

    #  articles
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

    json_db = Articles('articles/final/bbc', engine='json-folder', key='article_id', schema=schema)
    sql_db = Articles('final', engine='sqlite', key='article_id', schema=schema)

    print(f'{len(json_db)} JSON articles')
    json_articles = json_db.get()
    sql_db.add(json_articles)
