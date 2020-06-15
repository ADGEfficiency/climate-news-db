# Climate Newspaper Downloader

CLI to download climate change news articles.

## Setup

Python 3.7+ (we use f-strings)

```bash
$ pip install -r requirements.txt
```

## Use

```bash
$ python download.py --newspapers all --n 50
```

This will download files into `$HOME`.  The final data has the schema:
```json
{
	"newspaper": "",
	"body": "",
	"url": "",
	"id': "",
	"published": "",
}
```

The corresponding raw HTML is found at `raw/{id}.html'`.

## Useful commands

See how many articles you have:

```bash
$ ls ~/climate-nlp/final | wc -l
```
