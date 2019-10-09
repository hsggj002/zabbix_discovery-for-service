#!/bin/env python                                                                                                                                                                                                       [25/1855]

import re
import os
import json

p = re.compile(r'src.*port = (\d+)')

def get_flume_port(name):
    port = []
    with open(name) as f:
        for line in f:
            r=p.search(line)
            if r:
                t=r.group(1)
                port.append(t)
    return port

def get_flume():
    files = []
    l = [x for x in os.listdir("/opt/zyz/flume") if os.path.isdir("/opt/zyz/flume/%s" %x)]
    for i in l:
        files.append(i)

    return files

def get_flume_dir():
    files = []
    l = [x for x in os.listdir("/opt/flume") if os.path.isdir("/opt/flume/%s" %x)]
    for i in l:
        files.append(i)

    return files
    
def get_flume_name():
    files_name = ["flume-app.conf","flume-center-mem.conf","flume.conf","flume-brandsafe.conf","flume-backup.conf"]

    FLUME_ROOT = '/opt/zyz/flume'
    files = []
    ports = {}
    ports2 = {}
    for dir_name in get_flume():
        for file_name in files_name:
            if os.path.exists("%s/%s/conf/%s" %(FLUME_ROOT,dir_name,file_name)):
                files.append("%s/%s/conf/%s" %(FLUME_ROOT,dir_name,file_name))
    for file_path in files:
        file = get_flume_port(file_path)
        for file_port in file:
            if file_port:
                ports[file_port]=file_path.split('/')[-1].split('.')[0]

    return ports

if __name__ == "__main__":

    r = {"data": []}
    ports = ['4464','4445','4446','4447','4448','4451','4452']
    for file_port in get_flume_name():
        if file_port not in ports:
            r["data"].append({"{#SNAME}": get_flume_name()[file_port],
                              "{#SPORT}": file_port})
    print(json.dumps(r, sort_keys=True))
