"""
Want to:

- render home page
- with all article as list of json
- that come from sqlite
"""

from climatedb.databases_neu import (
    find_all_articles,
    find_article,
    find_random_article,
    find_articles_by_newspaper,
)
from fastapi.staticfiles import StaticFiles

from typing import Optional

from fastapi import FastAPI, Request

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from datetime import datetime


articles = find_all_articles()
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def datetimeformat(value, fmt="%Y-%m-%d"):
    dt = str(value).replace("Z", "")
    return datetime.fromisoformat(dt).strftime(fmt)


templates.env.filters["datetimeformat"] = datetimeformat


@app.get("/")
async def read_root():
    return articles


@app.get("/article/{article_id}", response_class=HTMLResponse)
async def read_article(request: Request, article_id: int):
    """show one article by article id"""
    article = find_article(article_id)
    return templates.TemplateResponse(
        "article.html", {"request": request, "article": article}
    )


@app.get("/random", response_class=HTMLResponse)
async def read_random_article(request: Request):
    """show a random article"""
    article = find_random_article()
    return templates.TemplateResponse(
        "article.html", {"request": request, "article": article}
    )


@app.get("/newspaper/{newspaper_id}", response_class=HTMLResponse)
async def read_newspaper_articles(request: Request, newspaper_id: int):
    """show one article by article id"""
    articles, newspaper = find_articles_by_newspaper(newspaper_id)

    return templates.TemplateResponse(
        "newspaper.html",
        {"request": request, "articles": articles, "newspaper": newspaper},
    )
