import json

import argparse

from newspapers.guardian import check_guardian_url, parse_guardian_html
from newspapers.fox import check_fox_url, parse_fox_html

from pathlib import Path

from make_logger import make_logger

logger = make_logger('logger.log')


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
        # {"id": "nytimes", "name": "New York Times", "url": "nytimes.com"},
        # {"id": "sky-au", "name": "Sky News Australia", "url": "skynews.com.au"}
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

        #  search url getter
        #  return urls
        query = "climate change site:" + newspaper['url']
        from googlesearch import search
        checker = newspaper['checker']

        urls = [
            url for url in search(
                query,
                start=1,
                stop=args.num,
                pause=2.0,
                user_agent='climatecode'
            )
            if checker(url, logger)
        ]
        # print(f'found {len(urls)} for {newspaper['name']}')

        parser = newspaper['parser']
        for url in urls:
            parsed = parser(url)

            if parsed:
                fname = str(parsed['id'])
                logger.debug(f'saving {fname}')
                raw.post(parsed['html'], fname+'.html')
                del parsed['html']
                final.post(json.dumps(parsed), fname+'.json')
