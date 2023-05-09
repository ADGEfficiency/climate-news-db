import random
import typing

import sqlmodel
from rich import print
from scrapy.settings import Settings
from sqlalchemy import func
from sqlalchemy.dialects.sqlite import insert

from climatedb import files
from climatedb.models import Article, GPTOpinion, Newspaper

settings = Settings()
settings.setmodule("climatedb.settings")


def get_random_article_id(db_uri: str = settings["DB_URI"]) -> int:
    engine = sqlmodel.create_engine(db_uri)
    with sqlmodel.Session(engine) as session:
        low, high = session.query(func.min(Article.id), func.max(Article.id)).one()
        return random.randint(low, high)


def read_all_articles(db_uri: str = settings["DB_URI"]) -> list[Article]:
    engine = sqlmodel.create_engine(db_uri)
    with sqlmodel.Session(engine) as session:
        return session.query(Article).order_by(Article.date_published.desc()).all()


def read_articles(
    newspaper: Newspaper, db_uri: str = settings["DB_URI"]
) -> list[Article]:
    engine = sqlmodel.create_engine(db_uri)
    with sqlmodel.Session(engine) as session:
        statement = sqlmodel.select(Article).where(Article.newspaper_id == newspaper.id)
        return session.exec(statement).all()


def read_all_newspapers(db_uri: str = settings["DB_URI"]) -> list[Newspaper]:
    engine = sqlmodel.create_engine(db_uri)
    with sqlmodel.Session(engine) as session:
        return session.query(Newspaper).order_by(Newspaper.name).all()


def read_article(article_id: int, db_uri: str = settings["DB_URI"]) -> Article:
    engine = sqlmodel.create_engine(db_uri)
    with sqlmodel.Session(engine) as session:
        return session.query(Article).where(Article.id == article_id).one()


def read_newspaper_by_id(
    newspaper_id: int, db_uri: str = settings["DB_URI"]
) -> list[Newspaper]:
    engine = sqlmodel.create_engine(db_uri)
    with sqlmodel.Session(engine) as session:
        return session.query(Newspaper).where(Newspaper.id == newspaper_id).one()


def read_newspaper(newspaper_name: str, db_uri: str = settings["DB_URI"]) -> Newspaper:
    engine = sqlmodel.create_engine(db_uri)
    with sqlmodel.Session(engine) as session:
        return session.exec(
            sqlmodel.select(Newspaper).where(Newspaper.name == newspaper_name)
        ).one()


def read_opinion(
    article_id: int, db_uri: str = settings["DB_URI"]
) -> typing.Optional[GPTOpinion]:
    engine = sqlmodel.create_engine(db_uri)
    GPTOpinion.metadata.create_all(engine)
    with sqlmodel.Session(engine) as session:
        return session.exec(
            sqlmodel.select(GPTOpinion).where(GPTOpinion.article_id == article_id)
        ).one_or_none()


def write_article(db_uri: str, article: Article) -> None:
    engine = sqlmodel.create_engine(db_uri)
    with sqlmodel.Session(engine) as session:
        stmt = (
            insert(Article)
            .values(**article.dict())
            .on_conflict_do_update(
                index_elements=[Article.article_name],
                set_={
                    "headline": article.headline,
                    "body": article.body,
                    "date_published": article.date_published,
                    "article_url": article.article_url,
                    "datetime_crawled_utc": article.datetime_crawled_utc,
                    "article_length": article.article_length,
                },
            )
        )
        session.execute(stmt)
        session.commit()


def write_opinion(db_uri, opinion) -> None:
    engine = sqlmodel.create_engine(db_uri)
    GPTOpinion.metadata.create_all(engine)

    with sqlmodel.Session(engine) as session:
        session.add(opinion)
        session.commit()


def seed_newspapers(db_uri: str) -> None:
    newspapers = files.JSONFile("./newspapers.json").read()
    engine = sqlmodel.create_engine(db_uri)

    print(f"seeding newspapers to {db_uri}")

    Newspaper.metadata.create_all(engine)
    for paper in newspapers:
        paper = Newspaper(**paper)
        print(f" inserting {paper}")
        with sqlmodel.Session(engine) as session:
            stmt = (
                insert(Newspaper)
                .values(**paper.dict())
                .on_conflict_do_update(
                    index_elements=[Newspaper.name],
                    set_={
                        "fancy_name": paper.fancy_name,
                        "site": paper.site,
                        "color": paper.color,
                    },
                )
            )
            session.execute(stmt)
            session.commit()


