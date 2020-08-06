from random import randint

from flask import Flask, render_template, request, jsonify
import pandas as pd

from analytics import create_article_df, groupby_newspaper, groupby_years_and_newspaper
from database import TextFiles
from newspapers.registry import get_newspaper, registry


app = Flask("climate-article-downloader")
db = TextFiles("final")
all_articles = db.get_all_articles()

registry = pd.DataFrame(registry)
registry = registry.set_index("newspaper_id")


@app.route("/papers.json")
def paper_json():
    """groupby paper, calculate statistics"""
    df = create_article_df(all_articles)
    group = groupby_newspaper(df)
    group = group.set_index("newspaper_id")
    papers = group.to_dict(orient="records")

    #  passing in the parse & check functions here!
    papers = pd.concat([group, registry], axis=1)
    papers = papers.dropna(axis=0)
    papers.loc[:, "newspaper_id"] = papers.index
    papers = papers.sort_index()
    papers = papers.reset_index(drop=True)
    return papers.to_dict(orient="records")


@app.route("/years.json")
def year_json():
    """groupby paper and by year"""
    df = create_article_df(all_articles)
    return groupby_years_and_newspaper(df)

    return {
        'years': [2011, 2012, 2013],
        'nytimes': [11, 12, 13],
        'guardian': [11, 12, 13],
    }


@app.route("/year-chart")
def year_chart():
    return render_template('year_chart.html')


@app.route("/")
def home():
    data = {"n_articles": len(all_articles), "articles": all_articles}
    papers = paper_json()
    return render_template("home.html", data=data, papers=papers)


@app.route("/random")
def show_random_article():
    #  this loads entire json
    #  better to load single one by index
    # articles = db.get_all_articles()

    idx = randint(0, len(all_articles) - 1)
    article = all_articles[idx]
    return render_template("article.html", article=article)


@app.route("/article")
def show_one_article():
    article_id = request.args.get("article_id")
    db = TextFiles("final")
    article = db.get_article(article_id)
    return render_template("article.html", article=article)


@app.route("/newspaper")
def show_one_newspaper():
    newspaper = request.args.get("newspaper_id")

    articles = db.get_articles_from_newspaper(newspaper)
    articles = pd.DataFrame(articles)
    articles = articles.sort_values('date_published', ascending=False)
    articles = articles.reset_index(drop=True)
    articles = articles.to_dict(orient="records")

    newspaper = get_newspaper(newspaper)

    return render_template("newspaper.html", newspaper=newspaper, articles=articles)


if __name__ == "__main__":
    app.run(debug=True)
