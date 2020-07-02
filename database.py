from pathlib import Path
import json


class TextFiles:
    def __init__(self, root=None):
        if root:
            self.root = Path.home() / 'climate-nlp' / root
        else:
            self.root = Path.home() / 'climate-nlp'
        self.root.mkdir(parents=True, exist_ok=True)

    def get(self, fi):
        # single file
        fi = self.root / fi
        with open(fi, 'r') as fp:
            return fp.read()

    def write(self, data, file, mode):

        #  needs to be a list due to how we add the newline character /n
        if isinstance(data, str):
            data = (data, )
        data = [d + '\n' for d in data]

        fi = self.root / file
        with open(fi, mode) as fp:
            fp.writelines(data)

    def get_all_articles(self):
        articles = []
        for f in self.root.iterdir():
            if f.is_file():
                with open(f, 'r') as fi:
                    articles.append(json.loads(fi.read()))
        return articles

    def get_article(self, article_id):
        fi = self.root / (article_id + '.json')
        with open(fi, 'r') as fi:
            article = json.loads(fi.read())

        return article

    def get_articles_from_newspaper(self, newspaper):
        articles = self.get_all_articles()
        articles = [a for a in articles if a['newspaper_id'] == newspaper]
        return articles



if __name__ == '__main__':
    db = TextFiles('final')
    art = db.get_all_articles()
