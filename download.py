import argparse
import json

from database import TextFiles
from logger import make_logger

from newspapers.registry import check_parsed_article, registry, clean_parsed_article

home = TextFiles()

import time
import random


def google_search(url, query='climate change', stop=10, backoff=1.0):
    #  protects against a -1 example
    if stop <= 0:
        raise ValueError('stop of {stop} is invalid - change the --num argument')

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
    parser.add_argument('--source', default='google', nargs='?', type=str)
    args = parser.parse_args()

    logger = make_logger('logger.log')
    logger.info(args)
    url_source = args.source

    #  get newspaper info
    newspapers = args.newspapers
    if newspapers == ['all', ]:
        newspapers = registry
    else:
        newspapers = [n for n in registry if n['newspaper_id'] in newspapers]
    print(newspapers)

    for newspaper in newspapers:
        #  collect_urls
        parser = newspaper['parser']
        checker = newspaper['checker']

        if url_source == 'google':
            print(f'searching for {args.num} from {newspaper["newspaper"]}')
            urls = google_search(newspaper['newspaper_url'], stop=args.num)
            urls = [url for url in urls if checker(url, logger)]
            logger.info(f'search: found {len(urls)} for {newspaper["newspaper"]}')
            home.write(urls, 'urls.data', 'a')
            print(f'finished searching')

        elif url_source == 'urls.data':
            urls = home.get('urls.data')
            urls = urls.split('\n')
            urls.remove('')

            #  filter by newspaper
            urls = [u for u in urls if newspaper['newspaper_url'] in u if checker(u, logger)][:args.num]
            logger.info(f'loaded {len(urls)} urls from {url_source}')

        else:
            raise ValueError(f'{url_source} is not valid')

        #  parse_urls
        for url in urls:
            logger.info(f'{url}, parsing')
            raw = TextFiles(f'raw/{newspaper}')
            final = TextFiles(f'final/{newspaper}')

            parsed = parser(url)
            if 'error' in parsed.keys():
                error = parsed['error']
                logger.info(f'{url}, {error}')

            else:
                parsed = check_parsed_article(parsed)
                if not parsed:
                    logger.info(f'{url}, failed check_parsed_article')

                else:
                    parsed = clean_parsed_article(parsed)

                    article_id = parsed['article_id']

                    logger.info(f'{url}, saving, article_id={article_id}')
                    raw.write(parsed['html'], article_id+'.html', 'w')
                    del parsed['html']
                    try:
                        final.write(json.dumps(parsed), article_id+'.json', 'w')
                    except TypeError:
                        logger.info(f'{url}, type error')
