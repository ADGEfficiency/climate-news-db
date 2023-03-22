import datetime
import json
import os
import typing

import pydantic
import requests
import sqlalchemy
import sqlmodel
from rich import print
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
    max_tokens: int = 1028
    request_time_utc: str = datetime.datetime.now().isoformat()


def call_gpt(article_body: str):
    max_characetrs = 4096 * 4
    article_body = article_body[: int(max_characetrs)]

    request = CompletionRequest(
        messages=[
            Message(
                role="system",
                content='You are evaluating the content of a newspaper article on climate change.  I want you to evaluate two things on a numeric, continuous scale of 0 to 1.0.  First is the accuracy of the article compared with the current scientific understanding of climate change. 1 would be very accurate, 0 would be inaccurate, 0.5 would be mixed.  Second is the an evaluation of how positive or negative the tone of the article is with regards to climate change.  1 would be very positive, 0 would be very negative, 0.5 would be mixed. For both you should be estimating an expected value across all the available data, population or samples available.  If you cannot evaluate either numeric-score, you should return -1. You should return a JSON string of the form `{"scientific-accuracy": {"numeric-score": 1.0, "explanation": "some explanation"}, "article-tone": {"numeric-score": 1.0, "explanation": "some explanation"}}`.  Keep the explanations short.',
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
        json=request.dict(exclude={"request_time_utc": True}),
    )
    print(response.json())
    return request, response


if __name__ == "__main__":
    articles = database.read_all_articles()
    print(len(articles))

    #  for each article
    for article in articles:
        #  TODO - should actually read by NAME here
        #  id won't be stable across different databases

        #  with this approach i throw away the result if i lose the database
        #  should save to json and re-seed later
        opinion = database.read_opinion(article.id)

        opinion_fi = files.JSONFile(f"./data/opinions/{article.article_name}")

        if opinion is None:
            print(
                f" [green]calling[/] openai: article: {article.article_name} id: {article.id}"
            )
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
                scientific_accuracy=message["scientific-accuracy"]["numeric-score"],
                article_tone=message["article-tone"]["numeric-score"],
            )

            settings = Settings()
            settings.setmodule("climatedb.settings")
            database.write_opinion(settings["DB_URI"], gpt_opinion)
            opinion_fi.write(gpt_opinion.json())

        else:
            print(f" not calling openai: {article.article_name}")

        breakpoint()  # fmt: skip
