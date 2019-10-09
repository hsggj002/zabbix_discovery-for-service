#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import os
import json

def get_docker_service():
    service={}
    with os.popen('docker service ls') as d_service:
        count=1
        for i in d_service:
            if "ID" not in i:
                service[count]=' '.join(i.split()).split(' ')
                count+=1
    return service

def get_docker_json():
    r={'data':[]}
    for i in get_docker_service():
        r['data'].append({"{#NAME}":get_docker_service()[i][1],
                          "{#REPLICAS}":get_docker_service()[i][3]})

    print(json.dumps(r, sort_keys=True))

def status(name):
    for i in get_docker_service():
        if name in get_docker_service()[i]:
            data = get_docker_service()[i][3].split('/')
            if int(data[1])/2>int(data[0]):
                print 0
            else:
                print 1

if __name__ == '__main__':
    try:
            name = sys.argv[1]
            status(name)
    except IndexError:
            get_docker_json()
