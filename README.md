# climate-news-db

Database of climate change news articles - [see the dataset here](http://www.climate-news-db.com/).


## Data Structures

data/$urls.txt

- text file with one url per line
- these urls are dirty


data/articles/$(NEWSPAPER_ID)/$(ARTICLE_ID).{json,html}

- stage = [raw, processed]
- newspaper_id
- article_id

