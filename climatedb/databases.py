from collections import defaultdict, namedtuple
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import pandas as pd
from fastapi.templating import Jinja2Templates
from rich import print
from sqlalchemy.sql.expression import func, select
from sqlmodel import Session, SQLModel, create_engine

from climatedb import files
from climatedb.config import data_home as home
from climatedb.config import db_uri
from climatedb.files import JSONFile
from climatedb.types import AppTable, Article, Newspaper

assert home is not None


def find_start_url(response):
    #  if we get redirected, use the original url we search for
    url = response.request.headers.get("Referer", None)
    if url is None:
        url = response.url
    else:
        url = url.decode("utf-8")
    return url


def find_newspaper_from_url(url: dict) -> dict:
    """not sure where this should live"""
    papers = JSONFile(Path(home) / "newspapers.json").read()
    for paper in papers.values():
        if paper["newspaper_url"] in url["url"]:
            return {**url, **paper}
    return {"name": "UNKNOWN"}


print(f"database connection: [green]{db_uri}[/]")
engine = create_engine(db_uri)
SQLModel.metadata.create_all(engine)


def find_id_for_newspaper(newspaper: str) -> None:
    """used in creating database"""
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
    """used by app"""
    with Session(engine) as session:
        query = (
            session.query(AppTable).order_by(AppTable.date_published.desc()).limit(12)
        )
        latest = [l[0] for l in session.exec(query).all()]

    with Session(engine) as session:
        query = (
            session.query(AppTable).order_by(AppTable.date_uploaded.desc()).limit(12)
        )
        scrape = [l[0] for l in session.exec(query).all()]

    return latest, scrape


def get_newspaper_colors():
    """helper for group_newspapers_by_year"""
    with Session(engine) as session:
        query = session.query(
            Newspaper.fancy_name,
            Newspaper.color,
        )
        data = session.exec(query).all()
    return data


def find_year_paper(year, paper, data):
    """helper for group_newspapers_by_year"""
    mask = (data["year"] == year) & (data["paper"] == paper)
    if mask.sum() == 1:
        sub = data[mask]
        return int(sub["count"])
    else:
        return 0


def group_newspapers_by_year():
    """used for chart in app"""
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

    out = defaultdict(list)
    years = range(year_start, data["year"].max() + 1)
    for year in years:
        for paper in sorted(list(set(data["paper"]))):
            count = find_year_paper(year, paper, data)
            out[paper].append(count)

    out["years"] = list(years)

    lens = [len(out[k]) for k in out.keys()]
    assert len(set(lens)) == 1
    colors = get_newspaper_colors()
    colors = {t[0]: t[1] for t in colors}
    out["colors"] = colors
    return out


def load_newspapers_json() -> JSONFile:
    """Read `newspapers.json` from the dataset."""
    return JSONFile(Path(home) / "newspapers.json").read()
