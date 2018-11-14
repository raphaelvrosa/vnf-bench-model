#!/bin/python

import sys
import yaml
import json
import os


def prefix_dict(d, prefix):
    r = dict()
    for k, v in d.items():
        r["%s%s" % (prefix, k)] = v
    return r 

def update_yml(path, data):
    old_data = dict()
    # try to load existing data
    if os.path.exists(path):
        print "Reading %r" % path
        with open(path, "r") as f:
            old_data = yaml.load(f)
    # inject new data
    old_data.update(data)
    # write yml
    print "Writing %r" % path
    with open(path, "w") as f:
        yaml.safe_dump(old_data, f, default_flow_style=False)


def main():
    INPUT = sys.argv[1]
    OUTPUT = sys.argv[2]
    print "Started result processing..."
    print "In:  %s" % INPUT
    print "Out: %s" % OUTPUT
    
    result = dict()

    with open(INPUT, "r") as f:    
        RAW = json.load(f)
        result["iperf_version"] = RAW.get("start").get("version")
        result.update(prefix_dict(
            RAW.get("start").get("test_start"),
            "iperf_"))
        result.update(prefix_dict(
            RAW.get("end").get("cpu_utilization_percent"),
            "iperf_cpu_"))
        result.update(prefix_dict(
            RAW.get("end").get("sum_sent"),
            "iperf_sent_"))
        result.update(prefix_dict(
            RAW.get("end").get("sum_received"),
            "iperf_received_"))

    update_yml(OUTPUT, result)
    print "done."


if __name__ == '__main__':
    main()