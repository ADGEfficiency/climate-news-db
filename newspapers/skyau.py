from bs4 import BeautifulSoup
import requests
from datetime import datetime as dt
import re


def check_sky_au_url(url, logger=None):
    return True


def parse_sky_au_url(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")
    article = ''.join([p.text for p in soup.findAll('p', attrs={"class": "description-text"})])

    #  finding published date as a unix stamp in a script tag
    try:
        scripts = soup.findAll('script')
        assert len(scripts) == 13
        script_tag = scripts[8]
        match = re.search('"publishedDate":"\d+"', script_tag.contents[0])
        unix_time = int(re.findall(r'\d+', match.group(0))[0])
        from datetime import datetime as dt
        #  / 1000 as stamp is in milliseconds
        stamp = dt.utcfromtimestamp(unix_time / 1000).isoformat()
    except AttributeError:
        #  TODO
        stamp = soup.findAll('div', attrs={'class': 'article-byline'})
        assert len(stamp) == 1

    return {
        'newspaper': 'skyau',
        'body': article,
        'html': html,
        'url': url,
        'id': url.split('/')[-1],
        'published': stamp
    }


if __name__ == '__main__':
    url = 'https://www.skynews.com.au/details/_6106377484001'
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")

    scripts = soup.findAll('script')
    assert len(scripts) == 13
    s = scripts

    import re
    script_tag = scripts[8]

    match = re.search('"publishedDate":"\d+"', script_tag.contents[0])
    unix_time = int(re.findall(r'\d+', match.group(0))[0])
    from datetime import datetime as dt
    #  / 1000 as stamp is in milliseconds
    stamp = dt.utcfromtimestamp(unix_time / 1000).isoformat()
