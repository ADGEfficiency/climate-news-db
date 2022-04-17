from collections import namedtuple, defaultdict
from sqlalchemy import UniqueConstraint
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
import pandas as pd

from climatedb import types
from climatedb.files import JSONLines
from sqlalchemy.sql.expression import func, select

from climatedb.types import Newspaper


def get_urls_for_paper(paper: str) -> List[str]:
    """
    Gets all urls for a newspaper from $(DATA_HOME) / urls.csv
    """
    raw = pd.read_csv(f"{home}/urls.csv")
    mask = raw["name"] == paper
    data = raw[mask]
    urls = data["url"].values.tolist()

    #  here we can filter out what we already have
    existing = Path(home) / "articles" / f"{paper}.jsonlines"
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


#  sqlite stuff


print(f"database connection: [green]{db_uri}[/]")
engine = create_engine(db_uri)
SQLModel.metadata.create_all(engine)


def save_html(paper, article, response):
    """used by spiders"""
    fi = (
        Path.home() / "climate-news-db" / "data-reworked" / "articles" / paper / article
    )
    fi.parent.mkdir(exist_ok=True, parents=True)
    fi.with_suffix(".html").write_bytes(response.body)


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
        articles = s.exec(st).fetchall()
        return [a[0] for a in articles]


def read_app_table():
    """used by inspect"""
    with Session(engine) as s:
        st = select(AppTable)
        articles = s.exec(st).fetchall()
        return [a[0] for a in articles]


def find_all_papers():
    """used by app"""
    with Session(engine) as s:
        st = select(Newspaper).order_by(Newspaper.fancy_name)
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


def get_newspaper_colors():
    with Session(engine) as session:
        query = session.query(
            Newspaper.fancy_name,
            Newspaper.color,
        )
        data = session.exec(query).all()
    return data


def group_newspapers_by_year():
    with Session(engine) as session:
        query = (
            session.query(
                func.strftime("%Y", Article.date_published),
                func.count(Article.id),
                Newspaper.fancy_name,
            )
            .join(Newspaper, Article.newspaper_id == Newspaper.id)
            .group_by(func.strftime("%Y", Article.date_published), Article.newspaper_id)
        )

    raw = session.exec(query).all()

    year_start = 2010
    data = []
    for row in raw:
        if row[0] is not None:
            if int(row[0]) >= year_start:
                data.append(
                    {
                        "year": int(row[0]),
                        "count": int(row[1]),
                        "paper": row[2],
                    }
                )
    data = pd.DataFrame(data)
    print(data.head(3))

    def find_year_paper(year, paper, data):
        mask = (data["year"] == year) & (data["paper"] == paper)
        if mask.sum() == 1:
            sub = data[mask]
            return int(sub["count"])
        else:
            return 0

    out = defaultdict(list)
    years = range(year_start, data["year"].max() + 1)
    for year in years:
        for paper in list(set(data["paper"])):
            count = find_year_paper(year, paper, data)
            out[paper].append(count)

    out["years"] = list(years)
    # years = set(new_data["year"])

    # for row in range(new_data.shape[0]):
    #     row = new_data.iloc[row, :]
    #     out[row["name"]].append(int(row["count"]))

    # out = dict(out)
    # out["years"] = list(range(min(years), max(years) + 1))
    lens = [len(out[k]) for k in out.keys()]
    assert len(set(lens)) == 1
    colors = get_newspaper_colors()
    colors = {t[0]: t[1] for t in colors}
    out["colors"] = colors
    return out


"""
{'The Guardian': [1, 1, 3, 8, 2, 6, 8, 18, 30, 19, 29, 32, 56, 88, 281, 198, 13], 'The Economist': [3, 2, 2, 3, 3, 3, 9, 6, 14, 5, 9, 9, 15, 5, 10, 16, 60, 55, 44, 7], 'Deutsche Welle': [1, 2, 1, 1, 2, 1, 1, 5, 3, 9, 9, 27, 39, 53, 36, 46, 1], 'The New York Times': [2, 1, 2, 5, 5, 1, 7, 3, 17, 17, 19, 24, 31, 87, 164, 166, 27], 'Al Jazeera': [2, 1, 2, 3, 6, 12, 16, 18, 14, 13, 15, 105, 88, 153, 11], 'The BBC': [1, 3, 7, 10, 4, 7, 43, 102, 151, 165, 26], 'NewsHub.co.nz': [1, 6, 14, 11, 27, 115, 86, 74, 13], 'CNN': [18, 6, 20, 36, 108, 104, 146, 8], 'Stuff.co.nz': [5, 4, 2, 29, 109, 262, 171, 31], 'Sky News Australia': [15, 166, 169, 166, 18], 'years': [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]}
"""
