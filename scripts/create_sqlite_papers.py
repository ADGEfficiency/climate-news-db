from pathlib import Path

from rich import print
from sqlmodel import Session, SQLModel, create_engine

from climatedb.config import data_home as home
from climatedb.config import db_uri
from climatedb.databases import Newspaper
from climatedb.files import JSONFile

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
    add_papers()


if __name__ == "__main__":
    main()
