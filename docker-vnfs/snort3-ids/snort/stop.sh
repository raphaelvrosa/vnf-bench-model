#! /bin/bash

# pkill snort
kill -SIGINT `ps -ef | grep snort | head -n 1 | awk '{print $2}'` 2> /dev/null

sleep 2

# copy stats files
cp *.csv /mnt/share/

# process snort.stats and create result.yml
python processresults.py /mnt/share/snort.log /mnt/share/result.yml
python /log_intf_statistics.py /mnt/share/result.yml

date > /mnt/share/stop.txt
