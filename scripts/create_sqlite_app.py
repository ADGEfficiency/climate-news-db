from sqlalchemy import func
from sqlmodel import Session, SQLModel, create_engine

from climatedb.config import db_uri
from climatedb.databases import AppTable, Article, Newspaper

engine = create_engine(db_uri)
SQLModel.metadata.create_all(engine)


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
            (
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


def main():
    add_app_table()


if __name__ == "__main__":
    main()
