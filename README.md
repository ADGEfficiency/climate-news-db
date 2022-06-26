# climate-news-db

A database of climate change news articles - [use the dataset here](http://www.climate-news-db.com/).


## Dataset Description

The database is made up of a number of data structures (such as JSONLines text files or a SQLite database).

You can grab a copy of all the data from a public S3 bucket using (this will copy data into a folder `./data-neu`):

```shell
$ make pulls3
```

This folder contains all the data:

```
$ tree data-neu
data-neu
├── articles
│   ├── aljazeera.jsonlines
│   ├── atlantic.jsonlines
│   ├── bbc.jsonlines
│   ├── cnn.jsonlines
│   ├── dailymail.jsonlines
│   ├── dw.jsonlines
│   ├── economist.jsonlines
│   ├── fox.jsonlines
│   ├── guardian.jsonlines
│   ├── independent.jsonlines
│   ├── newshub.jsonlines
│   ├── nytimes.jsonlines
│   ├── nzherald.jsonlines
│   ├── skyau.jsonlines
│   ├── stuff.jsonlines
│   └── washington_post.jsonlines
├── climate-news-db-dataset.zip
├── db.sqlite
├── newspapers.json
├── urls.csv
└── urls.jsonl

1 directory, 21 files

```

urls.jsonl

- text file with one (url, scrape time) per line
- these urls are raw & dirty - often have duplicates

urls.csv

- CSV with one url per line - url + newspaper info
- has meta data from data/newspapers.json for each paper

articles/$(NEWSPAPER_ID)/$(ARTICLE_ID).{json,html}

- stage = [raw, processed]
- newspaper_id
- article_id

db.sqlite

climate-news-db-dataset.zip

