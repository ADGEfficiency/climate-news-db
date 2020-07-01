"""Tools for backwards compatability with older schema"""

import os

from pathlib import Path
import json

from database import TextFiles
local_db = TextFiles()

def scrape_old_db(source):
    # always writes to local db
    path = Path(source)
    for file in path.iterdir():
        if file.is_file():
            with open(file, 'r') as fi:
                data = json.loads(fi.read())
                local_db.write(data['url'], 'urls.data', 'a')

source = os.environ['HOME'] + '/climate-nlp-s3/final'
scrape_old_db(source)

scrape_old_db(os.environ['HOME'] + '/climate-nlp/final')

# def clean_urls():

urls = local_db.get('urls.data')
urls = urls.split('\n')
urls.remove('')

print(urls)

local_db.write(set(urls), 'urls.data', 'w')

