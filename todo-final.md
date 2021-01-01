Unit of work for collecting & parsing?

---

# RULES

- everything in JSON
- all times UTC
- all logging / error handling in main
- only parse date published

# GOALS

## SCRAPING & PARSING
- fail safely
- sqlite database
- tools to analyze logs

## Clean all 16 newspapers

## APP
- see last article added

## TESTS

END TO END - without google - check collect & parse from static urls

UNIT - databases, engines

## MIGRATION TOOLING
- check urls, fix ids, fix .html

URLS
- urls.data -> urls.json
- urls.json -> sqlite

ARTICLES
- regenerate articles from raw html -> json OR sqlite
