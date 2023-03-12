import sys
from pathlib import Path

from rich import print
from sqlalchemy.dialects.sqlite import insert
from sqlmodel import Session, SQLModel, create_engine

from climatedb.config import data_home as home
from climatedb.config import db_uri
from climatedb.databases import Article, find_id_for_newspaper
from climatedb.files import JSONLines

engine = create_engine(db_uri)
SQLModel.metadata.create_all(engine)


def add_articles(newspaper):
    articles = JSONLines(Path(home) / f"articles/{newspaper}.jsonlines").read()
    articles = [
        Article(**a, newspaper_id=find_id_for_newspaper(newspaper)) for a in articles
    ]

    with Session(engine) as session:
        count = 0
        for art in articles:
            try:
                st = insert(Article).values(art.dict())
                session.execute(st)
                count += 1
            except Exception as err:
                print(err)
            session.commit()
    print(f"added {count} from {len(articles)} articles to {db_uri} for {newspaper}")


def main():
    paper = sys.argv[1]
    add_articles(paper)


if __name__ == "__main__":
    main()
