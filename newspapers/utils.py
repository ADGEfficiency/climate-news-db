def check_match(url, unwanted):
    for unw in unwanted:
        if unw in url:
            return False
    return True


def find_one_tag(soup, name, attrs={}):
    """find a single tag (and only one tag) in bs4"""
    data = soup.findAll(name, attrs)
    if len(data) != 1:
        import pdb; pdb.set_trace()
    assert len(data) == 1
    return data[0]


def form_article_id(url):
    article_id = url.split('/')[-1]
    return article_id.replace('.html', '')
