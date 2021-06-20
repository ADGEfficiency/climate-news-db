# climate-news-db

Database of climate change news articles - [see the dataset here](http://www.climate-news-db.com/).

## Setup

Python 3.7+.

```bash
$ make init
```

## Use

The entry point to the data collection is the CLI command `collect`.  To collect 16 articles from Google and download into `$HOME/climate-news-db/data`:

```bash
$ dbcollect economist -n 16 --parse --source google
```

Flask app to display data in `$HOME/climate-news-db/data`:

```bash
$ make app
```

CLI options:

```bash
$ dbcollect --help
```

## Test

```bash
$ make test
```
