import sqlmodel
from scrapy.settings import Settings
from sqlalchemy import func

from climatedb.models import Article, Newspaper

settings = Settings()
settings.setmodule("climatedb.settings")
import datetime


def get_home_chart(db_uri: str = settings["DB_URI"]):
    engine = sqlmodel.create_engine(db_uri)

    now = datetime.datetime.now()
    min_datetime = datetime.date(now.year - 9, 1, 1)

    with sqlmodel.Session(engine) as session:
        stmt = sqlmodel.select(Newspaper.fancy_name, Newspaper.color)
        newspapers = session.exec(stmt).all()

        stmt = (
            session.query(
                func.extract("year", Article.date_published).label("year"),
                Newspaper.fancy_name.label("newspaper_name"),
                func.count(Article.id).label("article_count"),
            )
            .join(Newspaper, Article.newspaper_id == Newspaper.id)
            .filter(Article.date_published >= min_datetime)
            .group_by("year", "newspaper_name")
            .subquery()
        )

        # Retrieve the grouped data
        rows = session.query(
            stmt.c.year, stmt.c.newspaper_name, stmt.c.article_count
        ).all()

    import numpy as np

    years = np.arange(min_datetime.year, now.year + 1)
    assert len(years) == 10
    newspapers = {
        name: {
            "backgroundColor": color + "80",
            "borderColor": color,
            "borderWidth": 1,
            "label": name,
            "data": np.zeros(10, dtype=int).tolist(),
        }
        for name, color in newspapers
    }
    for year, newspaper, count in rows:
        newspapers[newspaper]["data"][year - min_datetime.year] = count

    breakpoint()  # fmt: skip
    return {
        "years": years.tolist(),
        "datasets": sorted(newspapers.values(), key=lambda x: x["label"]),
    }


if __name__ == "__main__":
    get_home_chart()
