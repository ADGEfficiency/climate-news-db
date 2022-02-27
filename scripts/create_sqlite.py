from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine
from sqlalchemy import select

from rich import print

from climatedb.databases_neu import (
    JSONLines,
    JSONFile,
    Newspaper,
    Article,
    AppTable,
    find_id_for_newspaper,
)
from config import data_home as home
from config import db_uri

from datetime import datetime

engine = create_engine(db_uri)
SQLModel.metadata.create_all(engine)


def add_papers():
    raw_papers = JSONFile(home / "newspapers.json").read()
    papers = [Newspaper(**p) for p in raw_papers.values()]
    with Session(engine) as session:
        for p in papers:
            session.add(p)
        session.commit()

    print(f"added {len(papers)} newspapers to {db_uri}")
    return raw_papers


def add_articles(newspaper):
    articles = JSONLines(home / f"articles/{newspaper}.jsonlines").read()
    articles = [
        Article(**a, newspaper_id=find_id_for_newspaper(newspaper)) for a in articles
    ]
    from sqlalchemy.dialects.sqlite import insert

    with Session(engine) as session:
        for art in articles:
            #  huge TODO - should be able to ignore in the add
            # session.add(art)
            try:
                session.execute(
                    insert(Article).values(art.dict()).on_conflict_do_nothing()
                )
                session.commit()
            except Exception as err:
                pass

    print(f"added {len(articles)} articles to {db_uri} for {newspaper}")


def add_app_table():
    with Session(engine) as session:
        query = session.query(Article, Newspaper).join(
            Newspaper, Article.newspaper_id == Newspaper.id
        )
        data = session.exec(query).all()

    with Session(engine) as session:
        for d in data:
            art, new = d
            ap = AppTable(
                body=art.body,
                headline=art.headline,
                article_id=art.id,
                article_url=art.article_url,
                date_published=art.date_published,
                newspaper_id=new.id,
                fancy_name=new.fancy_name,
            )
            session.add(ap)
        session.commit()


if __name__ == "__main__":
    papers = add_papers()
    for paper in papers.keys():
        try:
            add_articles(paper)
        except FileNotFoundError:
            pass
    add_app_table()
