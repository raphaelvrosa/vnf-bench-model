#
# Quick and dirty prometheus exporter.
#
import subprocess
import time
import json
import flatten_json
import os
from prometheus_client import Gauge
from prometheus_client import start_http_server as start_export_http_server

EVE_FILE = "/usr/local/var/log/suricata/eve.json"
#EVE_FILE = "test_eve.json"
SLEEP_TIME = 2
METRIC_PREFIX = "suricata_"
TIMESTAMP_KEY = METRIC_PREFIX + "timestamp"
PROMETHEUS_EXPORTER_PORT = 9089

METRIC_REGISTRY = dict()
NETWORK_INTERFACES = ["input", "output"]


def update_metric(metric, value):
    try:
        value = float(value)
        if metric not in METRIC_REGISTRY:
            METRIC_REGISTRY[metric] = Gauge(metric, "Auto exported Suricata metric")
        METRIC_REGISTRY[metric].set(value)
        print("Prometheus exporter set numeric metric '{}' to {}".format(metric, value))
    except BaseException as ex:
        print(ex)


def monitor_suricata_logs():
    data = dict()
    try:
        # efficiently get and parse last line from EVE_FILE
        line = subprocess.check_output(['tail', '-1', EVE_FILE])
        data = json.loads(line.decode("utf-8"))
    except BaseException as ex:
        print(ex)
    data_flat = flatten_json.flatten(data)
    data_flat = {METRIC_PREFIX + k: v for k, v in data_flat.items()}
    for k, v in data_flat.items():
        if k != TIMESTAMP_KEY:
            update_metric(k, v)


def monitor_network_stats(interfaces):
    value = -1
    for i in interfaces:
        for m in ["rx_bytes", "rx_packets", "tx_bytes", "tx_packets"]:
            try:
                # efficiently get and parse last line from EVE_FILE
                line = subprocess.check_output(
                    ["cat",
                     "/sys/class/net/{}/statistics/{}".format(i, m)])
                value = int(line)
            except BaseException as ex:
                print(ex)
            update_metric("vnf_network_{}_{}".format(i, m), value)


def monitor_custom_stats():
    value = -1
    for f in ["/tngbench_share/ruleset.log"]:
        try:
            line = subprocess.check_output(
                ["cat", "{}".format(f)])
            value = float(line)
        except BaseException as ex:
            print(ex)
        m = os.path.basename(f)
        m = m.replace(".log", "")
        m = m.replace("/", "")
        update_metric("vnf_custom_{}".format(m), value)


def main():
    # start exporter server
    start_export_http_server(PROMETHEUS_EXPORTER_PORT)
    # start scraping the EVE_FILE
    while True:
        monitor_suricata_logs()
        monitor_network_stats(NETWORK_INTERFACES)
        monitor_custom_stats()
        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()