import scrapy
import sqlmodel
from rich import print
from scrapy.settings import Settings
from sqlalchemy.dialects.sqlite import insert
from sqlmodel.pool import StaticPool

from climatedb import files
from climatedb.models import Article, Newspaper, NewspaperMeta

settings = Settings()
settings.setmodule("climatedb.settings")


def read_all_articles(db_uri: str = settings["DB_URI"]) -> list[Article]:
    engine = sqlmodel.create_engine(db_uri)
    with sqlmodel.Session(engine) as session:
        return session.query(Article).all()


def read_newspaper(
    newspaper: NewspaperMeta, db_uri: str = settings["DB_URI"]
) -> Newspaper:
    engine = sqlmodel.create_engine(db_uri)
    with sqlmodel.Session(engine) as session:
        return session.exec(
            sqlmodel.select(Newspaper).where(Newspaper.name == newspaper.name)
        ).one()


def seed():
    #  create the newspapers

    #  todo
    import pathlib

    newspapers = files.JSONFile("./newspapers.json").read()
    data_home = pathlib.Path("./data")

    #  TODO
    engine = sqlmodel.create_engine("sqlite:///data/db.sqlite")

    Newspaper.metadata.create_all(engine)
    for paper in newspapers:
        paper = Newspaper(**paper)
        with sqlmodel.Session(engine) as session:
            stmt = (
                insert(Newspaper)
                .values(**paper.dict())
                .on_conflict_do_update(
                    index_elements=[Newspaper.name],
                    set_={
                        "fancy_name": paper.fancy_name,
                        "newspaper_url": paper.newspaper_url,
                        "color": paper.color,
                    },
                )
            )
            session.execute(stmt)
            session.commit()

    #  create the articles
    Article.metadata.create_all(engine)

    for article in [p for p in (data_home / "articles").iterdir() if p.is_dir()]:
        breakpoint()  # fmt: skip

    #  update the statistics


if __name__ == "__main__":
    seed()
