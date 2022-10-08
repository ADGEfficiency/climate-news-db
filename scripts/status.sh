echo "url counts"
wc -l data-neu/urls.jsonl
wc -l data-neu/urls.csv

echo "article json files"
find data-neu/articles/ -name '*.jsonlines' | xargs -n 1 -I {} wc -l {}
