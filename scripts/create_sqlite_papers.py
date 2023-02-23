from datetime import datetime
from pathlib import Path
from typing import Optional

from rich import print
from sqlalchemy import func, select
from sqlalchemy.dialects.sqlite import insert
from sqlmodel import Field, Session, SQLModel, create_engine

from climatedb.config import data_home as home
from climatedb.config import db_uri
from climatedb.databases import (
    AppTable,
    Article,
    Newspaper,
    find_all_articles,
    find_all_papers,
    find_id_for_newspaper,
)
from climatedb.files import JSONFile, JSONLines

engine = create_engine(db_uri)
SQLModel.metadata.create_all(engine)


def add_papers():
    raw_papers = JSONFile(Path(home) / "newspapers.json").read()
    papers = [Newspaper(**p) for p in raw_papers.values()]
    with Session(engine) as session:
        for p in papers:
            session.add(p)
        session.commit()

    print(f"added {len(papers)} newspapers to {db_uri}")
    return raw_papers

def main():
    #  think this is important!
    add_papers()


if __name__ == "__main__":
    main()
