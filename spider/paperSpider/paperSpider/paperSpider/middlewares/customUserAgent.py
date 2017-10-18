#!/usr/bin/env python
#-*- coding: utf-8 -*-

from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from paperSpider.middlewares.resource import UserAgents
import random

class RandomUserAgent(UserAgentMiddleware):
    def process_request(self,request,spider):
        ua = random.choice(UserAgents)
        request.headers.setdefault('User-Agent', ua)