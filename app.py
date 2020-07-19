from random import randint

from flask import Flask, render_template, request
import pandas as pd

from analytics import create_article_df, groupby_newspaper
from database import TextFiles
from newspapers.registry import get_newspaper, registry


app = Flask("climate-article-downloader")
db = TextFiles("final")
papers = [folder.name for folder in db.root.iterdir() if folder.is_dir()]
all_articles = []
for paper in papers:
    db = TextFiles(f"final/{paper}")
    all_articles.extend(db.get_all_articles())

registry = pd.DataFrame(registry)
registry = registry.set_index("newspaper_id")


@app.route("/")
def home():
    data = {"n_articles": len(all_articles), "articles": all_articles}

    df = create_article_df(all_articles)
    group = groupby_newspaper(df)
    group = group.set_index("newspaper_id")
    papers = group.to_dict(orient="records")

    papers = pd.concat([group, registry], axis=1)
    papers = papers.dropna(axis=0)
    papers.loc[:, "newspaper_id"] = papers.index
    papers = papers.reset_index(drop=True)
    papers = papers.to_dict(orient="records")

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

    db = TextFiles(f"final/{newspaper}")
    articles = db.get_all_articles()
    newspaper = get_newspaper(newspaper)

    return render_template("newspaper.html", newspaper=newspaper, articles=articles)


if __name__ == "__main__":
    app.run(debug=True)
