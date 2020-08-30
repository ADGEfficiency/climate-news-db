# climate-news-db

Database of climate change news articles -  [play with the data here](http://www.climate-news-db.com/).

## Setup

Python 3.7+ (we use f-strings).

```bash
$ make setup
```

## Use

The entry point to the data collection is the CLI command `collect`.  To collect 16 articles from Google:

```bash
$ collect economist -n 16 --parse --source google
```

This will download data into `$HOME/climate-nlp`.  The final data is in `$HOME/climate-nlp/final/{newspaper_id}/{article_id}.json`.  The corresponding raw HTML is found at `$HOME/climate-nlp/raw/{newspaper_id}/{article_id}.html'`.

Options for the CLI:

```bash
$ collect --help
collect [OPTIONS] [NEWSPAPERS]...
  -n, --num INTEGER     Number of urls to attempt to collect.  [default: 5]
  --source TEXT         Where to look for urls.  [default: google]
  --parse / --no-parse
  --help                Show this message and exit.
```
