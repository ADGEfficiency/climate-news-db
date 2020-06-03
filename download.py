import argparse


from guardian import check_guardian_url, parse_guardian_html


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--newspapers', default="all", nargs='*')
    parser.add_argument('--num', default=2, nargs='?', type=int)
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
        {"id": "fox", "name": "Fox News", "url": "foxnews.com"},
        {"id": "nytimes", "name": "New York Times", "url": "nytimes.com"},
        {"id": "sky-au", "name": "Sky News Australia", "url": "skynews.com.au"}
    ]

    newspapers = args.newspapers
    if newspapers == 'all':
        newspapers = registry
    else:
        newspapers = [n for n in registry if n['id'] in newspapers]

    print(newspapers)

    for newspaper in newspapers:
        print(f'scraping {args.num} from {newspaper["name"]}')

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
            if checker(url)
        ]
        print(urls)
