import pathlib

from climatedb import files, models
from climatedb.models import Newspaper


def read_newspapers_json(base: str = ".") -> list[models.Newspaper]:
    path = pathlib.Path(base) / "newspapers.json"
    newspapers = files.JSONFile(path).read()
    return [models.Newspaper(**p) for p in newspapers]


def get_one_newspaper(name: str) -> dict[str, Newspaper]:
    paper: list[Newspaper] = [n for n in read_newspapers_json() if n.name == name]
    assert len(paper) == 1
    return paper[0]
