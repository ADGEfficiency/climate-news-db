from flask import Flask, render_template, request, jsonify

app = Flask("climate-news-db")

from climatedb.spiders.guardian import JSONLines
from config import data_home as home

import numpy as np
import pandas as pd

jl = JSONLines(home / "articles/guardian.jsonlines").read()
articles = pd.DataFrame(jl)


@app.route("/")
def home():
    return "hi"


@app.route("/article")
def show_one_article():
    article_id = request.args.get("article_id")
    article = articles.iloc[0, :].to_dict()
    return render_template("article.html", article=article)


from datetime import datetime


@app.template_filter("datetimeformat")
def datetimeformat(value, fmt="%Y-%m-%d"):
    dt = str(value).replace("Z", "")
    return datetime.fromisoformat(dt).strftime(fmt)


if __name__ == "__main__":
    app.run(debug=True)
