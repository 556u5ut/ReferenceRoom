#!/usr/bin/env python
#-*- coding: utf-8 -*-

from newsSpader01.middlewares.resource import PROXIES
import random
import base64

class RandomProxy(object):
    def process_request(self,request,spider):
        proxy = random.choice(PROXIES)
        userPasswd = proxy.split('@')[0]
        ipPort = proxy.split('@')[1]
        request.meta['proxy'] = 'http://%s' %ipPort
        proxy_user_pass = userPasswd
        encoded_user_pass = base64.encodestring(proxy_user_pass)
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass