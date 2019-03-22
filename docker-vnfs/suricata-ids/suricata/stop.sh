#!/bin/bash

kill -SIGINT `ps -ef | grep suricata | head -n 1 | awk '{print $2}'` 2> /dev/null

rm -f /usr/local/var/run/suricata.pid

sleep 2

# Gym
./stats.py /usr/local/var/log/suricata/result.yml
python ./log_intf_statistics.py /usr/local/var/log/suricata/result.yml
# tng-bench (needs results in different folder)
cp /usr/local/var/log/suricata/suricata.log /tngbench_share/
cp /usr/local/var/log/suricata/*.yml /tngbench_share/
cp /usr/local/var/log/suricata/*.json /tngbench_share/

date > /usr/local/var/log/suricata/stop.txt
