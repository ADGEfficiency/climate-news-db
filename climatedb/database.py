import pathlib
import typing

import sqlmodel
from rich import print
from scrapy.settings import Settings
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import joinedload

from climatedb import files
from climatedb.models import Article, GPTOpinion, Newspaper, NewspaperMeta

settings = Settings()
settings.setmodule("climatedb.settings")


def read_all_articles(db_uri: str = settings["DB_URI"]) -> list[Article]:
    engine = sqlmodel.create_engine(db_uri)
    with sqlmodel.Session(engine) as session:
        return session.query(Article).order_by(Article.date_published.desc()).all()


def read_article(article_id: int, db_uri: str = settings["DB_URI"]) -> list[Article]:
    engine = sqlmodel.create_engine(db_uri)
    with sqlmodel.Session(engine) as session:
        return session.query(Article).where(Article.id == article_id).one()


def read_newspaper_by_id(
    newspaper_id: int, db_uri: str = settings["DB_URI"]
) -> list[Newspaper]:
    engine = sqlmodel.create_engine(db_uri)
    with sqlmodel.Session(engine) as session:
        return session.query(Newspaper).where(Newspaper.id == newspaper_id).one()


def read_opinion(article_id: int, db_uri: str = settings["DB_URI"]) -> GPTOpinion:
    engine = sqlmodel.create_engine(db_uri)
    with sqlmodel.Session(engine) as session:
        return (
            session.query(GPTOpinion)
            .where(GPTOpinion.article_id == article_id)
            .one_or_none()
        )


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
    with sqlmodel.Session(engine) as session:
        return session.exec(
            sqlmodel.select(GPTOpinion).where(GPTOpinion.article_id == article_id)
        ).one_or_none()


def write_opinion(db_uri, opinion) -> None:
    engine = sqlmodel.create_engine(db_uri)

    GPTOpinion.metadata.create_all(engine)

    with sqlmodel.Session(engine) as session:
        session.add(opinion)
        session.commit()


def seed(db_uri: str, data_home: pathlib.Path) -> None:
    newspapers = files.JSONFile("./newspapers.json").read()
    engine = sqlmodel.create_engine(db_uri)

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

    # #  create the articles ??? not sure
    # Article.metadata.create_all(engine)

    # for article in [p for p in (data_home / "articles").iterdir() if p.is_dir()]:
    #     breakpoint()  # fmt: skip

    # #  update the statistics


def get_articles_with_opinions(db_uri: str = settings["DB_URI"]) -> list:
    engine = sqlmodel.create_engine(db_uri)

    with sqlmodel.Session(engine) as session:
        query = (
            session.query(Article, GPTOpinion)
            .outerjoin(GPTOpinion, Article.id == GPTOpinion.article_id)
            .options(joinedload(Article.newspaper))
        )

        results = []
        for article, opinion in query.all():
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
                    # "opinion_message": opinion.message if opinion else None,
                    "scientific_accuracy_score": opinion.scientific_accuracy
                    if opinion
                    else None,
                    "article_tone_score": opinion.article_tone if opinion else None,
                }
            )

        return results


if __name__ == "__main__":
    settings = Settings()
    settings.setmodule("climatedb.settings")
    seed(settings["DB_URI"], settings["DATA_HOME"])
    print("seed done")
