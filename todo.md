parse not being tested (error on )
```
  parse_url(url['url'], replace=replace, lgr=lgr)
File "/Users/adam/climate-news-db/climatedb/parse.py", line 70, in main
  exists = final.exists('article_id', article_id)
TypeError: exists() takes 2 positional arguments but 3 were given
```

way failing on exi

part of code not being tested

different way engine.exists(value) works versus database.exists(key, value) etc

---

Sort out the 1970!

Analyse failed article parsing

tool to remove rejected urls from urls.json

Test the datetime conversions...

Point towards data science south

Put link to download database as csv

## what is a service?
- searching,
- parsing,
- collecting (?) what is collecting

collect does
- search or get all urls from urls_db,
- check exists,
- limit num,
- if parse

parse does
- run parse,
- handle errors,
- checks articles,
- cleans articles,
- saves parsed (should be saved articles)

for parse - change parsed_articles into only articles

HTMLfolder should be a database?
- same level as JSONFolder


---

# RULES

- everything in JSON
- all times UTC
- all logging / error handling in main
- only parse date published
- fail and keep going

# GOALS

## TESTS

END TO END - without google - check collect & parse from static urls

UNIT - databases, engines

## MIGRATION TOOLING

- check urls, fix ids, fix .html

URLS
- urls.json -> sqlite

ARTICLES
- regenerate articles from raw html -> json OR sqlite

# next time

Unit of work for collecting & parsing?

Check errors being passed back into logs

Should I remove urls that fail check from urls.jsonl - yes

---

# app
questions the app should answer
- how many articles added in last day to urls.data
- how many in raw not in finished, how many in urls.data not in db etc

add most recent article on home page
- add a num articles added in last 5 days column to home page

put a line at the bottom before the footer
See latest added

Sorting by date
- or ability to sort by column on the tables

shortcut to downolad entire database as file

add number of urls onto homepage (or onto an admin page?)

add ability to access log (last 50 entries)

make the app work with no newspapers

formatting of datetime

most recent & oldest for each newspaper

graph of articles per year / month for newspaper pages



# next time

- ability to parse a url from commandline 
- multiprocess the downloading

Cleaning
- carbon dioxide, CO2
- degree standardization?
- not getting twitter stuff - https://www.nzherald.co.nz/sport/news/article.cfm?c_id=4&objectid=12301148

## integrate other datasets

https://blog.gdeltproject.org/a-new-contextual-dataset-for-exploring-climate-change-narratives-6-3m-english-news-urls-with-contextual-snippets-2015-2020/

https://climatefeedback.org/

## improving the search (where to get list of urls from)

search for "climate crisis"

429 Error from google search


## analytics

Mentions of 1.5 C, two degrees C etc
- how this changes over time

1C Celsius, 49C, 1.5C

Add logging to the database creation

### ml uses

clustering

question answering (?)

things learnt
- put sanity checks on cleaned data (body certain length, headline not missing etc)

