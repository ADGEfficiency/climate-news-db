# goals

- S3 only for backups, not for version control
- log database & S3 use
- fail and keep going

functionality
- regenerate from json (should only ever be one reason to regenerate the json)


# tasks

Create a dataclass for the primitives
- so can write data as row
- is the dataclass same schema as the db?
- first goal = generate a urls table with all urls loaded from urls.data

Clean all 16 newspapers

Refactor registry & utils up a level

All Db times should be UTC
- created on


# code quality

logging should all happen in main - functions should return messages
return error after passing {'error': 'parse error'} - check for error key in download.py
handling of parse errors (currently these just return empty dict {})
refactor out get_article_url from fox.py
collect analytics on the s3 syncs (num uploads, deletes etc)


# data
Possible to get non-unique article id's
move urls.data into the repo
stripping of html from article id
multiple copies of raw data, because of the use of delete
store all urls found
save all dates as UTC as well

test using database mocks!

## urls.data

something better to manage urls.data - want an additional level of raw data, that's always stored

order of urls.data is being corrupted by the set
- maybe urls.data should have time stamps

ability to check urls.data only
- for what?

Regenerate urls.data from raw

# scraping

add description ? (can be in ld/json)

not redownloading if already there


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

