from rich import print

from climatedb import database, files, models
from climatedb.settings import get_project_settings

if __name__ == "__main__":
    settings = get_project_settings()

    newspapers = [
        p
        for p in (settings["DATA_HOME"] / "articles").iterdir()
        if p.suffix == ".jsonl"
    ]

    """
    for newspaper in newspapers:
        load articles from jsonl
        insert into articles table
    """

    for newspaper in newspapers:
        print(f"newspaper: [bold blue]{newspaper.name}[/bold blue]")
        newspaper = database.read_newspaper(newspaper.stem)

        articles = files.JSONLines(
            settings["DATA_HOME"] / "articles" / newspaper.name
        ).read()

        for article in articles:
            article = models.Article(
                **article,
                article_length=len(article["body"].split(" ")),
                newspaper=newspaper,
                newspaper_id=newspaper.id,
            )
            database.write_article(settings["DB_URI"], article)
        print(f" {len(articles)} articles written")

    """
    for opinion in opinions:
        load opinion from json
        insert into opinions table
    """
