#!/bin/bash
set -e

target_repo=${1-mpeuster}

docker build -t $target_repo/tng-bench-mp -f tng-bench-mp/Dockerfile tng-bench-mp
docker build -t $target_repo/vnf-ids-suricata -f suricata-ids/Dockerfile suricata-ids
docker build -t $target_repo/vnf-calibration-stress -f stress-calibration/Dockerfile stress-calibration
