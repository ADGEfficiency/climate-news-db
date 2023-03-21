import fastapi
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from scrapy.settings import Settings

from climatedb import database

app = fastapi.FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


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
def newspaper(request: fastapi.Request):
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
    articles = database.read_all_articles(settings["DB_URI"])

    newspaper = {"fancy_name": "Guardian"}
    return templates.TemplateResponse(
        "newspaper.html",
        {"request": request, "articles": articles, "newspaper": newspaper},
    )


@app.get("/article/{id}")
def article(request: fastapi.Request):
    settings = Settings()
    settings.setmodule("climatedb.settings")

    # articles = database.read_all_articles(settings["DB_URI"])
    article = {
        "newspaper_name": "guardian",
        "newspaper_fancy_name": "Guardian",
        "date_published": "2020-01-01",
        "article_url": "https://www.theguardian.com/environment/2020/jan/01/australia-bushfires-heatwave-temperatures",
        "body": "hello",
    }

    return templates.TemplateResponse(
        "article.html",
        {"request": request, "article": article},
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
