# Suricata Benchmarking Experiment by Paderborn University

This experiment tires to replicate the Gym experiment using the 5GTANGO [`tng-sdk-benachmark`](https://github.com/sonata-nfv/tng-sdk-benchmark) tool developed by Paderborn University.

## Folder Contents

| Folder/File | Comment |
| --- | --- |
| `peds/ped_suricata_experiment_small.yml` | Experiment definition file, used by tng-sdk-benchmark to automatically execute the benchmarking experiment (small version for quick tests, testing less parameters (< 10 experiments)). |
| `peds/ped_suricata_experiment_full.yml` | Experiment definition file, used by tng-sdk-benchmark to automatically execute the benchmarking experiment (full version for realistic benchmarking (> 36 experiment)). |
| `services/` | Folder with example network services to be benchmarked. Services are given in the [5GTANGO](https://5gtango.eu) service description format (NSD, VNFDs are aligned to ETSI). |
| `config.yml` | Configuration file for tng-sdk-benchmark defining which target machine should be used to execute the experiments. |
| `experiment-results/` | Experiment results based on `ped_suricata_experiment_full.yml` |
| `experiment-results/result_ec_metrics.csv` | Aggregated results from subfolders as Pandas CSV. This table contains all experiment metrics except of monitoring data. |
| `experiment-results/result_ts_metrics.csv` | Aggregated results from subfolders as Pandas CSV. Tis table contains the timeseries data from the Docker stats API. |
| `experiment-results/<experiment_name>-bd.yaml` | BD rendered for the particular experiment. |
| `experiment-results/<experiment_name>/` | Folder containing all the results (logs, metrics, etc.) collected by tng-sdk-benchmark during the experiment runs. |

## Workflow

The following workflow explains how to reproduce the experiments.

### Setup

You need two machines as minimal setup: The controller machine running [`tng-sdk-benchmark`](https://github.com/sonata-nfv/tng-sdk-benchmark) and the experiment execution platform running [`vim-emu`](https://osm.etsi.org/wikipub/index.php/VIM_emulator).

[This wiki page](https://osm.etsi.org/wikipub/index.php/VIM_emulator) explains how to setup and configure the system.

### Run the Experiment(s)

Once everything is installed, the following command(s) can be used to execute the experiments.

```sh
# running all experiments with a single command:
tng-bench -p peds/ped_suricata_experiment_full.yml --ibbd experiment-results/ --result-dir experiment-results/
```

After that, the results (BDs, logs, monitoring logs) will be available in `experiment-results/`.

### Result Analysis

The following step is automatically done after an experiment run. But it can also be triggered manually.
It will generate the `*.csv` files containing the aggregated metrics.

```sh
# manually trigger result processing of generated results (to create *.csv files)
tng-bench-result -rd experiment-results/  
```


### Result Archive

We archive all (even broken) results in UPB's GitLab: https://git.cs.upb.de/peuster/tng-bench-result-archive


