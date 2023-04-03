#!/bin/sh

hi () {
echo ':wave: Hello from the climate-news-db'  | gum format -t emoji
}

hi
PAPERS=$(cat newspapers.json | jq '.[].name' -r | tac)
gum style "select a paper:" --foreground 2
PAPER=$(gum choose $PAPERS)
clear

hi
echo "$(gum style 'paper:' --foreground 2) $PAPER"

gum style "select a number to search:" --foreground 2
NUM=$(gum input --value 5 --prompt ">>> ")
clear

hi
for QUERY in "climate change" "climate crisis"; do
  python ./climatedb/search.py "$PAPER" "$QUERY" "$NUM"
done
