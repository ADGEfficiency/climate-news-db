from flask import Flask

from database import TextFiles


app = Flask('climate-article-downloader')

db = TextFiles('final')


@app.route('/')
def home():
    articles = db.get_all_articles()

    data = {
        'n_articles': len(articles),
        'articles': articles
    }

    return data



if __name__ == '__main__':
    app.run(debug=True)
