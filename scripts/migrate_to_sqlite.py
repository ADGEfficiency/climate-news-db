from datetime import datetime
from climatedb.databases import ArticlesSQLite, ArticlesFolders


def add_articles_to_sqlite():
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

    articles = json_db.get()

    print(len(articles))
    #  remove articles from early times (1970 year)
    for article in articles[1:]:
        dt = datetime.fromisoformat(
            article['date_published'][:19]
        )
        if dt.year < 1980:
            articles.remove(article)

    print(len(articles))

    sql_db.add(articles)
    # csv_db.add(articles)


if __name__ == '__main__':
    add_articles_to_sqlite()
