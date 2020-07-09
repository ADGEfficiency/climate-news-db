#!/usr/bin/env bash

echo "$(ls -R ~/climate-nlp/final | wc -l) articles locally"
echo "$(cat ~/climate-nlp/urls.data | wc -l) urls in url.data"
echo " "
echo "First five articles in ~/climate-nlp/final:"
echo " "
echo "$(tree ~/climate-nlp/final | head -n 5)"
