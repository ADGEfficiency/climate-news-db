def check_match(url, unwanted):
    for unw in unwanted:
        if unw in url:
            return False
    return True


def find_one_tag(soup, name, attrs={}):
    """find a single tag (and only one tag) in bs4"""
    data = soup.findAll(name, attrs)
    if len(data) != 1:
        print(name, attrs, len(data))
    assert len(data) == 1
    return data[0]


def form_article_id(url, idx=-1):
    url = url.strip("/")
    article_id = url.split("/")[idx]
    return article_id.replace(".html", "")


def find_application_json(soup, find='headline'):
    import json
    apps = soup.findAll('script', {'type': 'application/ld+json'})
    for app in apps:
        app = json.loads(app.text)
        if find in app:
            return app
