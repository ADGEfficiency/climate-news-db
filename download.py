import argparse
import json

from database import TextFiles
from logger import make_logger

from newspapers.registry import registry

home = TextFiles()
raw = TextFiles('raw')
final = TextFiles('final')
logger = make_logger('logger.log')

import time
import random

def google_search(url, query='climate change', stop=10, backoff=1.0):
        from urllib.error import HTTPError
        try:
            from googlesearch import search
            query = f"{query} site:{url}"

            time.sleep((2**backoff) + random.random())

            urls = list(search(
                query,
                start=1,
                stop=stop,
                pause=4.0,
                user_agent='climatecode'
            ))
            logger.info('google search successful {*args} {**kwargs}')
            return urls

        except HTTPError as e:
            logger.info(f'{e} at backoff {backoff}')
            return google_search(url, query, stop, backoff=backoff+1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--newspapers', default=["all", ], nargs='*')
    parser.add_argument('--num', default=10, nargs='?', type=int)
    args = parser.parse_args()
    print(args)

    newspapers = args.newspapers
    if newspapers == ['all', ]:
        newspapers = registry
    else:
        newspapers = [n for n in registry if n['newspaper-id'] in newspapers]

    print(newspapers)

    for newspaper in newspapers:
        print(f'scraping {args.num} from {newspaper["newspaper"]}')
        urls = google_search(newspaper['url'], stop=args.num)

        checker = newspaper['checker']
        urls = [url for url in urls if checker(url, logger)]
        logger.info(f'search: found {len(urls)} for {newspaper["newspaper"]}')

        home.append(urls, 'urls.data')

        parser = newspaper['parser']
        for url in urls:
            # TODO check if the file exists -> don't parse
            logger.debug(f'parsing {url}')
            parsed = parser(url)

            if parsed:
                fname = str(parsed['article-id'])
                logger.debug(f'saving {fname}')
                raw.post(parsed['html'], fname+'.html')
                del parsed['html']
                try:
                    final.post(json.dumps(parsed), fname+'.json')
                except TypeError:
                    import pdb; pdb.set_trace()
