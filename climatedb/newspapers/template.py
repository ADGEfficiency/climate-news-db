def check_PAPER_url(url):
    return True


def get_PAPER_article_id(url):
    return article_id


def parse_PAPER_html(url):
    return {
        "newspaper_id": "guardian",
        "body": article,
        "headline": headline,
        "article_url": url,
        "html": html,
        "article_id": url.split("/")[-1],
        "date_published": published,
        "date_modified": updated,
    }

guardian = {
    "newspaper_id": "guardian",
    "newspaper": "The Guardian",
    "newspaper_url": "theguardian.com",
    "checker": check_guardian_url,
    "parser": parse_guardian_html,
    "get_article_id": get_guardian_article_id,
    "color": "#052962"
}
