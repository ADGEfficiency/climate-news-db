echo "url counts"
wc -l data-neu/urls.jsonl
wc -l data-neu/urls.csv
wc -l data-neu/rejected.jsonlines

echo "\narticle json files"
find data-neu/articles/ -name '*.jsonlines' | xargs -n 1 -I {} wc -l {}

python ./inspect_db.py
