from datetime import datetime
from typing import Optional

from rich import print
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert
from sqlmodel import Field, Session, SQLModel, create_engine
from pathlib import Path
from climatedb.files import (
    JSONLines,
    JSONFile,
)
from climatedb.databases import (
    Newspaper,
    Article,
    AppTable,
    find_id_for_newspaper,
    find_all_articles,
    find_all_papers,
)
from climatedb.config import data_home as home
from climatedb.config import db_uri


engine = create_engine(db_uri)
SQLModel.metadata.create_all(engine)


def add_papers():
    raw_papers = JSONFile(Path(home) / "newspapers.json").read()
    papers = [Newspaper(**p) for p in raw_papers.values()]
    with Session(engine) as session:
        for p in papers:
            session.add(p)
        session.commit()

    print(f"added {len(papers)} newspapers to {db_uri}")
    return raw_papers


def add_articles(newspaper):
    articles = JSONLines(Path(home) / f"articles/{newspaper}.jsonlines").read()
    articles = [
        Article(**a, newspaper_id=find_id_for_newspaper(newspaper)) for a in articles
    ]

    with Session(engine) as session:
        count = 0
        for art in articles:
            try:
                st = insert(Article).values(art.dict())
                session.execute(st)
                count += 1
            except Exception as err:
                print(err)
            session.commit()
    print(f"added {count} from {len(articles)} articles to {db_uri} for {newspaper}")


def add_app_table():

    #  group articles by newspaper
    with Session(engine) as session:
        query = session.query(
            Article.newspaper_id,
            func.count(Article.newspaper_id),
            func.avg(Article.article_length),
        ).group_by(Article.newspaper_id)
        #  id, count, avg length
        statistics = session.exec(query).all()

    #  update the newspaper table with these statistics
    with Session(engine) as session:
        for stats in statistics:
            st = (
                session.query(Newspaper)
                .filter(Newspaper.id == stats[0])
                .update(
                    {
                        "article_count": stats[1],
                        "average_article_length": stats[2],
                    }
                )
            )
        session.commit()

    #  add article and newspaper to apptable
    with Session(engine) as session:
        query = session.query(Article, Newspaper).join(
            Newspaper, Article.newspaper_id == Newspaper.id
        )
        data = session.exec(query).all()

    with Session(engine) as session:
        for d in data:
            art, pap = d
            ap = AppTable(
                body=art.body,
                headline=art.headline,
                article_id=art.id,
                article_url=art.article_url,
                date_published=art.date_published,
                date_uploaded=art.date_uploaded,
                newspaper_id=pap.id,
                fancy_name=pap.fancy_name,
            )
            session.add(ap)
        session.commit()


def load_latest():
    with Session(engine) as session:
        query = (
            session.query(AppTable).order_by(AppTable.date_published.desc()).limit(5)
        )
        latest = [l[0] for l in session.exec(query).all()]

    with Session(engine) as session:
        query = session.query(AppTable).order_by(AppTable.date_uploaded.desc()).limit(5)
        scrape = [l[0] for l in session.exec(query).all()]

    return latest, scrape


if __name__ == "__main__":
    papers = add_papers()

    for paper in papers.keys():
        try:
            add_articles(paper)
        except FileNotFoundError:
            print(f"no JSONLines for {paper}")

    add_app_table()
