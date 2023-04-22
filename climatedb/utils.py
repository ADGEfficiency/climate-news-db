import pathlib
from climatedb import files, models


def read_newspapers_json(base:str=".") -> list[models.Newspaper]:
    path = pathlib.Path(base) / "newspapers.json"
    newspapers = files.JSONFile(path).read()
    return [models.Newspaper(**p) for p in newspapers]
