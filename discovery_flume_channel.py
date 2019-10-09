#!/usr/bin/env python
#

import requests
import json
import os
import re
import sys

p = re.compile(r'port=(\d+)')

def get_flume_path():
    flume_file = {}

    if os.path.exists('/opt/zyz/flume'):
        flumes = os.listdir('/opt/zyz/flume')
        for row in flumes:
            if os.path.exists('/opt/zyz/flume/'+row+'/start.sh'):
                flume_file[row]='/opt/zyz/flume/'+row+'/start.sh'

    if os.path.exists('/opt/flume'):
        flumes_migu = os.listdir('/opt/flume')
        for row in flumes_migu:
            if os.path.exists('/opt/flume/'+row+'/start.sh'):
                flume_file[row]='/opt/flume/'+row+'/start.sh'

    return flume_file

def get_flume_port():
    ports = {}

    for i in get_flume_path().items():
        with open(i[1]) as f:
            for line in f:
                r = p.search(line)
                if r:
                    t = r.group(1)
                    ports[i[0]] = t
    return ports
    
def GetData():
    json_data = {}

    for port in get_flume_port().items():
        data = requests.get("http://127.0.0.1:{0}/metrics".format(port[1]))
        json_data[port[0]]=json.loads(data.content.decode())

    return json_data

def getSize():
    channel = {}

    for i in GetData().items():
        for y in i[1].items():
            if "CHANNEL" in y[0]:
                channel[i[0]] = {}
                channel[i[0]][y[0]] = {}

            for k in y[1].items():
                if k[0] == "ChannelSize" or k[0] == "ChannelFillPercentage":
                    channel[i[0]][y[0]][k[0]] = k[1]

    return channel

def get_json():
    r = {'data': []}

    for f_name in getSize().items():
        for channel_name in f_name[1].items():
            r['data'].append({"{#SERVER_NAME}":f_name[0], "{#FLUME_NAME}":channel_name[0], "{#FLUME_DATA}": channel_name[1]})

    print(json.dumps(r))

def as_num(x):
    y = '{0:.10f}'.format(x)

    return y
    
def get_data_num(s_name, c_name, nums):

    for f_name in getSize().items():
        for f_data in f_name[1].items():
            if s_name == f_name[0] and c_name in f_data:
                if nums == "ChannelFillPercentage":
                    if ('E' in nums or 'e' in nums):
                        print as_num(float(f_data[1][nums]))
                else:
                    print f_data[1][nums]

if __name__ == '__main__':
    try:
            s_name, c_name, nums = sys.argv[1], sys.argv[2], sys.argv[3]
            get_data_num(s_name, c_name, nums)
    except IndexError:
            get_json()
 
