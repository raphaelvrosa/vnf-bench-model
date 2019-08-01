#!/bin/bash
date > /usr/local/var/log/suricata/start.txt

# remove IPs from input/output interface to prepare them for bridging
ip addr flush dev $IFIN
ip addr flush dev $IFOUT

ifconfig $IFIN promisc
ifconfig $IFOUT promisc

# bridge interfaces (layer 2) and let snort listen to bridge (IDS mode)
brctl addbr br0
brctl addif br0 $IFIN $IFOUT
ifconfig br0 up

ethtool -K br0 gro off

ifconfig br0 promisc

rm -f /usr/local/var/run/suricata.pid
rm -rf /usr/local/var/log/suricata/*

echo "Starting Promethues exporter..."
python3 prometheus_exporter.py &#> exporter.log &

echo "Starting Suricata on interface br0 ..."
if [ -z $1 ]; then
	suricata -c /usr/local/etc/suricata/suricata-ids.yaml --af-packet -D
    echo "99" > /tngbench_share/ruleset.log
    echo "Suricata VNF started - AVG ruleset ..."
elif [ $1 == "small_ruleset" ]; then
	suricata -c /usr/local/etc/suricata/suricata-ids-small.yaml --af-packet -D
    echo "0" > /tngbench_share/ruleset.log
    echo "Suricata VNF started - SMALL ruleset ..."
elif [ $1 == "big_ruleset" ]; then
	suricata -c /usr/local/etc/suricata/suricata-ids-big.yaml --af-packet -D
    echo "1" > /tngbench_share/ruleset.log
    echo "Suricata VNF started - BIG ruleset ..."
elif [ $1 == "empty" ]; then
    echo "Suricata VNF NOT started ..."
fi
