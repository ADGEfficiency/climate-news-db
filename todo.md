logging should all happen in main - functions should return messages
return error after passing {'error': 'parse error'} - check for error key in download.py
handling of parse errors (currently these just return empty dict {})

move urls.data into the repo

stripping of html from article id

refactor out get_article_url from fox.py

add most recent article on home page

improve error handling & logging

put a line at the bottom before the footer

## download refactor and optimization

- ability to parse a url from commandline 
- multiprocess the downloading
save all dates as UTC as well


https://towardsdatascience.com/current-google-search-packages-using-python-3-7-a-simple-tutorial-3606e459e0d4

## newspaper cleanuv

nytimes article ID has `.html`
nytimes raw html is `.html.html`

skyau - ` Image: Kym Smith / News Corp Australia ` at end of article
'Image: Getty' occuring at the end of skyau (sometimes 'Image: Newscorp' etc)

Cleaning
- carbon dioxide, CO2
- degree standardization?
- not getting twitter stuff - https://www.nzherald.co.nz/sport/news/article.cfm?c_id=4&objectid=12301148

Fox
- 'Fox News Flash top headlines for May 20 are here. Check out what's clicking on Foxnews.com' - https://www.foxnews.com/science/octopuses-blind-climate-change-study
- 'CLICK HERE FOR THE FOX NEWS APP'

newshub article title has ` | Newshub`

economist

- ■Sign up to our fortnightly climate-change newsletter hereThis article appeared in the Briefing section of the print edition under the headline "Hotting up"
- ■This article appeared in the Science & technology section of the print edition under the headline "Delayed cool"
- ■This article appeared in the The World If section of the print edition under the headline "The elephant’s U-turn"

aljazzera

- some articles missing ld/json
- these also have a different html structure (text section)

cnn

- p tags at the end with links to other articles (different styling)


## app upgrades

Sorting by date
- or ability to sort by column on the tables

## shortcut to downolad entire database as file

## app improvements

want to see the

add number of urls onto homepage (or onto an admin page?)

add ability to access log (last 50 entries)

make the app work with no newspapers

formatting of datetime

most recent & oldest for each newspaper

graph of articles per year / month for newspaper pages

## integrate other datasets

https://blog.gdeltproject.org/a-new-contextual-dataset-for-exploring-climate-change-narratives-6-3m-english-news-urls-with-contextual-snippets-2015-2020/

https://climatefeedback.org/

## improving the search (where to get list of urls from)

search for "climate crisis"

429 Error from google search

download button
- as csv (most useful)

## analytics

Mentions of 1.5 C, two degrees C etc
- how this changes over time

1C Celsius, 49C, 1.5C

Add logging to the database creation

### ml uses

clustering

question answering (?)

## data collection

add description ? (can be in ld/json)

## papers

https://www.theguardian.com/media/2020/jan/10/news-corp-employee-climate-misinformation-bushfire-coverage-email

- the australian (hard - need selenium)
- daily telegraph AUS (hard - need selenium)
- herald sun (hard - need selenium)
- telegraph uk (paywall)
- the times uk (paywall)
- the sun
- Mail, Express, Sun and Telegraph

collect analytics on the s3 syncs (num uploads, deletes etc)

---

add a num articles added in last 5 days column to home page
- force me to update :)

refactor registry & utils up a level

things learnt
- put sanity checks on cleaned data (body certain length, headline not missing etc)

possibel to get non-unique article id's
