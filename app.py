from random import randint

from flask import Flask, render_template, request, jsonify
import pandas as pd

from climatedb.analytics import create_article_df, groupby_newspaper, groupby_years_and_newspaper
from climatedb.config import DBHOME
from climatedb import services, databases

from climatedb.registry import get_newspaper, registry


app = Flask("climate-news-db")
registry = pd.DataFrame(registry)
registry = registry.set_index("newspaper_id")

# db = databases.ArticlesFolders()
db = databases.ArticlesSQLite()
articles = services.get_all_articles(db)


@app.route("/newspaper")
def show_one_newspaper():
    newspaper_id = request.args.get("newspaper_id")
    articles = services.get_all_articles_from_newspaper(db, newspaper_id)
    articles = pd.DataFrame(articles)
    articles = articles.sort_values('date_published', ascending=False)
    articles = articles.reset_index(drop=True)
    articles = articles.to_dict(orient="records")
    newspaper = get_newspaper(newspaper_id)
    return render_template("newspaper.html", newspaper=newspaper, articles=articles)


@app.route("/article")
def show_one_article():
    article_id = request.args.get("article_id")
    article = services.get_article_from_article_id(db, article_id)
    return render_template("article.html", article=article)


@app.route("/papers.json")
def paper_json():
    """groupby paper, calculate statistics"""
    articles = services.get_all_articles(db)

    df = create_article_df(articles)
    group = groupby_newspaper(df)
    group = group.set_index("newspaper_id")

    papers = pd.concat([group, registry], axis=1)
    papers.loc[:, "newspaper_id"] = papers.index
    papers = papers.sort_index()
    papers = papers.reset_index(drop=True)
    papers = papers.fillna(0)
    return papers.to_dict(orient="records")


@app.route("/years.json")
def year_json():
    """groupby paper and by year"""
    articles = services.get_all_articles(db)
    df = create_article_df(articles)
    return groupby_years_and_newspaper(df)


@app.route("/year-chart")
def year_chart():
    return render_template('year_chart.html')


def get_latest_articles(articles, key='date_uploaded', num=8):
    articles = services.get_all_articles(db)
    df = create_article_df(articles)
    df = df.sort_values(key, ascending=False)
    return df.head(num).to_dict(orient="records")


@app.route("/")
def home():
    papers = paper_json()

    data = {
        "n_articles": len(articles),
        "articles": articles,
        "n_papers": len(papers)
    }
    return render_template(
        "home.html",
        data=data,
        papers=papers,
    )


@app.route("/latest")
def latest():
    df = create_article_df(articles)
    latest = get_latest_articles(articles, 'date_published')
    scrape = get_latest_articles(articles, 'date_uploaded')
    return render_template(
        "latest.html", latest=latest, scrape=scrape
    )


@app.route("/random")
def show_random_article():
    idx = randint(0, len(articles) - 1)
    article = articles[idx]
    return render_template("article.html", article=article)


@app.route("/logs")
def show_logs():
    toggle = request.args.get("toggle")
    if toggle is None:
        toggle = 'error'

    from climatedb.logger import load_logs
    logs = load_logs()
    if toggle == 'error':
       logs = [l for l in logs if 'error' in l['msg']]

    logs = logs
    logs = pd.DataFrame(logs)
    logs = logs.sort_values('time', ascending=False)
    logs = logs.to_dict(orient="records")
    return render_template("logs.html", logs=logs, toggle=toggle)

from datetime import datetime
@app.template_filter('datetimeformat')
def datetimeformat(value, fmt='%Y-%m-%d'):
    dt = str(value).replace('Z', '')
    return datetime.fromisoformat(dt).strftime(fmt)



if __name__ == "__main__":
    app.run(debug=True)
