#!/bin/bash
# run snort without additional outputs
#snort -i br0 -N -K none > snort.log 2>&1 &

pkill snort
sleep 1

# run snort as background process (snort2)
#snort -i br0 -D -q -k none -K ascii -l /mnt/share -A fast -c /etc/snort/snort.conf > /mnt/share/snort.log
#snort -i br0 -D -k none -K ascii -l /mnt/share -A fast -c /etc/snort/snort.conf -Z /mnt/share/snort.stat > /mnt/share/snort.log
#snort -Q -i input:output -D -k none -K ascii -l /mnt/share -A fast -c /etc/snort/snort.conf > /mnt/share/snort.log

# run snort as background process (snort3)
# -z = max number of pkt threads
./snort -i br0 -D -z 1 -k none -c snort.lua > /mnt/share/snort.log 2>&1 &

echo "Snort VNF started ..."
