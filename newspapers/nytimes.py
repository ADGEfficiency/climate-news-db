import json

from bs4 import BeautifulSoup
import requests

from newspapers.utils import check_match


def check_nytimes_url(url, logger):
    unwanted = ['interactive', 'topic', 'spotlight', 'times-journeys', 'freakonomics.blogs.nytimes.com', 'newsletters', 'ask', 'video']
    if not check_match(url, unwanted):
        logger.info(f'nytimes, {url}, check failed')
        return False
    else:
        return True


def parse_nytimes_html(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html5lib")

    section = soup.findAll('section', attrs={'name': 'articleBody'})
    if len(section) != 1:
        return {}
    article = ''.join([p.text for p in section[0].findAll('p')])

    noise = [
        'The Times is committed to publishing a diversity of letters to the editor. We’d like to hear what you think about this or any of our articles. Here are some tips. And here’s our email: letters@nytimes.com.Follow The New York Times Opinion section on Facebook, Twitter (@NYTopinion) and Instagram.',
        'Want climate news in your inbox? Sign up here for Climate Fwd:, our email newsletter.',
        'For more news on climate and the environment, follow @NYTClimate on Twitter.'

    ]
    for n in noise:
        article = article.replace(n, '')

    ld = soup.findAll('script', attrs={'type': 'application/ld+json'})
    ld = json.loads(ld[0].getText())

    return {
        'newspaper_id': 'nytimes',
        'body': article,
        'headline': ld['headline'],
        'article_url': url,
        'html': html,
        'article_id': url.split('/')[-1],
        'date_published': ld['datePublished'],
        'date_modified': ld['dateModified']
    }


if __name__ == '__main__':
    url = 'https://www.nytimes.com/2019/12/04/climate/climate-change-acceleration.html'
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html5lib")

    import json
    ld = soup.findAll('script', attrs={'type': 'application/ld+json'})
    ld = json.loads(ld[0].getText())
