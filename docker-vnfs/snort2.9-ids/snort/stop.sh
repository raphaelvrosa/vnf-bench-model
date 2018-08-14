#!/bin/bash

sudo kill -SIGINT `ps -ef | grep snort | head -n 1 | awk '{print $2}'` 2> /dev/null

./stats.py /var/log/snort/result.yml
python ./log_intf_statistics.py /var/log/snort/result.yml

date > /var/log/snort/stop.txt
