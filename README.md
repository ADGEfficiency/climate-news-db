# climate-news-db

The climate-news-db has two goals:

1. provide a dataset for NLP and climate change media researchers,
2. provide a [web application](http://www.climate-news-db.com/) to view how newspapers are writing about climate change.

# Dataset

The dataset is made up of a number of data artifacts (JSON, JSONL & CSV text files & SQLite database) ([you can download them here](https://www.climate-news-db.com/download)):

```
$ tree climate-news-db-dataset
climate-news-db-dataset
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
```

Daily scraping writes article URls to `urls.jsonl` on S3:

- text file with one JSON (url, scrape time) per line,
- these urls are raw & dirty - often have duplicates,
- each day a AWS Lambda function searches all newspapers for the terms `climate change` and `climate crisis`,
- search result URLs are appended to `urls.jsonl`.

```json
{"url": "https://www.newshub.co.nz/home/shows/2019/02/poll-does-climate-change-scare-you.html", "search_time_UTC": "01/01/2021 01:16:17"}
{"url": "https://www.theatlantic.com/science/archive/2015/12/what-old-weather-reports-dont-reveal-about-climate-change/419850/", "search_time_UTC": "01/01/2021 01:16:17"}
```

`urls.csv` is created from `urls.jsonl`:

- CSV with one url per line - URL + newspaper metadata,
- cleaner version of `urls.jsonl` - no duplicate URLs.

```txt
$ head -n 2 data-neu/urls.csv
url,name,fancy_name,newspaper_url,color
https://www.theguardian.com/environment/climate-consensus-97-per-cent/2017/oct/18/clifi-a-new-way-to-talk-about-climate-change,guardian,The Guardian,theguardian.com,#052962
```

Processed articles for each newspaper are stored in `articles/{$NEWSPAPER_NAME}.jsonlines`:

- text file with one JSON (article body, headline, published data),
- contains clean & processed data of the newspaper article.

```
{
  "body": "Presentations by climate scientists  in Copenhagen show that we might have underplayed the impacts of global warming in three important respects: Partly because the estimates by the Intergovernmental Panel on Climate Change (IPCC) took no account of meltwater from Greenland's glaciers, the rise in sea levels this century  as it forecast, with grave implications for coastal cities, farmland and freshwater reserves.  Two degrees of warming in the Arctic (which is heating up much more quickly than the rest of the planet)  a massive bacterial response in the soils there. As the permafrost melts, bacteria are able to start breaking down organic material that was previously locked up in ice, producing billions of tonnes of carbon dioxide and methane. This could catalyse one of the world's most powerful positive feedback loops: warming causing more warming.  Four degrees of warming  the Amazon rainforests, with appalling implications for biodiversity and regional weather patterns, and with the result that a massive new pulse of carbon dioxide is released into the atmosphere. Trees are basically sticks of wet carbon. As they rot or burn, the carbon oxidises. This is another way in which climate feedbacks appear to have been underestimated in the last IPCC report. Apart from the sheer animal panic I felt on reading these reports, two things jumped out at me. The first is that governments are relying on IPCC assessments that are years out of date even before they are published, as a result of the IPCC's extremely careful and laborious review and consensus process. This lends its reports great scientific weight, but it also means that the politicians using them as a guide to the cuts in greenhouse gases required are always well behind the curve. There is surely a strong case for the IPCC to publish interim reports every year, consisting of a summary of the latest science and its implications for global policy. The second is that we have to stop calling it climate change. Using \"climate change\" to describe events like this, with their devastating implications for global food security, water supplies and human settlements, is like describing a foreign invasion as an unexpected visit, or bombs as unwanted deliveries. It's a ridiculously neutral term for the biggest potential catastrophe humankind has ever encountered. I think we should call it \"climate breakdown\". Does anyone out there have a better idea?",
  "headline": "Time to change 'climate change' | George Monbiot | The Guardian",
  "article_name": "climate-change-copenhagen-monbiot",
  "article_url": "https://www.theguardian.com/commentisfree/2009/mar/12/climate-change-copenhagen-monbiot",
  "date_published": "2009-03-12 14:30:00",
  "article_length": 2435,
  "date_uploaded": "2022-04-18T05:21:52.382475"
}
```

`newspapers.json` contains metadata for each newspapers, such as URLs, fancy names, colors:

```json
  "guardian": {
    "name": "guardian",
    "fancy_name": "The Guardian",
    "newspaper_url": "theguardian.com",
    "color": "#052962"
  },
```

The web application uses a SQLite database `db.sqlite`:

- uses data directly from the newspaper JSONLines files,
- used by the `fastapi` webapp.

A single ZIP file is available for download `climate-news-db-dataset.zip`:

- created during webapp deployment - available at `https://www.climate-news-db.com/download`.

# Automation

The `climate-news-db` is automated through two independent workflows:

1. a `search` lambda that runs once per day, searching for `climate change` and `climate crisis` for each of the newspapers and saves the URLs to a `.jsonlines` file on S3,
2. a `scape` lambda that starts up an EC2 instance, which takes the URLs from the searching, processes them into a SQLite database and publishes the webapp to a Heroku Docker application:

The `scrape` process is automated through a cron command that runs when the EC2 instance starts up:

```crontab
SHELL=/bin/bash
@reboot bash -l -c '/home/ubuntu/climate-news-db/cron-tmux.sh'
```
