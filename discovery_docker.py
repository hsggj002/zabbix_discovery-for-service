#!/usr/bin/python                                                                                                                                                                                                        [5/1828]
import sys
import os
import re
import json

def discover():
    d = {}
    d['data'] = []
    with os.popen("docker ps --format {{.Names}}") as pipe:
        for line in pipe:
            info = {}
            info['{#CONTAINERNAME}'] = line.replace("\n","")
            d['data'].append(info)

    print json.dumps(d)


def status(name,action):
    if action == "ping":
        cmd = 'docker inspect --format="{{.State.Running}}" %s' %name
        result = os.popen(cmd).read().replace("\n","")
        if result == "true":
            print 1
        else:
            print 0
    elif action == "MemUsage":
        cmd = 'docker stats %s --no-stream --format "{{.%s}}"' % (name,action)
        result = os.popen(cmd).read().replace("\n","")
        if "/" in result:
            result = result.split("/")
            #print float(re.findall(r'([0-9]+.[0-9]+)([A-Z,a-z]+)',result[0])[0][0])
            values = re.findall(r'([0-9]+.[0-9]+)([A-Z,a-z]+)',result[0])
            if "GiB" in values[0]:
                print float(values[0][0])*1000
            else:
                print float(values[0][0])
        else:
            print result
    else:
        cmd = 'docker stats %s --no-stream --format "{{.%s}}"' % (name,action)
        result = os.popen(cmd).read().replace("\n","")
        if "%" in result:
            print float(result.replace("%",""))
        else:
            print result
            
if __name__ == '__main__':
        try:
                name, action = sys.argv[1], sys.argv[2]
                status(name,action)
        except IndexError:
                discover()            
