# climate-news-db

The climate-news-db has two goals - to create a dataset of climate change newspaper articles for NLP researchers and to provide a public interface for users to view climate change news.

Data linage chart
- lambda -> database on s3

Deployment chart
- scraper
- flyio

# Use

## Crawling URLs

```shell-session
$ make crawl
```

## Interactive Search for Getting URLs

Requires Gum

```shell-session
$ bash scripts/cli.sh
```

## Statistics

- number of rejected urls,
- number of parsed urls,

# Data Catalog

{"url": "https://www.chinadaily.com.cn/a/202302/21/WS63f4aea4a31057c47ebb004e.html", "search_time_utc": "2023-03-20T00:05:02.998560"}
{"url": "https://www.chinadaily.com.cn/a/202301/19/WS63c8a4a8a31057c47ebaa8e4.html", "search_time_utc": "2023-03-20T00:05:02.998560"}

## urls.jsonl

Append only storage of raw newspaper urls.  Created by a daily Google search for each newspaper with the keywords `climate change` and `climate crisis`.  This file contains many duplicates.
