import fastapi
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from scrapy.settings import Settings

from climatedb import database

app = fastapi.FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


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
    data = {"n_articles": 0, "n_papers": 0}
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "data": data,
            "papers": [
                {
                    "name": "guardian",
                    "fancy_name": "Guardian",
                    "article_count": 100,
                    "average_article_length": 100,
                }
            ],
        },
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
    articles = database.get_articles_with_opinions(settings["DB_URI"])
    newspaper = database.read_newspaper(newspaper)
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
    settings = Settings()
    settings.setmodule("climatedb.settings")

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


@app.get("/newspaper-by-year.json")
def years_json():
    data = {
        "years": [2010, 2011],
        "datasets": [
            {
                "label": "Guardian",
                "backgroundColor": "#FA9000",
                "data": [100, 200],
            },
            {
                "label": "NY Times",
                "backgroundColor": "#000000",
                "data": [100, 200],
            },
        ],
        "colors": {
            "guardian": "#FA9000",
        },
    }

    return fastapi.responses.JSONResponse(content=data)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80, reload=True)
