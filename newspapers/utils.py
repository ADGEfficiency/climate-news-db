from datetime import datetime


def check_match(url, unwanted):
    for unw in unwanted:
        if unw in url:
            return False
    return True


def parser_decorator(parser):
    def wrapper(*args, **kwargs):
        parsed = parser(*args, **kwargs)
        parsed['date-uploaded'] = datetime.utcnow().isoformat()

        schema = [
            'newspaper-id',
            'body',
            'html',
            'url',
            'article-id',
            'date-published',
            'date-modified',
            'date-uploaded'
        ]
        for s in schema:
            if s not in parsed.keys():
                raise ValueError(f'{s} missing from parsed article')

        return parsed
    return wrapper
