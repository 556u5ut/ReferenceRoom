#!/usr/bin/env python
#-*- coding: utf-8 -*-

import random
import base64

PROXIES = [
  'cnpc:cnpc@123.249.16.231:8888',
  'cnpc:cnpc@123.249.16.232:8888',
  'cnpc:cnpc@123.249.16.233:8888',
  'cnpc:cnpc@123.249.16.234:8888',
  'cnpc:cnpc@123.249.16.235:8888',
  'cnpc:cnpc@123.249.16.236:8888',
  'cnpc:cnpc@123.249.16.237:8888',
  'cnpc:cnpc@123.249.16.238:8888',
  'cnpc:cnpc@123.249.16.239:8888',
  'cnpc:cnpc@123.249.16.240:8888'
]

class RandomProxy(object):
    def process_request(self,request,spider):
        proxy = random.choice(PROXIES)
        userPasswd = proxy.split('@')[0]
        ipPort = proxy.split('@')[1]
        request.meta['proxy'] = 'http://%s' %ipPort
        proxy_user_pass = userPasswd
        encoded_user_pass = base64.encodestring(proxy_user_pass)
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass