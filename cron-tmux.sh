#!/bin/bash -l
. /home/ubuntu/.profile
. /home/ubuntu/.bashrc
cd /home/ubuntu/climate-news-db && /usr/bin/tmux new -d -s cron-scraper
docker system prune --all --force
/usr/bin/tmux send-keys -t cron-scraper "/usr/bin/make scrape >> ~/cron-log.txt && sudo shutdown" C-m
