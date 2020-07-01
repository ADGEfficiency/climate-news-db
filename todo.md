setup.py
handling of parse errors (currently these just return empty dict {})
parse article after download?
ability to parse a url from commandline
ability to only get urls (to stdout)
multiprocess the downloading
control of logging from CLI

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

## papers

NZ Herald, stuff, newshub
