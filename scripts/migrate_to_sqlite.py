from climatedb.databases import ArticlesSQLite, ArticlesFolders


def add_articles_to_sqlite():
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

    json_db = ArticlesFolders()
    sql_db = ArticlesSQLite()

    json_articles = json_db.get()
    print(len(json_articles))
    sql_db.add(json_articles)


if __name__ == '__main__':
    add_articles_to_sqlite()
