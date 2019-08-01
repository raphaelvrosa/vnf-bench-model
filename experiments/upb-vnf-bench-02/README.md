# Suricata Benchmarking Experiment by Paderborn University

This experiment will be used to compare Gym and the 5GTANGO [`tng-sdk-benachmark`](https://github.com/sonata-nfv/tng-sdk-benchmark) tool developed by Paderborn University.

## Experiment Definition

According to call on 2019-07-25:

- VNF: Suricata IDS
- parameters:
    - cpu_bw 0.1 - 1.0, step 0.1
    - core pinnig (1 core per container)
    - memory: 1024MB
    - rulset: empty, small, large
    - low sizes (pcaps): smallFlows, bugFlows (tcpreplay -i data -tK --loop 1000)
    - repetitions: 10
    - round time (measurement of one config): 30 seconds
- recorded metrics:
    - suricata_bytes
    - suricata_dropped
    - suricate_drops
    - suricata_packets


## Experiment Execution

```sh
tng-bench -p peds/upb-vnf-bench-02-01.yml --no-prometheus  --ibbd results
```