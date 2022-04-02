start with a single, atomic sample

```python
url = "https://www.theguardian.com/science/2015/mar/17/climate-change-demands-immense-economic-changes"
```

Following below to create a spider with selectors

https://docs.scrapy.org/en/latest/intro/tutorial.html


Making a spider
/Users/adam/climate-news-db/scrapy_cdb/spiders/guardian.py

```
#  ./cdb_scrapy/cdb_scrapy/spiders/guardian.py
from pathlib import Path
import scrapy
import json


class GuardianSpider(scrapy.Spider):
    name = "guardian"
    start_urls = [
        "https://www.theguardian.com/commentisfree/2018/oct/30/climate-change-action-effective-ipcc-report-fossil-fuels"
    ]

    def parse(self, response):
        article_name = response.url.split("/")[-1]
        paper = "guardian"

        fi = (
            Path.home()
            / "climate-news-db"
            / "data-reworked"
            / "articles"
            / paper
            / article_name
        )
        fi.parent.mkdir(exist_ok=True, parents=True)

        #  save html
        fi.with_suffix(".html").write_bytes(response.body)
        self.log(f" saved to {fi}.html")

        #  save json file
        meta = {"title": response.css("title::text").get()}
        fi.with_suffix(".json").write_text(json.dumps(meta))
        self.log(f" saved to {fi}.json")
```

Now onto extracting data

```
$ scrapy shell "https://www.theguardian.com/commentisfree/2018/oct/30/climate-change-action-effective-ipcc-report-fossil-fuels"
```

Two ways:
1. via CSS (response.css),
2. xpath (response.xpath) = important one (CSS converted to xpath)

Xpath is powerful due to being able to scrape based on *content* - like 'select link that contains next

## https://docs.scrapy.org/en/latest/topics/selectors.html#topics_selectors - scrapy docs on xpath

.get versus .getall to make strings

`.attrib['href']` to query for attributes, or use `@href`

tutorial by example - http://zvon.org/comp/r/tut-XPath_1.html

tutorial - how to think in xpath - http://plasmasturm.org/log/xpath101/

---

Following links = [RnR]

By default, Scrapy filters out duplicated requests to URLs already visited, avoiding the problem of hitting servers too much because of a programming mistake. This can be configured by the setting DUPEFILTER_CLASS.

As yet another example spider that leverages the mechanism of following links, check out the CrawlSpider class for a generic spider that implements a small rules engine that you can use to write your crawlers on top of it.

---

After have a basic spider working, need to decide the structure of the article json

Use 

```
from datetime import datetime

import pydantic
from pydantic import BaseModel


class ArticleModel(BaseModel):
    body: str
    title: str
    article_url: str
    html: str
    article_id: str
    date_published: datetime


class PaperModel(BaseModel):
    newspaper_id: str
    newspaper: str
    newspaper_url: str

```

Urls pipeline:

- google search -> urls.txt (just a list of urls)
- urls.txt -> urls.csv

create simple urls.csv to get pipeline going (fake out add_newspaper_to_urls.py)

```
url,newspaper_id
https://www.theguardian.com/environment/2020/jun/17/climate-crisis-alarm-at-record-breaking-heatwave-in-siberia,guardian
https://www.theguardian.com/commentisfree/2018/oct/30/climate-change-action-effective-ipcc-report-fossil-fuels,guardian
```


```
scrapy:
	scrapy crawl guardian -o ./data-reworked/articles/guardian.jsonlines -L INFO

./data-reworked/urls.csv: ./data-reworked/urls.txt scripts/add_newspaper_to_urls.py
	python3 scripts/add_newspaper_to_urls.py

pipe: scrapy

inspect:
	wc -l ./data-reworked/articles/guardian.jsonlines -L INFO


```

---

for finding date - this was first way , didn't work

        date = response.xpath('//label[@for="dateToggle"]//text()').get()
        date = date.replace("BST", "+0100")
        date = date.replace("GMT", "+0000")
        date = datetime.strptime(date, "%a %d %b %Y %H.%M %z")

But ended up getting it from application.json

---

created newspapers.json - use it to drive makefile

---

.env - with {} syntax for sharing with Make, include .env

---

rewrite app in fast api, settle on using meta for most scraping stuff

---

moving analytics from the webapp into the backend

join, insert in sqlite

---

using the dataset - first.py

---

# FIRST



Let's start our project with scraping a single sample - 

---

brew tap heroku/brew && brew install heroku

```
heroku login
heroku create

generate req.txt (use poetry for this)
```
uvicorn==0.12.3
aiofiles==0.6.0
python-multipart==0.0.5
jinja2==2.11.2

```
generate runtime.txt (python-3.8.12)

git push heroku main
heroku open
```

---
docker bit

build:
  docker:
    web: docker/app.Dockerfile

heroku stack:set container

git push heroku master

---

heroku container:login

docker tag climatedb-app-local registry.heroku.com/climate-news-db/web
docker push registry.heroku.com/climate-news-db/web

heroku container:release web

---

full deploy

- pull s3
- make database
- push s3
- make heroku docker


public bucket 

{
    "Version": "2008-10-17",
    "Statement": [
        {
            "Sid": "AllowPublicRead",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::climatedb-dev/*",
                "arn:aws:s3:::climatedb-dev"
            ]
        }
    ]
}
