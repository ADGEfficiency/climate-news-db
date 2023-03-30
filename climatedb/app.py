import fastapi
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from scrapy.settings import Settings

from climatedb import database

app = fastapi.FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
settings = Settings()
settings.setmodule("climatedb.settings")


def get_opinion_web(opinion_message: str):
    opinion_web = []
    for key in ["scientific-accuracy", "article-tone"]:
        data = opinion_message[key]
        opinion_web.append(
            {
                "name": key.replace("-", " ").title(),
                "score": data["numeric-score"],
                "width": data["numeric-score"] * 100,
                "message": data["explanation"],
            }
        )
    return opinion_web


def datetimeformat(value, fmt="%Y-%m-%d"):
    try:
        dt = str(value).replace("Z", "")
        return datetime.fromisoformat(dt).strftime(fmt)
    except:
        return ""


def comma_number(x):
    return "{0:,.0f}".format(x)


templates.env.filters["datetimeformat"] = datetimeformat
templates.env.filters["comma_number"] = comma_number


@app.get("/")
async def home(request: fastapi.Request):
    settings = Settings()
    settings.setmodule("climatedb.settings")
    papers = database.create_newspaper_statistics(settings["DB_URI"])
    data = {
        "n_articles": sum([p["article_count"] for p in papers]),
        "n_papers": len(papers),
    }
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "data": data, "papers": papers},
    )


@app.get("/newspaper/{newspaper}")
def newspaper(request: fastapi.Request, newspaper: str):
    articles = [
        {
            "date_published": "2020-01-01",
            "article_id": 0,
            "headline": "headline",
            "body": "body",
        }
    ]

    settings = Settings()
    settings.setmodule("climatedb.settings")
    newspaper = database.read_newspaper(newspaper)
    articles = database.get_articles_with_opinions(newspaper, settings["DB_URI"])
    opinions = {
        "average_article_accuracy": 0.5,
        "average_article_tone": 0.5,
    }

    return templates.TemplateResponse(
        "newspaper.html",
        {
            "request": request,
            "articles": articles,
            "newspaper": newspaper,
            "opinions": opinions,
        },
    )


@app.get("/article/{id}")
def article(request: fastapi.Request, id: int):
    article = database.read_article(id, settings["DB_URI"])
    opinion = database.read_opinion(id, settings["DB_URI"])

    if opinion:
        prompt = opinion.request["messages"][0]["content"]
        opinion_web = get_opinion_web(opinion.message)
    else:
        prompt = None
        opinion_web = None
    newspaper = database.read_newspaper_by_id(article.newspaper_id, settings["DB_URI"])

    return templates.TemplateResponse(
        "article.html",
        {
            "request": request,
            "article": article,
            "newspaper": newspaper,
            "opinions": opinion_web,
            "prompt": prompt,
        },
    )


@app.get("/random")
def random():
    id = database.get_random_article_id(settings["DB_URI"])
    return fastapi.responses.RedirectResponse(url=f"/article/{id}")


@app.get("/latest")
async def read_latest(request: fastapi.Request):
    """show the latest articles"""
    latest_published, latest_scraped = database.get_latest(settings["DB_URI"])
    return templates.TemplateResponse(
        "latest.html",
        {"request": request, "latest": latest_published, "scrape": latest_scraped},
    )


@app.get("/newspaper-by-year.json")
def years_json():
    from climatedb import charts

    home_chart_data = charts.get_home_chart(settings["DB_URI"])
    return fastapi.responses.JSONResponse(content=home_chart_data)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80, reload=True)
