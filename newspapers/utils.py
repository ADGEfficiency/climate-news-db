def check_match(url, unwanted):
    for unw in unwanted:
        if unw in url:
            return False
    return True
