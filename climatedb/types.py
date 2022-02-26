from datetime import datetime

import pydantic
from pydantic import BaseModel


class ArticleModel(BaseModel):
    body: str
    title: str
    article_url: str
    article_id: str
    date_published: datetime


class PaperModel(BaseModel):
    newspaper_id: str
    newspaper: str
    newspaper_url: str
