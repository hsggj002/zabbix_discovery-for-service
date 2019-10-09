#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
import sys
import os
import json
import logging

logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s, %(filename)s, %(levelname)s, %(message)s',
                datefmt = '%a, %d %b %Y %H:%M:%S',
                filename = os.path.join('/etc/zabbix/alertscripts','weixin.log'),
                filemode = 'a')

corpid='wx059471abeb063951'
appsecret='01dAgRdjc_08wMsqazgZo1wl-2OLKhruEvj_eGPFJd8'
agentid=1000011
#获取accesstoken
token_url='https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + appsecret
req=requests.get(token_url)
accesstoken=req.json()['access_token']

#发送消息
msgsend_url='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + accesstoken



def choose_tag(severity):
    tag = '1'
    if serverity >= 4:
        tag = '2|3'
    elif serverity >= 3:
        tag = '2'

    return tag


touser=sys.argv[1]
subject=sys.argv[2]
#toparty='1875'
#toparty='3|4|5|6'
message=sys.argv[3]
Tagid = "1"


#def get_alter_severity(message):
#    msg_list = []
#    msg_dic = {}
#    for line in message:
#        msg_list.append(line.split(":"))

#    for dic in msg_list:
#        msg_dic[dic[0]] = dic[-1]

#alert_send(sys.argv[1], sys.argv[2])
params={
        "touser": touser,
      #  "toparty": toparty,
        "totag": Tagid,
        "msgtype": "text",
        "agentid": agentid,
        "text": {
                "content": message
        },
        "safe":0
}


req=requests.post(msgsend_url, data=json.dumps(params))

#logging.info('sendto:' + touser + ';;subject:' + subject + ';;message:' + message)
logging.info('sendto:' + touser + ';;subject:' + subject + ';;message:' + message)
