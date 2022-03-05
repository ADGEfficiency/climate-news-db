from climatedb.config import data_home as home
from climatedb.config import db_uri
from datetime import datetime
from fastapi.templating import Jinja2Templates
from pathlib import Path
from pydantic import constr
from rich import print
from sqlalchemy import select
from sqlmodel import Field, Session, SQLModel, create_engine
from typing import List
from typing import Optional
import json
import pandas as pd


def get_urls_for_paper(paper: str) -> List[str]:
    """
    Gets all urls for a newspaper from $(DATA_HOME) / urls.csv
    """
    raw = pd.read_csv(f"{home}/urls.csv")
    mask = raw["name"] == paper
    data = raw[mask]
    urls = data["url"].values.tolist()

    #  here we can filter out what we already have
    existing = home / "articles" / f"{paper}.jsonlines"
    if existing.is_file():
        jl = JSONLines(existing)
        existing = jl.read()
        existing = [a["article_url"] for a in existing]

        #  last one is '' - TODO do this properly
        dispatch = set(urls).difference(set(existing))
    else:
        dispatch = urls
        existing = []

    print(
        f"{paper}, all_urls {raw.shape[0]}, urls {len(urls)}, existing {len(existing)}, dispatch {len(dispatch)}"
    )

    return list(dispatch)


class JSONLines:
    def __init__(self, path):
        self.path = Path(path)

    def read(self):
        data = self.path.read_text().split("\n")[:-1]
        return [json.loads(a) for a in data]
        return data


class JSONFile:
    def __init__(self, path):
        self.path = Path(path)

    def read(self):
        return json.loads(self.path.read_text())


#  sqlite stuff


engine = create_engine(db_uri)
SQLModel.metadata.create_all(engine)


def save_html(paper, article, response):
    """used by spiders"""
    fi = (
        Path.home() / "climate-news-db" / "data-reworked" / "articles" / paper / article
    )
    fi.parent.mkdir(exist_ok=True, parents=True)
    fi.with_suffix(".html").write_bytes(response.body)


class Newspaper(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    fancy_name: str
    newspaper_url: str
    color: str

    article_count: Optional[int]
    average_article_length: Optional[int]


from sqlalchemy import UniqueConstraint


class Article(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("article_name"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    body: constr(min_length=64)
    headline: constr(min_length=8)
    article_name: constr(min_length=4)
    article_url: str
    date_published: Optional[datetime]
    date_uploaded: datetime
    newspaper_id: int

    article_length: int


class AppTable(SQLModel, table=True):
    #  article
    body: constr(min_length=64)
    headline: str
    article_id: int = Field(primary_key=True)
    article_url: str
    date_published: Optional[datetime]
    date_uploaded: datetime
    #  newspaper
    newspaper_id: int
    fancy_name: str


def find_id_for_newspaper(newspaper: str):
    with Session(engine) as s:
        st = select(Newspaper.id).where(Newspaper.name == newspaper)
        return s.exec(st).first()[0]


def find_all_articles():
    """used by app"""
    with Session(engine) as s:
        st = select(Article)
        return s.exec(st).fetchall()


def find_all_papers():
    """used by app"""
    with Session(engine) as s:
        st = select(Newspaper)
        data = s.exec(st).fetchall()

        papers = []
        for paper in data:
            paper = paper[0]
            if paper.article_count is None:
                paper.article_count = 0
            if paper.average_article_length is None:
                paper.average_article_length = 0

            papers.append(paper)

        return papers


def find_article(article_id: int):
    """used by app"""
    with Session(engine) as s:
        st = select(AppTable).where(AppTable.article_id == article_id)
        return s.exec(st).first()[0]


def find_random_article():
    """used by app"""
    from sqlalchemy.sql.expression import func, select

    with Session(engine) as s:
        st = select(AppTable).order_by(func.random())
        return s.exec(st).first()[0]


def find_articles_by_newspaper(newspaper_id):
    """used by app"""

    with Session(engine) as s:
        st = (
            select(AppTable)
            .where(AppTable.newspaper_id == newspaper_id)
            .order_by(AppTable.date_published.desc())
        )
        articles = s.exec(st).all()
        articles = [a[0] for a in articles]

    with Session(engine) as s:
        st = select(Newspaper).where(Newspaper.id == newspaper_id)
        newspaper = s.exec(st).first()[0]

    return articles, newspaper
