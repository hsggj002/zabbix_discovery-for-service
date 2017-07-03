#!/bin/env python

import os
import re
import json

p = re.compile(r'(?<=djport=")[0-9].*(?="$)')

pat = '/etc/init.d'

def get_swoole_port(arg):
    port_list = []
    port_list1 = []

    config = "%s/%s" %(pat,arg)
    with open(config) as f:
        for line in f:
            r = p.search(line)
            if r:
                port_list.append(r.group())
                for i in port_list:
                    for j in i.split(','):
                        port_list1.append(j)

    return port_list1

def get_swoole_base():
    l1 = os.listdir(pat)
    fi = [x for x in l1 if x.startswith('dj')]

    return fi

if __name__ =="__main__":
    r = {"data":[]}
    for s_name in get_swoole_base():
        s_port = get_swoole_port(s_name)
        for i in s_port:
            r["data"].append({
                "{#SNAME}":s_name,
                "{#SPORT}":i,
            })

    print(json.dumps(r,sort_keys=True))