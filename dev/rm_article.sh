#!/usr/bin/env bash
PAPER=$1
ARTICLE=$2
echo "$1 $2"
rm ~/climate-news-db-data/raw/$1/$2*
rm ~/climate-news-db-data/final/$1/$2*
