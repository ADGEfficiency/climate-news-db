from bs4 import BeautifulSoup
import requests


def check_match(url, unwanted):
    for unw in unwanted:
        if unw in url:
            return False
    return True


def check_guardian_url(url):
    unwanted = ['live', 'gallery', 'audio', 'video', 'ng-interactive', 'interactive']
    if not check_match(url, unwanted):
        print('rejecting {}'.format(url))
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
            print('rejecting {}'.format(url))
            return False

    #  short url
    except IndexError:
        print('rejecting {}'.format(url))
        return False


def parse_guardian_html(link):
    cls = 'content__article-body from-content-api js-article__body'
    itemprop = 'articleBody'
    req = requests.get(link)
    html = req.text
    soup = BeautifulSoup(html, features="html5lib")
    table = soup.findAll('div', attrs={"itemprop": itemprop})

    if len(table) != 1:
        return {}

    article = [p.text for p in table[0].findAll('p')]
    article = ''.join(article)
    return {
        'body': article,
        'url': link,
        'author': "",
        'date': "",
        'newspaper': 'guardian',
        'html': html
    }
