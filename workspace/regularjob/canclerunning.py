#!/usr/local/bin/python2.7
import os
import time
import json
import requests

BaseURL = 'http://localhost:6800'
def cancle(id):
    url = BaseURL + '/cancel.json'
    #print url
    data = {'project': 'seCrawler', 'job': id}
    res = requests.post(url, data=data)
    #print res.text

url = BaseURL + '/listjobs.json?project=seCrawler'
res = requests.get(url).text
data = json.loads(res)
for spider in  data['running']:
    start_time = time.mktime(time.strptime(spider['start_time'], '%Y-%m-%d %H:%M:%S.%f'))
    now = time.time()
    if 1:
        id = spider['id']
        os.system('ps aux |grep %s|grep -v grep |awk \'{print $2}\'|xargs kill -9' % id)
        print spider
        cancle(id)

