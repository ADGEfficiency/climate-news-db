setup.py
handling of parse errors (currently these just return empty dict {})
parse article after download?
ability to parse a url from commandline
ability to only get urls (to stdout)
multiprocess the downloading
control of logging from CLI

logging should all happen in main - functions should return messages

refactor out get_article_url from fox.py

return error after passing {'error': 'parse error'} - check for error key in download.py

separate out the url collection from the parsing

save all dates as UTC as well

nytimes article ID has `.html`
nytimes raw html is `.html.html`

skyau - ` Image: Kym Smith / News Corp Australia ` at end of article

check google trends for the best name (climane news db, database etc)

https://blog.gdeltproject.org/a-new-contextual-dataset-for-exploring-climate-change-narratives-6-3m-english-news-urls-with-contextual-snippets-2015-2020/

ability to parse from HTML stored in RAW
- check first if raw html exsits!!

## improving the search (where to get list of urls from)

search for "climate crisis"

429 Error from google search

download button
- as csv (most useful)

## articles that are failing

guardian - https://www.theguardian.com/environment/2019/may/18/climate-crisis-heat-is-on-global-heating-four-degrees-2100-change-way-we-live (failing as it has live in it)

## parsing cleanup

'Image: Getty' occuring at the end of skyau (sometimes 'Image: Newscorp' etc)

## analytics

Mentions of 1.5 C, two degrees C etc
- how this changes over time

1C Celsius, 49C, 1.5C

## downloading smarter

ability to parse url from file

don't download if file already exists

Cleaning
- removing the BOLD BITS FROM FOX
- carbon dioxide, CO2
- degree standardization?
- not getting twitter stuff - https://www.nzherald.co.nz/sport/news/article.cfm?c_id=4&objectid=12301148

Fox
- 'Fox News Flash top headlines for May 20 are here. Check out what's clicking on Foxnews.com' - https://www.foxnews.com/science/octopuses-blind-climate-change-study
- 'CLICK HERE FOR THE FOX NEWS APP'

Add logging to the database creation

Sorting by date
- or ability to sort by column on the tables

newshub article title has ` | Newshub`

## papers

economist, aljazzera, cnn, washington post, dw.com/en, bbc, atlantic

https://www.theguardian.com/media/2020/jan/10/news-corp-employee-climate-misinformation-bushfire-coverage-email
- the australian, daily telegraph, herald sun


economist
- ■Sign up to our fortnightly climate-change newsletter hereThis article appeared in the Briefing section of the print edition under the headline "Hotting up"
- ■This article appeared in the Science & technology section of the print edition under the headline "Delayed cool"
- ■This article appeared in the The World If section of the print edition under the headline "The elephant’s U-turn"


## shortcut to downolad entire database as file

## app improvements

add number of urls onto homepage

add ability to access log (last 50 entries)

make the app work with no newspapers

formatting of datetime

most recent & oldest for each newspaper

graph of articles per year / month for newspaper pages
