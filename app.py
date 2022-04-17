import os
from datetime import datetime
from typing import Optional

from fastapi.staticfiles import StaticFiles
import uvicorn

from fastapi.responses import FileResponse
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

from climatedb.config import data_home
from climatedb.databases import (
    find_all_articles,
    find_all_papers,
    find_article,
    find_random_article,
    find_articles_by_newspaper,
    load_latest,
    group_newspapers_by_year,
)


articles = find_all_articles()
papers = find_all_papers()
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def datetimeformat(value, fmt="%Y-%m-%d"):
    try:
        dt = str(value).replace("Z", "")
        return datetime.fromisoformat(dt).strftime(fmt)
    except:
        return ""


templates.env.filters["datetimeformat"] = datetimeformat


@app.get("/")
async def read_root(request: Request):
    data = {"n_articles": len(articles), "articles": articles, "n_papers": len(papers)}
    return templates.TemplateResponse(
        "home.html", {"request": request, "data": data, "papers": papers}
    )


@app.get("/article/{article_id}", response_class=HTMLResponse)
async def read_article(request: Request, article_id: int):
    """show one article by article id"""
    article = find_article(article_id)
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


@app.get("/random", response_class=HTMLResponse)
async def read_random_article(request: Request):
    """show a random article"""
    article = find_random_article()
    return templates.TemplateResponse(
        "article.html", {"request": request, "article": article}
    )


@app.get("/latest", response_class=HTMLResponse)
async def read_latest(request: Request):
    """show the latest articles"""

    latest, scrape = load_latest()
    return templates.TemplateResponse(
        "latest.html", {"request": request, "latest": latest, "scrape": scrape}
    )


@app.get("/download", response_class=HTMLResponse)
def download(request: Request):
    return FileResponse(
        path=f"{data_home}/climate-news-db-dataset.zip",
        filename="climate-new-db-dataset.zip",
        media_type="zip",
    )


@app.get("/years.json")
def years_json(request: Request):
    """used by JS.charts on home page"""
    data = group_newspapers_by_year()
    return JSONResponse(content=data)


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
