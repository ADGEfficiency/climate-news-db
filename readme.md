# Climate News DB

[This app is deployed here](http://www.climate-news-db.com/).

Database of climate change news articles.

## Setup

Python 3.7+ (we use f-strings)

```bash
$ pip install -r requirements.txt
```

## Use

```bash
$ python download.py --newspapers all --n 50
```

This will download files into `$HOME`.  The final data is in `final/{article_id}.json`.

The corresponding raw HTML is found at `raw/{article_id}.html'`.

`article_id` is the last part of the article url.

## Useful commands

See how many articles you have:

```bash
$ ls ~/climate-nlp/final | wc -l
```

How many urls
```bash
$ cat ~/climate-nlp/urls.data | wc -l
```

## Deploy

```bash
$ aws s3 sync ~/climate-nlp s3://climate-nlp

$ make app
```
