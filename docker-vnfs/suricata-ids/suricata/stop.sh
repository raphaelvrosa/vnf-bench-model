#!/bin/bash

kill -SIGINT `ps -ef | grep suricata | head -n 1 | awk '{print $2}'` 2> /dev/null

rm -f /usr/local/var/run/suricata.pid

sleep 2

./stats.py /usr/local/var/log/suricata/result.yml
python ./log_intf_statistics.py /usr/local/var/log/suricata/result.yml

date > /usr/local/var/log/suricata/stop.txt
