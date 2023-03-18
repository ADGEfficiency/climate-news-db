from climatedb import files
from climatedb.models import NewspaperMeta


def find_urls_to_scrape(newspaper: str) -> list[str]:
    return ["https://www.chinadaily.com.cn/a/202301/19/WS63c8a4a8a31057c47ebaa8e4.html"]


def create_article_name(url: str, idx: int = -1) -> str:
    url = url.strip("/")
    url = url.split("?")[0]
    url = url.strip("/")
    article_id = url.split("/")
    article_id = [u for u in article_id if len(url) > 0]
    return article_id[idx].replace(".html", "")


def find_newspaper_from_url(url: str) -> NewspaperMeta:
    papers = files.JSONFile("./newspapers.json").read()

    for pap in papers:
        paper = NewspaperMeta(**pap)
        if paper.newspaper_url in url:
            return paper
    raise ValueError(f"No paper found for {url}")
