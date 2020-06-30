from bs4 import BeautifulSoup
import requests

from newspapers.utils import check_match, parser_decorator


def check_guardian_url(url, logger):
    unwanted = ['live', 'gallery', 'audio', 'video', 'ng-interactive', 'interactive']

    if not check_match(url, unwanted):
        logger.info(f'guardian, {url}, check failed')
        return False

    parts = url.split('/')
    try:
        #  check if there is a year / str / day
        #  can be in one of two positions
        cond1 = parts[4].isdigit() and parts[6].isdigit()
        cond2 = parts[5].isdigit() and parts[7].isdigit()

        if cond1 or cond2:
            return True
        else:
            logger.info(f'guardian, {url}, check failed')
            return False

    #  short url
    except IndexError:
        logger.info(f'guardian, {url}, check failed')
        return False


@parser_decorator
def parse_guardian_html(url):
    itemprop = 'articleBody'
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, features="html5lib")

    table = soup.findAll('div', attrs={"itemprop": itemprop})
    if len(table) != 1:
        return {}
    article = ''.join([p.text for p in table[0].findAll('p')])

    published = soup.findAll('time', attrs={'itemprop': 'datePublished'})
    assert len(published) == 1
    published = published[0]['datetime']

    return {
        'newspaper-id': 'guardian',
        'body': article,
        'url': url,
        'html': html,
        'article-id': url.split('/')[-1],
        'date-published': published
    }
