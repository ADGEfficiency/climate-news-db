# climate-news-db

A database of climate change news articles - [use the dataset here](http://www.climate-news-db.com/).

The goal of the `climate-news-db` is to provide a dataset for NLP and climate change media researchers.


## Dataset

The database is made up of a number of data structures (such as JSONLines text files or a SQLite database).

You can [download all the data](https://www.climate-news-db.com/download) using the webapp.

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
```

`urls.jsonl`

- text file with one JSON (url, scrape time) per line,
- these urls are raw & dirty - often have duplicates,
- each day a serverless function on AWS Lambda searches all newspapers for the terms `climate change` and `climate crisis`,
- search result URLs are appended to `urls.jsonl`.

`urls.csv`

- CSV with one url per line - URL + newspaper metadata,
- cleaner version of `urls.jsonl` - no duplicate URLs,
- created from `urls.jsonl`.

`articles/{$NEWSPAPERID}.jsonlines`

- text file with one JSON (article body, headline, published data),
- contains clean & processed data of the newspaper article.

A single line of a newspaper JSONLines file:

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

`db.sqlite`

- SQLite database,
- uses data directly from the newspaper JSOLines files,
- used by the `fastapi` webapp.

`climate-news-db-dataset.zip`

- created during webapp deployment - available at `https://www.climate-news-db.com/download`.
