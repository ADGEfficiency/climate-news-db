#!/bin/bash -l
. /home/ubuntu/.profile
. /home/ubuntu/.bashrc
cd /home/ubuntu/climate-news-db && /usr/bin/tmux new -d -s cron-scraper
/usr/bin/tmux send-keys -t cron-scraper "/usr/bin/make scrape; sudo shutdown" C-m
