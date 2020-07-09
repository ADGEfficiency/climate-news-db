setup.py
handling of parse errors (currently these just return empty dict {})
parse article after download?
ability to parse a url from commandline
ability to only get urls (to stdout)
multiprocess the downloading
control of logging from CLI

return error after passing {'error': 'parse error'} - check for error key in download.py

separate out the url collection from the parsing


save all dates as UTC as well

nytimes article ID has `.html`

ability to parse from HTML stored in RAW
- check first if raw html exsits!!

## improving the search (where to get list of urls from)

search for "climate crisis"

429 Error from google search


## articles that are failing

guardian - https://www.theguardian.com/environment/2019/may/18/climate-crisis-heat-is-on-global-heating-four-degrees-2100-change-way-we-live (failing as it has live in it)

## parsing cleanup

'Image: Getty' occuring at the end of skyau (sometimes 'Image: Newscorp' etc)

## analytics

Mentions of 1.5 C, two degrees C etc
- how this changes over time

## downloading smarter

ability to parse url from file

don't download if file already exists

Cleaning
- removing the BOLD BITS FROM FOX
- carbon dioxide, CO2
- degree standardization?
- not getting twitter stuff - https://www.nzherald.co.nz/sport/news/article.cfm?c_id=4&objectid=12301148

Add logging to the database creation

## papers

stuff, newshub


## shortcut to downolad entire database as file


## article quality

pictures

## app improvements

add number of urls onto homepage

add ability to access log (last 50 entries)

make the app work with no newspapers
