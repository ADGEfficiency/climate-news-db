from pathlib import Path
import json


class NewspaperTextFiles:
    def __init__(self, root=None):
        self.root = Path.home() / 'climate-nlp' / root

    def get_all_articles(self):
        articles = []
        for f in self.root.iterdir():
            if f.is_file():
                with open(f, 'r') as fi:
                    articles.append(json.loads(fi.read()))
        return articles


class TextFiles:
    def __init__(self, root=None):
        #  root is either raw or final
        if root:
            self.root = Path.home() / 'climate-nlp' / root
        else:
            self.root = Path.home() / 'climate-nlp'

        self.root.mkdir(parents=True, exist_ok=True)

        self.newspapers = {
            folder.name: NewspaperTextFiles(f"{root}/{folder.name}")
            for folder in self.root.iterdir() if folder.is_dir()
        }

    def get_all_articles(self):
        """searches all newspapers"""
        self.articles = []
        for paper in self.newspapers.keys():
            self.articles.extend(self.newspapers[paper].get_all_articles())
        return self.articles

    def get_article(self, article_id):
        """searches all newspapers"""
        for f in self.root.rglob('**/*.json'):
            if f.is_file() and article_id in f.name:
                with open(f, 'r') as fi:
                    article = json.loads(fi.read())
        return article

    def get_articles_from_newspaper(self, paper):
        """all articles from one newspaper"""
        return self.newspapers[paper].get_all_articles()

    def get(self, fi):
        """single file"""
        fi = self.root / fi
        with open(fi, 'r') as fp:
            return fp.read()

    def write(self, data, file, mode):
        """single file"""
        #  needs to be a list due to how we add the newline character /n
        if isinstance(data, str):
            data = (data, )
        data = [d + '\n' for d in data]

        fi = self.root / file
        with open(fi, mode) as fp:
            fp.writelines(data)
