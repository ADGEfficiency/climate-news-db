import sqlmodel
from scrapy.settings import Settings

from climatedb.models import ArticleTable

settings = Settings()
settings.setmodule("climatedb.settings")


def read_all_articles(db_uri: str = settings["DB_URI"]) -> list[ArticleTable]:
    engine = sqlmodel.create_engine(db_uri)
    with sqlmodel.Session(engine) as session:
        return session.query(ArticleTable).all()
