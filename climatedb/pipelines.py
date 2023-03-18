# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pathlib

import scrapy
import sqlmodel
from rich import print
from sqlmodel.pool import StaticPool

from climatedb import files
from climatedb.crawl import find_newspaper_from_url
from climatedb.models import ArticleItem, ArticleMeta, ArticleTable


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
            datetime_crawled=item.datetime_crawled,
        )


class InsertArticle:
    def __init__(self, db_uri: str) -> None:
        self.db_uri = db_uri
        self.engine = sqlmodel.create_engine(
            db_uri,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        ArticleTable.metadata.create_all(self.engine)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings["DB_URI"])

    def open_spider(self, spider):
        self.session = sqlmodel.Session(self.engine)

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item: ArticleMeta, spider):
        print(f" Insert Article {item.headline} to {self.db_uri}")
        article = ArticleTable(
            headline=item.headline,
            body=item.body,
            date_published=item.date_published,
            article_name=item.article_name,
            article_url=item.article_url,
            datetime_crawled=item.datetime_crawled,
            article_length=len(item.body),
        )
        self.session.add(article)
        self.session.commit()

        return article
