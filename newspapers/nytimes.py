from bs4 import BeautifulSoup
import requests

from newspapers.guardian import check_match


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

    article = article.replace(
        'The Times is committed to publishing a diversity of letters to the editor. We’d like to hear what you think about this or any of our articles. Here are some tips. And here’s our email: letters@nytimes.com.Follow The New York Times Opinion section on Facebook, Twitter (@NYTopinion) and Instagram.',
        ''
    )

    #  relying on published being the first date
    dts = soup.findAll('time')
    published = dts[0]['datetime']

    return {
        'newspaper': 'nytimes',
        'body': article,
        'url': url,
        'html': html,
        'id': url.split('/')[-1],
        'published': published,
    }
