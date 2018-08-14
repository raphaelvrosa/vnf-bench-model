#!/bin/bash
rm -rf /var/log/snort/*

date > /var/log/snort/start.txt

# remove IPs from input/output interface to prepare them for bridging
ip addr flush dev $IFIN
ip addr flush dev $IFOUT

# bridge interfaces (layer 2) and let snort listen to bridge (IDS mode)
brctl addbr br0
brctl addif br0 $IFIN $IFOUT
ifconfig br0 up

ethtool -K br0 gro off

ifconfig br0 promisc

snort -i br0 -c /etc/snort/snort.conf -D > /var/log/snort.stats 2>&1 &

echo "Snort VNF started ..."

# if [ -z $1 ]; then
# 	snort -i ens4 -c /etc/snort/snort.conf
# elif [ $1 == "b" ]; then
# 	snort -i ens4 -c /etc/snort/snort.conf -D
# fi
