#!/usr/bin/env bash
PAPER=$1
ARTICLE=$2
echo "$1 $2"
rm ~/climate-news-db/raw/$1/$2*
rm ~/climate-news-db/final/$1/$2*
