# climate-news-db

A database of climate change news articles - [use the dataset here](http://www.climate-news-db.com/).


## Data Structures

The database is made up of a number of data structures (such as JSONLines text files or a SQLite database).

You can grab a copy of all the data from a public S3 bucket using:

```shell
$ make pulls3
```

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
