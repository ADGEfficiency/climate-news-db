from climatedb.spiders.guardian import JSONLines
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Table, DateTime, MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
import numpy as np
import pandas as pd

from sqlalchemy.orm import sessionmaker

import os

from config import data_home as home
from config import db_uri

meta = MetaData()

articles_table = Table(
    "articles",
    meta,
    Column("id", Integer, primary_key=True),
    Column("body", String),
    Column("title", String),
    Column("article_id", String, unique=True),
    Column("article_url", String),
    Column("date_published", DateTime),
    Column("newspaper_id", String),
)
engine = create_engine(db_uri, connect_args={"check_same_thread": False})
Session = sessionmaker(engine)

if __name__ == "__main__":
    meta.create_all(engine)

    jl = JSONLines(home / "articles/guardian.jsonlines").read()

    articles = pd.DataFrame(jl)
    articles["date_published"] = pd.to_datetime(articles["date_published"])
    articles["date_published"] = [d.to_pydatetime() for d in articles["date_published"]]

    # article = ArticleTable(**article)
    articles["newspaper_id"] = "guardian"

    #  really want to join on newspapers here eh
    #  will need to make that table first
    #  maybe create a table called app for the app only

    with Session() as s:
        for row in range(articles.shape[0]):
            article = articles.iloc[row].to_dict()
            # engine.execute(articles_table.insert.on_conflict_do_nothing(), **article)

            from sqlalchemy.dialects.sqlite import insert

            #  st = statement
            st = insert(articles_table).values(**article)
            st = st.on_conflict_do_nothing()
            engine.execute(st)
