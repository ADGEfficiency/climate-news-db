import dataclasses
import datetime
import typing

import sqlmodel
from sqlalchemy import String
from sqlalchemy.sql.schema import Column


@dataclasses.dataclass
class RawURL:
    """Maps to urls.jsonl"""

    url: str
    search_time_utc: str


@dataclasses.dataclass
class RejectedURL:
    """Maps to rejected.jsonl"""

    article_url: str
    article_start_url: str
    datetime_rejected_utc: str


@dataclasses.dataclass
class ArticleMeta:
    """Maps to articles/{newspaper}.jsonl"""

    headline: str
    body: str
    date_published: typing.Optional[datetime.date]
    article_name: str
    article_url: str
    article_start_url: str
    datetime_crawled_utc: datetime.datetime = datetime.datetime.now()

    def __repr__(self) -> str:
        return f"ArticleMeta(headline={self.headline}, article_name: {self.article_name}, date_published: {self.date_published})"


@dataclasses.dataclass(kw_only=True)
class ArticleItem(ArticleMeta):
    html: str

    def __repr__(self) -> str:
        return f"ArticleItem(headline={self.headline}, article_name: {self.article_name}, date_published: {self.date_published})"


@dataclasses.dataclass
class NewspaperMeta:
    """Maps to newspaper.json"""

    name: str
    fancy_name: str
    site: str
    color: str


class Newspaper(sqlmodel.SQLModel, table=True):
    __tablename__ = "newspaper"

    id: typing.Optional[int] = sqlmodel.Field(default=None, primary_key=True)

    #  from newspaper.json
    name: str = sqlmodel.Field(sa_column=Column("name", String, unique=True))
    fancy_name: str
    site: str
    color: str

    #  aggregated statistics from Newspaper
    article_count: int = 0
    average_article_length: float = 0

    #  one newspaper can have many articles
    articles: list["Article"] = sqlmodel.Relationship(back_populates="newspaper")


class Article(sqlmodel.SQLModel, table=True):
    __tablename__ = "article"

    id: typing.Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    headline: str = sqlmodel.Field()
    body: str = sqlmodel.Field()
    date_published: typing.Optional[datetime.date] = sqlmodel.Field(default=None)
    article_name: str = sqlmodel.Field(
        sa_column=Column("article_name", String, unique=True)
    )

    article_url: str = sqlmodel.Field()
    datetime_crawled_utc: datetime.datetime = sqlmodel.Field()
    article_length: int

    newspaper_id: int = sqlmodel.Field(foreign_key="newspaper.id")
    newspaper: Newspaper = sqlmodel.Relationship(back_populates="articles")


class GPTOpinion(sqlmodel.SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: typing.Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    message: dict = sqlmodel.Field(
        default_factory=dict, sa_column=Column(sqlmodel.JSON)
    )
    request: dict = sqlmodel.Field(
        default_factory=dict, sa_column=Column(sqlmodel.JSON)
    )
    response: dict = sqlmodel.Field(
        default_factory=dict, sa_column=Column(sqlmodel.JSON)
    )
    article_id: int = sqlmodel.Field(foreign_key="article.id")

    class Config:
        arbitrary_types_allowed = True
