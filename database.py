from pathlib import Path
import json


class TextFiles:
    def __init__(self, root):
        self.root = Path.home() / 'climate-nlp' / root
        self.root.mkdir(parents=True, exist_ok=True)

    def post(self, data, fi):
        fi = self.root / fi
        with open(fi, 'w') as fp:
            fp.write(data)

    # interface

    def get_all_articles(self):
        articles = []
        for f in self.root.iterdir():
            if f.is_file():
                with open(f, 'r') as fi:
                    articles.append(json.loads(fi.read()))
        return articles


if __name__ == '__main__':
    #  dev
    db = TextFiles('final')
    art = db.get_all_articles()

