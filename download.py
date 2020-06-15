import json

import argparse

from newspapers.guardian import check_guardian_url, parse_guardian_html
from newspapers.fox import check_fox_url, parse_fox_html
from newspapers.skyau import check_sky_au_url, parse_sky_au_url
from newspapers.nytimes import check_nytimes_url, parse_nytimes_html

from pathlib import Path

from make_logger import make_logger

logger = make_logger('logger.log')


def google_search(url, query='climate change', stop=10):
    from googlesearch import search
    query = f"{query} site:{url}"
    return search(
        query,
        start=1,
        stop=stop,
        pause=2.0,
        user_agent='climatecode'
    )


class TextFiles:
    def __init__(self, root):
        self.root = Path.home() / 'climate-nlp' / root
        self.root.mkdir(parents=True, exist_ok=True)

    def post(self, data, fi):
        fi = self.root / fi
        with open(fi, 'w') as fp:
            fp.write(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--newspapers', default=["all", ], nargs='*')
    parser.add_argument('--num', default=10, nargs='?', type=int)
    args = parser.parse_args()
    print(args)

    registry = [
        {
            "id": "guardian",
            "name": "The Guardian",
            "url": "theguardian.com",
            "checker": check_guardian_url,
            "parser": parse_guardian_html
        },
        {
            "id": "fox",
            "name": "Fox News",
            "url": "foxnews.com",
            "checker": check_fox_url,
            "parser": parse_fox_html
        },
        {
            "id": "nytimes",
            "name": "New York Times",
            "url": "nytimes.com",
            "checker": check_nytimes_url,
            "parser": parse_nytimes_html
        },
        {
            "id": "skyau",
            "name": "Sky News Australia",
            "url": "skynews.com.au",
            "checker": check_sky_au_url,
            "parser": parse_sky_au_url
        }
    ]

    newspapers = args.newspapers
    if newspapers == ['all', ]:
        newspapers = registry
    else:
        newspapers = [n for n in registry if n['id'] in newspapers]

    raw = TextFiles('raw')
    final = TextFiles('final')

    print(newspapers)

    for newspaper in newspapers:
        print(f'scraping {args.num} from {newspaper["name"]}')

        urls = google_search(newspaper['url'], stop=args.num)

        checker = newspaper['checker']
        urls = [
            url for url in urls
            if checker(url, logger)
        ]

        logger.info(f'search: found {len(urls)} for {newspaper["name"]}')

        parser = newspaper['parser']
        for url in urls:
            # TODO check if the file exists -> don't parse
            parsed = parser(url)

            if parsed:
                fname = str(parsed['id'])
                logger.debug(f'saving {fname}')
                raw.post(parsed['html'], fname+'.html')
                del parsed['html']
                final.post(json.dumps(parsed), fname+'.json')
