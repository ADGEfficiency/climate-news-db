#!/bin/sh
# DB_BUCKET=$(aws cloudformation describe-stacks --stack-name BucketStack | jq -r ".Stacks[0].Outputs[0].OutputValue")
DB_BUCKET="TODO"
# TODO restore down
litestream replicate --exec "make crawl" ./data/database.db "s3://${DB_BUCKET}/litestream"
