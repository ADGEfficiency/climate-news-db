import asyncio
import datetime
import json
import os
import random
import typing

import aiohttp
import pydantic
import requests
from rich import print
from scrapy.settings import Settings

from climatedb import database, files
from climatedb.crawl import find_newspaper_from_url
from climatedb.database import read_newspaper
from climatedb.models import Article, GPTOpinion

settings = Settings()
settings.setmodule("climatedb.settings")


class Message(pydantic.BaseModel):
    role: typing.Literal["user", "system", "assistant"]
    content: str


class ChatRequest(pydantic.BaseModel):
    messages: list[Message]
    model: typing.Literal["gpt-3.5-turbo"] = "gpt-3.5-turbo"
    temperature: float = 0.0
    max_tokens: int = 1028
    request_time_utc: str = datetime.datetime.now().isoformat()


def get_chat_request(article_body: str) -> ChatRequest:
    return ChatRequest(
        messages=[
            Message(
                role="system",
                content='You are evaluating the content of a newspaper article on climate change on two things.  I want you to evaluate the article on a numeric, continuous scale of 0 to 1.0, and give a natural language explanation.  First is the accuracy of the article compared with the current scientific understanding of climate change. 1 would be very accurate, 0 would be inaccurate, 0.5 would be mixed.  Second is the an evaluation of how positive or negative the tone of the article is with regards to climate change.  1 would be very positive, 0 would be very negative, 0.5 would be mixed. For both you should be estimating an expected value across all the available data, population or samples available.  If you cannot evaluate either numeric-score, you should return -1. In addition to the two evaluations, you should return the topics of the article as a list of strings.  You should return a JSON string of the form `{"scientific-accuracy": {"numeric-score": 1.0, "explanation": "some explanation"}, "article-tone": {"numeric-score": 1.0, "explanation": "some explanation"}, "topics": ["topic1", "topic2"]}`. Keep explanations short. Return a JSON decodable string.',
            ),
            Message(role="user", content=f"Evaluate this article: {article_body}"),
        ]
    )


async def request_gpt_chat_async(article_body: str) -> typing.Optional[tuple]:
    print(f" [green]request_gpt_chat_async[/], article_body: {article_body[:100]}")
    max_characetrs = 4096 * 4
    article_body = article_body[: int(max_characetrs)]
    request = get_chat_request(article_body)

    await asyncio.sleep(random.random() * 3)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
                },
                json=request.dict(exclude={"request_time_utc": True}),
            ) as response:
                print(f"Request status: {response.status}")
                pkg = await response.json()
                print(pkg, flush=True)
                return request, response

        except Exception as e:
            print(f"Error in request_gpt_chat_async: {e}")
    return None


def request_gpt_chat(article_body: str) -> tuple:
    max_characetrs = 4096 * 4
    article_body = article_body[: int(max_characetrs)]

    request = get_chat_request(article_body)
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        },
        json=request.dict(exclude={"request_time_utc": True}),
    )
    print(response.json())
    assert response.ok
    return request, response


async def call_open_ai(
    article: Article,
    opinion_fi: files.JSONFile,
    request_fn: typing.Callable = request_gpt_chat,
) -> None:
    try:
        request, response = await request_fn(article.body)
        pkg = await response.json()
        choices = pkg["choices"]

        assert len(choices) == 1
        message = choices[0]["message"]["content"]
        message = json.loads(message)

        gpt_opinion = GPTOpinion(
            request=request.dict(),
            response=pkg,
            message=message,
            article_id=article.id,
            scientific_accuracy=message["scientific-accuracy"]["numeric-score"],
            article_tone=message["article-tone"]["numeric-score"],
            topics=message["topics"],
        )
        opinion_fi.write(gpt_opinion.dict())
        database.write_opinion(settings["DB_URI"], gpt_opinion)

    except Exception as e:
        reject_fi = files.JSONLines("./data/rejected-gpt.jsonl")
        reject_fi.write([{**article.dict()}])
        print(f" {article.article_url} failed {e}", flush=True)


async def regenerate(opinion_fi: files.JSONFile, article: Article) -> None:
    print(f" [blue]regenerating[/] {article.article_name}")
    existing = opinion_fi.read()

    if "article_id" not in existing:
        print(f" nothing saved: {existing.keys()}")
        return

    existing['article_id'] = article.id
    assert article.id == existing["article_id"]

    gpt_opinion = GPTOpinion(**existing)

    settings = Settings()
    settings.setmodule("climatedb.settings")
    database.write_opinion(settings["DB_URI"], gpt_opinion)
    print(f" [blue]regenerated[/] {article.article_name}")


async def process_articles(articles: typing.List[Article]) -> None:
    tasks = []
    for article in articles:
        paper_meta = find_newspaper_from_url(article.article_url)
        paper = read_newspaper(paper_meta.name)

        #  id won't be stable across different databases#
        #  does that matter - don't think so?
        assert article.id is not None
        opinion = database.read_opinion(article.id)
        opinion_fi = files.JSONFile(
            f"./data/opinions/{paper.name}/{article.article_name}"
        )
        if opinion_fi.exists():
            print(
                f" [blue]regenerate[/], article: {article.article_name}, id: {article.id}"
            )
            tasks.append(regenerate(opinion_fi, article))

        elif opinion is None:
            print(
                f" [green]call_open_ai[/], article: {article.article_name}, id: {article.id}"
            )
            tasks.append(
                call_open_ai(
                    article=article,
                    opinion_fi=opinion_fi,
                    request_fn=request_gpt_chat_async,
                )
            )
        else:
            print(
                f" [yellow]skipping[/], article: {article.article_name}, id: {article.id}"
            )

    await asyncio.gather(*tasks)


async def main() -> None:
    limit = 10
    articles = database.read_all_articles()
    random.shuffle(articles)

    for chunk in chunks(articles, limit):
        await process_articles(chunk)


def chunks(lst: list, n: int) -> typing.Any:
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


if __name__ == "__main__":
    asyncio.run(main())
