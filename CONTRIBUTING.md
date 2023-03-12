# Adding a Newspaper

/Users/adam/climate-news-db/climatedb/spiders/daily_post_nigeria.py
Create a new spider

/Users/adam/climate-news-db/climatedb/databases.py
Hack into `get_urls_for_paper` to get urls into the spider for development

```
def get_urls_for_paper(paper: str, return_all=False) -> List[str]:
    """Gets all urls for a newspaper from $(DATA_HOME) / urls.csv"""
    return [
        "https://nation.africa/kenya/health/can-we-climb-out-of-this-hole-the-climate-crisis-of-our-times-4003530",
        "https://nation.africa/kenya/blogs-opinion/editorials/intensify-efforts-to-fight-climate-change-crisis-4050092"
    ]
```
Develop your spider using

```
make scrape-one PAPER=daily_post_nigeria
```

Need to be careful about putting urls into `rejected.jsonl`

Then big manual search 

/Users/adam/climate-news-db/climatedb/search.py

This will put urls into `url.jsonl`

You then need to run `create_urls_csv.py` - make sure to *unhack* `get_urls_for_paper`
