logging should all happen in main - functions should return messages
return error after passing {'error': 'parse error'} - check for error key in download.py
handling of parse errors (currently these just return empty dict {})

move urls.data into the repo

stripping of html from article id

refactor out get_article_url from fox.py

add most recent article on home page

improve error handling & logging

put a line at the bottom before the footer

what do i want from new system
- use S3 only for backups, not for version control
- stop storing 
- use a proper database
- regenerate from json (should only ever be one reason to regenerate the json)

build proper tooling to inspect what is going on where

order of urls.data is being corrupted by the set
- maybe urls.data should have time stamps

multiple copies of raw data, because of the use of delete

rework
- check parts of url to not get the section pages
- something better to manage urls.data - want an additional level of raw data, that's always stored
- ability to regenerate urls.data from this raw data by only checking
- store all urls found
- not redownloading if already there

rework functionality
- fail and keep going
- ability to check urls.data only
- store all raw data, to regenerate urls.data from raw

newspaper metadata
- owner, date founded etc



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
- https://www.economist.com/news/2020/04/24/the-economists-coverage-of-climate-change REDIRECTS

- ■Sign up to our fortnightly climate-change newsletter hereThis article appeared in the Briefing section of the print edition under the headline "Hotting up"
- ■This article appeared in the Science & technology section of the print edition under the headline "Delayed cool"
- ■This article appeared in the The World If section of the print edition under the headline "The elephant’s U-turn"

aljazzera

- some articles missing ld/json
- these also have a different html structure (text section)
- redirects are killing me (https://www.aljazeera.com/news/2020/02/democratic-primaries-climate-change-key-issue-voters-200210152832900.html)

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

---

bbc future

https://www.bbc.com/future/article/20200618-climate-change-who-is-to-blame-and-why-does-it-matter
https://www.bbc.com/future/article/20200521-planting-trees-doesnt-always-help-with-climate-change
https://www.bbc.com/future/article/20200706-the-law-that-could-make-climate-change-illegal
https://www.bbc.com/future/tags/climatechange
https://www.bbc.com/future/article/20200624-has-covid-19-brought-us-closer-to-stopping-climate-change
https://www.bbc.com/future/article/20200421-what-lockdown-loneliness-taught-me-about-climate-change
https://www.bbc.com/future/smart-guide-to-climate-change

bbc avA

https://www.bbc.com/news/av/world-australia-51369140
https://www.bbc.com/news/av/science-environment-34555220
https://www.bbc.com/news/av/science-environment-47575165
https://www.bbc.com/news/av/science-environment-45792942
https://www.bbc.com/news/av/science-environment-50396797
https://www.bbc.com/news/av/science-environment-48917148
https://www.bbc.com/news/av/world-africa-50976829/climate-change-has-brought-parts-of-zambia-to-the-brink-of-famine?ocid=wsnews.chat-apps.in-app-msg.whatsapp.trial.link1_.auin
https://www.bbc.com/news/av/uk-48018034
https://www.bbc.com/news/av/science-environment-49643353
https://www.bbc.com/news/av/uk-51667018
https://www.bbc.com/news/av/uk-47972979
https://www.bbc.com/news/av/world-asia-49854753
https://www.bbc.com/news/av/science-environment-45792362
https://www.bbc.com/news/av/science-environment-51129250/our-planet-matters-climate-change-explained
https://www.bbc.com/news/av/world-us-canada-33764762
https://www.bbc.com/news/av/science-environment-46496140
https://www.bbc.com/news/av/world-46381529
https://www.bbc.com/news/av/science-environment-44642147
https://www.bbc.com/news/av/science-environment-48858692

atlantic video
https://www.theatlantic.com/video/index/394583/nunavut-hunter-gatherer-society-runs-out-food/
https://www.theatlantic.com/video/index/561587/tangier-island/
https://www.theatlantic.com/video/index/602995/disaster-capitalism/
https://www.theatlantic.com/video/index/599635/dry-town-central-valley/
https://www.theatlantic.com/video/index/379787/how-will-climate-change-transform-us-cities/
https://www.theatlantic.com/video/index/559790/jeff-vandermeer/
https://www.theatlantic.com/video/index/508508/climate-change-and-child-marriage/
https://www.theatlantic.com/video/index/515667/how-would-immortality-change-the-way-we-live/
https://www.theatlantic.com/video/index/414118/whats-the-best-tool-we-have-to-stop-environmental-disaster/
https://www.theatlantic.com/video/index/597139/hinkley-point/
https://www.theatlantic.com/video/index/605146/dulce/
https://www.theatlantic.com/video/index/591832/climate-refugees/
https://www.theatlantic.com/video/index/389144/80-to-90-ft/
https://www.theatlantic.com/video/index/519000/the-russian-scientists-bringing-back-the-ice-age/
https://www.theatlantic.com/video/index/278548/whos-to-blame-for-climate-change/
