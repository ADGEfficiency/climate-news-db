from typing import *
from datetime import datetime
from typing import Optional

from pydantic import constr
from sqlmodel import SQLModel, Field
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


class Newspaper(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    fancy_name: str
    newspaper_url: str
    color: str

    article_count: Optional[int]
    average_article_length: Optional[int]
