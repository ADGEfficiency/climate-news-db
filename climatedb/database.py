import abc
from pathlib import Path
import json


DBHOME = Path.home() / "climate-news-db-data"


class AbstractDB(abc.ABC):
    @abc.abstractmethod
    def add(self, batch):
        raise NotImplementedError()

    @abc.abstractmethod
    def get(self, reference):
        raise NotImplementedError()


class File(AbstractDB):
    """Single File"""
    def __init__(self, name):
        self.data = DBHOME / name

    def add(self, batch, mode='a'):
        if isinstance(batch, str):
            batch = (batch,)
        batch = [d + "\n" for d in batch]

        if not self.data.is_file():
            mode = 'w'

        with open(self.data, mode) as fp:
            fp.writelines(batch)

    def get(self, reference=None):
        with open(self.data, "r") as fp:
            data = fp.read()
            data = data.split("\n")
            data.remove("")
            return data[-reference:]


class Folder(AbstractDB):
    """Folder of files"""
    def __init__(
        self,
        name,
        folder_key='newspaper_id',
        file_key='article_id'
    ):
        self.name = DBHOME / name
        self.folder_key = folder_key
        self.file_key = file_key
        self.data = {}

    def add(self, batch):
        for data in batch:
            key = data[self.folder_key]

            fldr = self.name / key
            fldr.mkdir(exist_ok=True, parents=True)

            fi = (fldr / str(data[self.file_key])).with_suffix('.json')
            with open(fi, 'w') as fi:
                fi.write(json.dumps(data))

    def get(self, reference):
        if reference is None:
            fldr = self.name
        else:
            fldr = self.name / reference

        articles = []
        for f in fldr.iterdir():
            if f.is_file():
                with open(f, "r") as fi:
                    articles.append(json.loads(fi.read()))
        return articles




class TextFiles:
    def __init__(self, root=None, logger=None):
        #  root is either raw or final
        if root:
            self.root = Path.home() / db_folder / root
            self.root.mkdir(parents=True, exist_ok=True)
            self.newspapers = {
                folder.name: NewspaperTextFiles(f"{root}/{folder.name}")
                for folder in self.root.iterdir()
                if folder.is_dir()
            }
        else:
            self.root = Path.home() / db_folder
            self.root.mkdir(parents=True, exist_ok=True)

        if logger:
            logger.info(f"init db at {self.root}")

    def get_all_articles(self):
        """searches all newspapers"""
        self.articles = []
        for paper in self.newspapers.keys():
            self.articles.extend(self.newspapers[paper].get_all_articles())
        return self.articles

    def get_article(self, article_id):
        """searches all newspapers"""
        for f in self.root.rglob("**/*.json"):
            if f.is_file() and article_id in f.name:
                with open(f, "r") as fi:
                    article = json.loads(fi.read())
        return article

    def get_articles_from_newspaper(self, paper):
        """all articles from one newspaper"""
        return self.newspapers[paper].get_all_articles()

    def get(self, fi):
        """single file"""
        fi = self.root / fi
        with open(fi, "r") as fp:
            return fp.read()

    def write(self, data, file, mode):
        """single file"""
        #  needs to be a list due to how we add the newline character /n
        if isinstance(data, str):
            data = (data,)
        data = [d + "\n" for d in data]

        fi = self.root / file
        with open(fi, mode) as fp:
            fp.writelines(data)


class NewspaperTextFiles(TextFiles):
    def __init__(self, root=None):
        super().__init__(root=root)

    def get_all_articles(self):
        #  todo precompute this list on init
        articles = []
        for f in self.root.iterdir():
            if f.is_file():
                with open(f, "r") as fi:
                    articles.append(json.loads(fi.read()))
        return articles

    def check(self, article_id):
        articles = self.get_all_articles()
        article_ids = set([a["article_id"] for a in articles])
        if article_id in article_ids:
            return True
        return False
