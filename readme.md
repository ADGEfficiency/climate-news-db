# climate-news-db

Database of climate change news articles - [see with the dataset here](http://www.climate-news-db.com/).

## Setup

Python 3.7+.

```bash
$ make init
```

## Use

The entry point to the data collection is the CLI command `collect`.  To collect 16 articles from Google:

```bash
$ dbcollect economist -n 16 --parse --source google
```

This will download data into `$HOME/climate-nlp`.  The final data is in `$HOME/climate-nlp/final/{newspaper_id}/{article_id}.json`.  The corresponding raw HTML is found at `$HOME/climate-nlp/raw/{newspaper_id}/{article_id}.html'`.

CLI options:

```bash
$ dbcollect --help
```
