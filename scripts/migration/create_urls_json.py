"""Migrates from urls.data list to urls.json"""
from datetime import datetime

from climatedb.config import DBHOME
from climatedb.databases import URLs
from climatedb.registry import find_newspaper_from_url


if __name__ == '__main__':
    start_fresh = True
    check_urls = False

    with open(DBHOME / 'urls.data', 'r') as fi:
        data = fi.readlines()
        data = [d.strip('\n') for d in data]

    print(f'read {len(data)} from urls.data')
    data = list(set(data))

    new_data = []

    for n, url in enumerate(data):
        try:
            print(n / len(data) * 100, len(new_data), url)
            paper = find_newspaper_from_url(url)

            c1 = paper['newspaper_id'] == 'guardian'
            c2 = paper['newspaper_id'] == 'bbc'

            if c1 or c2:
                checker = paper['checker']
                if checker(url):
                    new_data.append(url)
                else:
                    print(f'dropping {url}')
        except TypeError:  # sometimes can't find paper because of times urls
            pass

    #  SHOULD ALSO SAVE A NEW URLS.DATA?

    data = [{'url': d, 'search_time_UTC': datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S')} for d in data]
    print(f'added timestamps')

    urls = URLs('urls.jsonl', engine='jsonl', key='url')
    if start_fresh and len(urls):
        urls.engine.data.unlink()

    print(f'adding urls to {urls.name}')
    print(f'  before {len(urls)}')
    urls.add(data)
    print(f'  after {len(urls)}')

