from flask import Flask, render_template, request

from database import TextFiles


app = Flask('climate-article-downloader')

db = TextFiles('final')
from analytics import create_article_df, groupby_newspaper

@app.route('/')
def home():
    articles = db.get_all_articles()
    data = {'n_articles': len(articles), 'articles': articles}

    df = create_article_df(articles)
    group = groupby_newspaper(df)
    papers = group.to_dict(orient='records')

    return render_template('home.html', data=data, papers=papers)


@app.route('/random')
def show_random_article():
    articles = db.get_all_articles()
    from random import randint
    idx = randint(0, len(articles))
    article = articles[idx]
    return render_template('article.html', article=article)


@app.route('/article')
def show_one_article():
    article_id = request.args.get('article-id')
    article = db.get_article(article_id)
    return render_template('article.html', article=article)



if __name__ == '__main__':
    app.run(debug=True)
