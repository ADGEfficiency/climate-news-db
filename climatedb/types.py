from typing import *

from sqlmodel import SQLModel, Field


class Newspaper(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    fancy_name: str
    newspaper_url: str
    color: str

    article_count: Optional[int]
    average_article_length: Optional[int]
