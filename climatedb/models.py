# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import dataclasses
import datetime
import typing

import sqlmodel
from sqlalchemy import String
from sqlalchemy.sql.schema import Column


@dataclasses.dataclass
class RawURL:
    url: str
    search_time_utc: str


@dataclasses.dataclass
class RejectedURL:
    article_url: str
    article_start_url: str
    datetime_rejected_utc: str


@dataclasses.dataclass
class ArticleMeta:
    headline: str
    body: str
    date_published: typing.Optional[datetime.date]
    article_name: str
    article_url: str
    article_start_url: str
    datetime_crawled_utc: datetime.datetime = datetime.datetime.now()

    def __repr__(self) -> str:
        return f"NewspaperArticleMeta(headline={self.headline}, article_name: {self.article_name}, date_published: {self.date_published})"


@dataclasses.dataclass(kw_only=True)
class ArticleItem(ArticleMeta):
    html: str


class ArticleTable(sqlmodel.SQLModel, table=True):
    __tablename__ = "article"

    id: typing.Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    headline: str = sqlmodel.Field()
    body: str = sqlmodel.Field()
    date_published: typing.Optional[datetime.date] = sqlmodel.Field(default=None)
    article_name: str = sqlmodel.Field(
        sa_column=Column("article_name", String, unique=True)
    )

    article_url: str = sqlmodel.Field()
    datetime_crawled: datetime.datetime = sqlmodel.Field()
    article_length: int


@dataclasses.dataclass
class NewspaperMeta:
    name: str
    fancy_name: str
    newspaper_url: str
    color: str
