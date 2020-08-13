# climate-news-db

Database of climate change news articles.  [See the app deployed here](http://www.climate-news-db.com/) - [see the source code here](https://github.com/ADGEfficiency/climate-news-db).

## Setup

Python 3.7+ (we use f-strings).

```bash
$ pip install -r requirements.txt
$ python setup.py install
```

## Use

```bash
$ collect [OPTIONS] [NEWSPAPERS]...
  -n, --num INTEGER     Number of urls to attempt to collect.  [default: 5]
  --source TEXT         Where to look for urls.  [default: google]
  --parse / --no-parse
  --help                Show this message and exit.

parse [OPTIONS]
  --rewrite / --no-rewrite
  --help                    Show this message and exit.
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
