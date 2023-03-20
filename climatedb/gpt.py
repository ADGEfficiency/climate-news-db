import os
import typing

import pydantic
import requests
import sqlalchemy
import sqlmodel
from sqlalchemy.sql.schema import Column

from climatedb import crawl, database


class GPTOpinion(sqlmodel.SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: typing.Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    message: dict = sqlmodel.Field(
        default_factory=dict, sa_column=Column(sqlmodel.JSON)
    )
    request: dict = sqlmodel.Field(
        default_factory=dict, sa_column=Column(sqlmodel.JSON)
    )
    response: dict = sqlmodel.Field(
        default_factory=dict, sa_column=Column(sqlmodel.JSON)
    )

    class Config:
        arbitrary_types_allowed = True


class Message(pydantic.BaseModel):
    role: typing.Literal["user", "system", "assistant"]
    content: str


class CompletionRequest(pydantic.BaseModel):
    messages: list[Message]
    model: typing.Literal["gpt-3.5-turbo"] = "gpt-3.5-turbo"
    temperature: float = 0.0


def call_gpt(article_body: str):
    request = CompletionRequest(
        messages=[
            Message(
                role="system",
                content='You are evaluating the content of a newspaper article on climate change.  I want you to evaluate two things.  First is the accuracy of the article compared with the current scientific understanding of climate change. 1 would be very accurate, 0 would be inaccurate.  Second is the an evaluation of how positive or negative the tone of the article is with regards to climate change.  1 would be very positive, 0 would be very negative. For both you should be estimating an expected value across all the available data, population or samples available.  If you cannot evaluate either numeric-score, you should return -1. You should return a JSON string of the form `{"scientific-accuracy": {"numeric-score": 1.0, "explanation": "some explanation" }, "article-tone": {"numeric-score": 1.0, "explanation": "some explanation"}}`.',
            ),
            Message(role="user", content=f"Evaluate this article: {article_body}"),
        ]
    )
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        },
        json=request.dict(),
    )
    print(response.json())
    return request, response


if __name__ == "__main__":
    from climatedb import database

    articles = database.read_all_articles()
    print(len(articles))
    import json

    #  for each article
    for article in articles:
        """
        where to do the cache
        - cache the file
        - cache in database
        """
        request, response = call_gpt(article.body)
        assert response.ok

        from climatedb import files

        print("make request")
        choices = response.json()["choices"]
        assert len(choices) == 1
        message = choices[0]["message"]["content"]
        message = json.loads(message)

        paper_meta = crawl.find_newspaper_from_url(article.article_url)
        paper = database.read_newspaper(paper_meta.name)

        gpt_opinion = GPTOpinion(
            request=request.dict(), response=response.json(), message=message
        )

        from scrapy.settings import Settings

        settings = Settings()
        settings.setmodule("climatedb.settings")
        database.write_opinion(settings["DB_URI"], gpt_opinion)
