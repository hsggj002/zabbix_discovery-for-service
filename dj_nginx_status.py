#!/usr/bin/env python
# coding:utf-8

import json
import sys
from urllib import urlopen
import traceback
from daojia_zabbix.common import generate_trapper_data, write_tmp_file, zabbix_sender

tmp_data_file = "/tmp/dj_nginx_status.tmp"
item_key_prefix = "dj.nginx.status"


def get_nginx_status():
    d = []
    url = "http://localhost/nstatus"
    r = urlopen(url).read()
    l = r.split('\n')
    for i in l:
        d.append(i.strip().split())
    
    return d


def get_dic(d):
    r = {}
    conn = ''.join(d[0][0])+''.join(d[0][1])
    
    r[d[1][1]]=d[2][0]
    r[d[1][2]]=d[2][1]
    r[d[1][3]]=d[2][2]
    r[d[1][4]]=d[2][3]
    r[conn]=d[0][2]
    r[d[3][0]]=d[3][1]
    r[d[3][2]]=d[3][3]
    r[d[3][4]]=d[3][5]
    return r

def generate_data(data):
    r = {
        'Active_connections': data['Activeconnections:'],
        'accepts': data['accepts'],
        'handled': data['handled'],
        'requests': data['requests'],
        'request_time': data['request_time'],
        'Reading': data['Reading:'],
        'Writing': data['Writing:'],
        'Waiting': data['Waiting:']
    }
    return r
    

if __name__ == "__main__":
    try:
        result = get_nginx_status()
        data = generate_data(get_dic(result))
        content = generate_trapper_data(item_key_prefix, data)
        write_tmp_file(tmp_data_file, content)
        status, stdout = zabbix_sender(tmp_data_file)
        sys.exit(status)
    except Exception, e:
        print traceback.format_exc()
        sys.exit(1)
