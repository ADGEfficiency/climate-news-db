import json
import os
import typing

import pydantic
import requests
import sqlalchemy
import sqlmodel
from scrapy.settings import Settings
from sqlalchemy.sql.schema import Column

from climatedb import crawl, database, files
from climatedb.models import GPTOpinion


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
    articles = database.read_all_articles()
    print(len(articles))

    #  for each article
    for article in articles:
        opinion = database.read_opinion(article)

        if opinion is None:
            print(f" calling openai: {article.article_name}")
            request, response = call_gpt(article.body)
            assert response.ok

            choices = response.json()["choices"]
            assert len(choices) == 1
            message = choices[0]["message"]["content"]
            message = json.loads(message)

            paper_meta = crawl.find_newspaper_from_url(article.article_url)
            paper = database.read_newspaper(paper_meta.name)

            gpt_opinion = GPTOpinion(
                request=request.dict(),
                response=response.json(),
                message=message,
                article_id=article.id,
            )

            settings = Settings()
            settings.setmodule("climatedb.settings")
            database.write_opinion(settings["DB_URI"], gpt_opinion)
        else:
            print(f" not calling openai: {article.article_name}")
