# climate-news-db

Database of climate change news articles - [see the dataset here](http://www.climate-news-db.com/).


ecr repo
https://ap-southeast-2.console.aws.amazon.com/ecr/repositories/private/087085368915/climatedb-dev?region=ap-southeast-2


## Data Structures

data/newspapers.json
- maintained by hand - registry of newspapers
- could be generated from the spiders in climatedb

data/urls.jsonl

- text file with one (url, scrape time) per line
- these urls are dirty - often have duplicates

data/urls.csv

- CSV with one url per line - url + newspaper info
- has meta data from data/newspapers.json for each paper

data/articles/$(NEWSPAPER_ID)/$(ARTICLE_ID).{json,html}

- stage = [raw, processed]
- newspaper_id
- article_id



## Newspapers Spiders

```python
from climatedb.databases_neu import get_urls_for_paper
from climatedb.parsing_utils import get_body
from climatedb.spiders.base import ClimateDBSpider
from climatedb.utils import form_article_id


class Template(ClimateDBSpider):
    """just for dev"""

    name = "name"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):
        article_name = form_article_id(response.url, -1)
        body = get_body(response)

        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        subtitle = response.xpath('//meta[@property="og:description"]/@content').get()
        date = response.xpath('//meta[@itemprop="datePublished"]/@content').get()

        meta = {
            "headline": headline,
            "subtitle": subtitle,
            "body": body,
            "article_url": response.url,
            "date_published": date,
            "article_name": article_name,
        }
        return self.tail(response, meta)
```
