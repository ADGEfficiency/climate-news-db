#!/bin/sh

echo ':wave: Hello from the climate-news-db'  | gum format -t emoji

PAPERS=$(cat newspapers.json | jq '.[].name' -r | tac)
gum style "select a paper:" --foreground 2
PAPER=$(gum choose $PAPERS)
clear
echo "$(gum style 'paper:' --foreground 2) $PAPER"

gum style "select a query:" --foreground 2
QUERY=$(gum choose "climate change" "climate crisis")
clear
echo "$(gum style "paper:" --foreground 2) $PAPER $(gum style "query:" --foreground 2) $QUERY"

gum style "select a number to search:" --foreground 2
NUM=$(gum input --value 5 --prompt "number to search for: ")
clear
echo "$(gum style "paper:" --foreground 2) $PAPER $(gum style "query:" --foreground 2) $QUERY $(gum style "num:" --foreground 2) $NUM"

python ./climatedb/search.py "$PAPER" "$QUERY" "$NUM"
