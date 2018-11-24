#!/bin/python

import sys
import yaml
import os
import json


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
        d = json.load(f)
        for k, v in d.items():
            result["boom_%s" % k] = v

    update_yml(OUTPUT, result)
    print "done."


if __name__ == '__main__':
    main()
