#!/bin/python

import sys
import yaml
import os


USE_KEYS = [
    ("Server Software", "ab_srv_version", "string"),
    ("Server Hostname", "ab_srv_host", "string"),
    ("Server Port", "ab_srv_port", "integer"),
    ("Document Path", "ab_doc_path", "string"),
    ("Document Length", "ab_doc_length", "integer"),
    ("Concurrency Level", "ab_concurrent_lvl", "integer"),
    ("Time taken for tests", "ab_time_used_s", "float"),
    ("Complete requests", "ab_completed_requests", "integer"),
    ("Failed requests", "ab_failed_requests", "integer"),
    ("Total transferred", "ab_total_transfer_byte", "integer"),
    ("HTML transferred", "ab_html_transfer_byte", "integer"),
    ("Requests per second", "ab_request_per_second", "float"),
    ("Time per request", "ab_mean_time_per_request", "float"),
    ("Transfer rate", "ab_transfer_rate_kbyte_per_second", "float")
]

def process_line(l):
    for k in USE_KEYS:
        if k[0] in l:
            return parse_line(l, k[1], k[2])
    return None, None


def parse_line(l, k, typ):
    try:
        p = l.split(":")
        value = p[1].split()[0]
        if typ == "integer":
            value = int(value)
        elif typ == "float":
            value = float(value)
    except Exception, e:
        value = None
    return k, value


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

def add_rt_distribution_data(path, r):
    """
    Try to find distribution data and add it if available
    """
    try:
        with open(path, "r") as f:
            csv = f.read()
            csv = csv.replace("\n",";")
        #print csv
        r["ab_rt_distribution"] = csv
    except:
        pass

def main():
    INPUT = sys.argv[1]
    OUTPUT = sys.argv[3]
    DIST_INPUT = sys.argv[2]
    print "Started result processing..."
    print "In:  %s" % INPUT
    print "Out: %s" % OUTPUT
    
    result = dict()

    with open(INPUT, "r") as f:    
        for l in f.readlines():
            k, v =  process_line(l)
            if k is not None:
                print "%s = %r" % (k, v)
                result[k] = v
    add_rt_distribution_data(DIST_INPUT, result)
    update_yml(OUTPUT, result)
    print "done."


if __name__ == '__main__':
    main()
