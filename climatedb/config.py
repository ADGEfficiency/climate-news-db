import dataclasses
import pathlib


@dataclasses.dataclass
class Config:
    home: pathlib.Path = pathlib.Path("data")
    db_uri: str = "sqlite:///data/db.sqlite"