def create_newspaper_statistics(db_uri: str) -> dict:
    engine = sqlmodel.create_engine(db_uri)
    with sqlmodel.Session(engine) as session:
        data = (
            session.query(
                Newspaper.name,
                Newspaper.fancy_name,
                func.count(Article.id).label("num_articles"),
                func.avg(Article.article_length).label("article_length"),
            )
            .join(Newspaper.articles)
            .group_by(Newspaper.name)
            .order_by(Newspaper.name)
            .all()
        )
        pkg = []
        for name, fancy_name, num_articles, article_length in data:
            pkg.append(
                {
                    "name": name,
                    "fancy_name": fancy_name,
                    "article_count": num_articles,
                    "average_article_length": article_length,
                }
            )

    return pkg


def get_articles_with_opinions(
    newspaper: Newspaper, db_uri: str = settings["DB_URI"]
) -> list:
    engine = sqlmodel.create_engine(db_uri)

    with sqlmodel.Session(engine) as session:
        statement = (
            sqlmodel.select(Article, GPTOpinion)
            .join(GPTOpinion, isouter=True)
            .where(Article.newspaper_id == newspaper.id)
            .order_by(Article.date_published.desc())
        )
        data = session.exec(statement)

        results = []
        for article, opinion in data:
            results.append(
                {
                    "id": article.id,
                    "headline": article.headline,
                    "body": article.body,
                    "date_published": article.date_published,
                    "article_name": article.article_name,
                    "article_url": article.article_url,
                    "datetime_crawled_utc": article.datetime_crawled_utc,
                    "article_length": article.article_length,
                    "newspaper_name": article.newspaper.name,
                    "scientific_accuracy_score": opinion.scientific_accuracy
                    if opinion
                    else None,
                    "article_tone_score": opinion.article_tone if opinion else None,
                }
            )

        return results


def get_all_articles_with_opinions(
    db_uri: str = settings["DB_URI"], n: int = 32
) -> list:
    engine = sqlmodel.create_engine(db_uri)
    from sqlalchemy import text
    with sqlmodel.Session(engine) as session:
        statement = (
            sqlmodel.select(Article, GPTOpinion)
            .join(GPTOpinion)
            # .order_by(sqlmodel.sql.func.random())
            .order_by(text("RANDOM()"))
            .limit(n)
        )
        data = session.exec(statement)

        results = []
        for article, opinion in data:
            results.append(
                {
                    "id": article.id,
                    "headline": article.headline,
                    "body": article.body,
                    "date_published": article.date_published,
                    "article_name": article.article_name,
                    "article_url": article.article_url,
                    "datetime_crawled_utc": article.datetime_crawled_utc,
                    "article_length": article.article_length,
                    "newspaper_name": article.newspaper.name,
                    "fancy_newspaper_name": article.newspaper.fancy_name,
                    "scientific_accuracy_score": opinion.scientific_accuracy,
                    "article_tone_score": opinion.article_tone,
                    "topics": opinion.topics,
                }
            )

        return results


def get_latest(db_uri: str = settings["DB_URI"]) -> list:
    engine = sqlmodel.create_engine(db_uri)
    with sqlmodel.Session(engine) as session:
        query = (
            session.query(Article, Newspaper)
            .join(Newspaper)
            .order_by(Article.date_published.desc())
            .limit(12)
        )
        latest_published = query.all()
        latest_published = [
            {
                "date_published": a.date_published,
                "date_uploaded": a.datetime_crawled_utc,
                "headline": a.headline,
                "fancy_name": n.fancy_name,
                "newspaper": n.name,
                "article_id": a.id,
            }
            for a, n in latest_published
        ]

        query = (
            session.query(Article, Newspaper)
            .join(Newspaper)
            .order_by(Article.datetime_crawled_utc.desc())
            .limit(12)
        )
        latest_scraped = query.all()
        latest_scraped = [
            {
                "date_published": a.date_published,
                "date_uploaded": a.datetime_crawled_utc.date(),
                "headline": a.headline,
                "fancy_name": n.fancy_name,
                "newspaper": n.name,
                "article_id": a.id,
            }
            for a, n in latest_scraped
        ]
    return latest_published, latest_scraped
