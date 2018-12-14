# Suricata Benchmarking Experiment by Paderborn University

This experiment tires to replicate the Gym experiment using the 5GTANGO [`tng-sdk-benachmark`](https://github.com/sonata-nfv/tng-sdk-benchmark) tool developed by Paderborn University.

## Folder Contents

| Folder/File | Comment |
| --- | --- |
| `ped_suricata_experiment_small.yml` | Experiment definition file, used by tng-sdk-benchmark to automatically execute the benchmarking experiment (small version for quick tests, testing less parameters). |
| `ped_suricata_experiment_full.yml` | Experiment definition file, used by tng-sdk-benchmark to automatically execute the benchmarking experiment (full version for realistic benchmarking). |
| `nw-services/` | Folder with example network services to be benchmarked. Services are given in the [5GTANGO](https://5gtango.eu) service description format (NSD, VNFDs are aligned to ETSI). |
| `config.yml` | Configuration file for tng-sdk-benchmark defining which target machine should be used to execute the experiments. |
| `results/` | Folder containing all the results (logs, metrics, etc.) collected by tng-sdk-benchmark during the experiment runs. |

## Usage

TODO