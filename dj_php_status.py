#!/usr/bin/env python
# coding:utf-8

import json
import sys
from urllib import urlopen
import traceback
from daojia_zabbix.common import generate_trapper_data, write_tmp_file, zabbix_sender

tmp_data_file = "/tmp/dj_php_status.tmp"
item_key_prefix = "dj.php.status"


def get_php_status():
    url = "http://localhost/php-fpm_status?json"
    r = urlopen(url).read()
    r = json.loads(r)
    return r


def generate_data(data):
    r = {
        "conn": data["accepted conn"],
        "listen_queue": data["listen queue"],
        "max_listen_queue": data["max listen queue"]
    }
    return r


if __name__ == "__main__":
    try:
        data = generate_data(get_php_status())
        content = generate_trapper_data(item_key_prefix, data)
        write_tmp_file(tmp_data_file, content)
        status, stdout = zabbix_sender(tmp_data_file)
        print status
        sys.exit(status)
    except Exception, e:
        print traceback.format_exc()
        sys.exit(1)
