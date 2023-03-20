# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pathlib
import typing

import scrapy
import sqlmodel
from rich import print
from sqlalchemy.dialects.sqlite import insert
from sqlmodel.pool import StaticPool

from climatedb import files
from climatedb.crawl import find_newspaper_from_url
from climatedb.database import read_newspaper
from climatedb.models import Article, ArticleItem, ArticleMeta


class SaveHTML:
    def process_item(self, item: ArticleItem, spider: scrapy.Spider) -> ArticleMeta:
        paper = find_newspaper_from_url(item.article_url)
        data_home = pathlib.Path(spider.settings["DATA_HOME"])
        fi = files.HTMLFile(data_home / "html" / paper.name / item.article_name)
        fi.write(item.html)
        return ArticleMeta(
            headline=item.headline,
            body=item.body,
            date_published=item.date_published,
            article_name=item.article_name,
            article_url=item.article_url,
            article_start_url=item.article_start_url,
            datetime_crawled_utc=item.datetime_crawled_utc,
        )


class InsertArticle:
    def __init__(self, db_uri: str, data_home: typing.Union[pathlib.Path, str]) -> None:
        self.db_uri = db_uri

        #  shouldnt need really - comes from the integration test
        #  where we pass DATA_HOME as a CLI setting
        data_home = pathlib.Path(data_home)
        data_home.mkdir(exist_ok=True, parents=True)
        print(f" [green]connecting[/] to {db_uri}")
        self.engine = sqlmodel.create_engine(
            db_uri,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Article.metadata.create_all(self.engine)

    @classmethod
    def from_crawler(cls, crawler: scrapy.crawler.Crawler) -> scrapy.crawler.Crawler:
        return cls(crawler.settings["DB_URI"], crawler.settings["DATA_HOME"])

    def open_spider(self, spider: scrapy.Spider) -> None:
        self.session = sqlmodel.Session(self.engine)

    def close_spider(self, spider: scrapy.Spider) -> None:
        self.session.close()

    def process_item(self, item: ArticleMeta, spider: scrapy.Spider) -> ArticleMeta:
        print(
            f" [green]insert article[/]\n headline: {item.headline}\n db_uri: {self.db_uri}"
        )

        #  first need to find the appropriate newspaper
        paper_meta = find_newspaper_from_url(item.article_url)
        paper = read_newspaper(newspaper=paper_meta)

        article = Article(
            headline=item.headline,
            body=item.body,
            date_published=item.date_published,
            article_name=item.article_name,
            article_url=item.article_url,
            datetime_crawled_utc=item.datetime_crawled_utc,
            article_length=len(item.body),
            newspaper=paper,
            newspaper_id=paper.id,
        )
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
        self.session.execute(stmt)
        self.session.commit()
        return item
