# Climate News DB

Database of climate change news articles.  [See the app deployed here](http://www.climate-news-db.com/) - [see the source code here](https://github.com/ADGEfficiency/climate-news-db).

## Setup

Python 3.7+ (we use f-strings).

```bash
$ pip install -r requirements.txt
```

## Use

```bash
$ python download.py --newspapers all --n 50
```

This will download files into `$HOME`.  The final data is in `final/{newspaper_id}/{article_id}.json`.

The corresponding raw HTML is found at `raw/{newspaper_id}/{article_id}.html'`.

## Useful commands

See how many articles you have:

```bash
$ ls ~/climate-nlp/final | wc -l
```

How many urls in `urls.data`:
```bash
$ cat ~/climate-nlp/urls.data | wc -l
```

## Use locally

```bash
$ make app
```
