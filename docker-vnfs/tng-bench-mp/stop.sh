#! /bin/bash
#
# NOTE: using the iperf.json backup copy is needed because iperf3 server skews up the json file during its terminataion
#

cp  /mnt/share/iperf.json  /mnt/share/iperf.json.bak
pkill iperf3
pkill ab

sleep 1
cp  /mnt/share/iperf.json.bak  /mnt/share/iperf.json

# process snort.stats and create result.yml
python /process_ab_results.py /mnt/share/ab.log /mnt/share/rt_dist.csv /mnt/share/result.yml
python /process_boom_results.py /mnt/share/boom.json /mnt/share/result.yml
python /process_httping_results.py /mnt/share/httping.log /mnt/share/result.yml
python /process_iperf3_results.py /mnt/share/iperf.json /mnt/share/result.yml
python /log_intf_statistics.py /mnt/share/result.yml

date > /mnt/share/stop.txt
