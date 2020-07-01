from pathlib import Path
import json


class TextFiles:
    def __init__(self, root=None):
        if root:
            self.root = Path.home() / 'climate-nlp' / root
        else:
            self.root = Path.home() / 'climate-nlp'
        self.root.mkdir(parents=True, exist_ok=True)

    def post(self, data, fi):
        fi = self.root / fi
        with open(fi, 'w') as fp:
            fp.write(data)

    def append(self, data, fi):

        #  needs to be a list due to how we add the newline character /n
        if isinstance(data, str):
            data = (data, )
        data = [d + '\n' for d in data]

        #  default append, write if file doesn't exist
        fi = self.root / fi
        mode = 'a'
        if not fi.is_file():
            mode = 'w'

        with open(fi, mode) as fp:
            fp.writelines(data)

    def get_all_articles(self):
        articles = []
        for f in self.root.iterdir():
            if f.is_file():
                with open(f, 'r') as fi:
                    articles.append(json.loads(fi.read()))
        return articles


if __name__ == '__main__':
    db = TextFiles('final')
    art = db.get_all_articles()
