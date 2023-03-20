import fastapi
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
        {"request": request, "data": data},
    )


@app.get("/charts")
async def charts(request: fastapi.Request):
    return templates.TemplateResponse(
        "charts.html",
        {
            "request": request,
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
