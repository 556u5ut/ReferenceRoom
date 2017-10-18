#!/usr/local/bin/python2.7
#coding:utf-8
from  gearman import GearmanWorker
from var_dump import var_dump

import requests
import json

HOST_URL = 'http://localhost:6800'

def weibo(gearman_worker,job):
    var_dump(job.data)
    param = json.loads(job.data)
    keyword = param['keyword']
    pages = param['pages']
    se = param['se']
    res = requests.post(HOST_URL + '/schedule.json', data = {'project':'seCrawler', 'spider':'weiboSpider', 'se': se, 'pages': pages, 'keyword':keyword})
    var_dump(res.text)
    return str("Job added")


def bbs(gearman_worker,job):
    res = requests.post(HOST_URL + '/schedule.json', data = {'project':'yuqingspider', 'spider':'bbsSpider'})
    var_dump(res.text)
    
    return str("Job added")


def blog(gearman_worker,job):
    res = requests.post(HOST_URL + '/schedule.json', data = {'project':'yuqingspider', 'spider':'blogSpider'})
    var_dump(res.text)
    
    return str("Job added")

def news(gearman_worker,job):
    res = requests.post(HOST_URL + '/schedule.json', data = {'project':'yuqingspider', 'spider':'newsSpider'})
    var_dump(res.text)
    
    return str("Job added")

def media(gearman_worker,job):
    res = requests.post(HOST_URL + '/schedule.json', data = {'project':'yuqingspider', 'spider':'mediaSpider'})
    var_dump(res.text)
    
    return str("Job added")

def same_class(gearman_worker,job):
    res = requests.post(HOST_URL + '/schedule.json', data = {'project':'yuqingspider', 'spider':'newsSameClassSpider'})
    var_dump(res.text)
    
    return str("Job added")

def main():
    gw = GearmanWorker(['127.0.0.1:4730'])
    gw.register_task("weibo_spider", weibo)
    gw.register_task("bbs_spider", bbs)
    gw.register_task("news_spider", news)
    gw.register_task("blog_spider", blog)
    gw.register_task("media_spider", media)
    gw.register_task("class_spider", same_class)
    gw.work()

if __name__ == "__main__":
    main()

