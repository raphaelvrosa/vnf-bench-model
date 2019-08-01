#
# Stats2: Exports all suricata stats. Needs Python3
#
import subprocess
import json
import yaml
import flatten_json
import os
import sys

EVE_FILE = "/usr/local/var/log/suricata/eve.json"
METRIC_PREFIX = "suricata_eve_"


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
    return data_flat


def update_yml(path, data):
    old_data = dict()
    # try to load existing data
    if os.path.exists(path):
        print("Reading %r" % path)
        with open(path, "r") as f:
            old_data = yaml.load(f)
    # inject new data
    old_data.update(data)
    # write yml
    print("Writing %r" % path)
    with open(path, "w") as f:
        yaml.safe_dump(old_data, f, default_flow_style=False)


def main():
    OUTPUT = sys.argv[1]
    print("Collecting VNF statistics...")
    data = monitor_suricata_logs()
    print("Out: %s" % OUTPUT)
    update_yml(OUTPUT, data)
    print("done.")


if __name__ == "__main__":
    main()
