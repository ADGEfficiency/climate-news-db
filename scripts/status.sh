echo "url counts"
wc -l data/urls/urls.data
wc -l data/urls/urls.jsonl

echo "raw html files"
find data/articles/raw -name '*.html' | wc -l
echo "article json files"
find data/articles/final -name '*.json' | wc -l
