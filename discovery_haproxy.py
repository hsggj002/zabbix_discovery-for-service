#!/bin/env python

import re
import json


HAPROXY_ROOT = '/etc/haproxy/haproxy.cfg'
config = '%s' %HAPROXY_ROOT

p = re.compile(r'\s\bbind.*:(\d+)')

def get_haproxy_port():
    port = []

    with open(config) as f:
        for line in f:
            r = p.search(line)
            if r:
                t=r.group(1)
                port.append(t)

    return port

if __name__ == "__main__":
    
    r = {"data":[]}
    for h_port in get_haproxy_port():
        if '9000' not in h_port:
            r["data"].append({
                "{#HPORT}":h_port,
            })

    print(json.dumps(r,sort_keys=True))

