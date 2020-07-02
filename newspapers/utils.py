from datetime import datetime


def check_match(url, unwanted):
    for unw in unwanted:
        if unw in url:
            return False
    return True


def parser_decorator(parser):
    def wrapper(*args, **kwargs):
        parsed = parser(*args, **kwargs)
        if not parsed:
            return {}

        parsed['date_uploaded'] = datetime.utcnow().isoformat()

        schema = [
            'newspaper',
            'newspaper_id',
            'body',
            'headline',
            'html',
            'url',
            'article_id',
            'date_published',
            'date_modified',
            'date_uploaded'
        ]
        for s in schema:
            if s not in parsed.keys():
                raise ValueError(f'{s} missing from parsed article')

        return parsed
    return wrapper
