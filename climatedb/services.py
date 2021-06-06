def get_all_articles(db):
    return db.get()


def get_article_from_article_id(db, article_id):
    articles = db.filter(
        key='article_id', value=article_id
    )
    assert len(articles) == 1
    return articles[0]


def get_all_articles_from_newspaper(db, newspaper_id):
    return db.filter(
        key='newspaper_id', value=newspaper_id
    )
