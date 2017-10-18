# !/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import time
import json
from elasticsearch import Elasticsearch
from config import FILTER_URL
from config import JUDGE_URL
from config import KEYSUMMARY_URL
from config import AREA_URL
from config import ESURL

es = Elasticsearch(ESURL)

def wtiterES(indexName,doc,id1):
    try:
        res = es.index(index=indexName,doc_type="doc",id=id1,body=doc)
        print "insert elasticsearch success"
    except Exception,e:
        print 'error in insert into elasticsearch', e

def writeText(title,content,sentiment):
    now = time.strftime('%Y-%m-%d-%H', time.localtime())
    fileName = 'news-' + now + '.txt'
    with open(fileName,'a') as fp:
            fp.write(title +'-----'+ content+ '-----' +sentiment + '\n\n')

def filterPost(title,content,url):
    postUrl = FILTER_URL
    params = {"title":title,"content": content,"url":url}
    headers = { 'Content-Type':'application/json'}
    request = urllib2.Request( postUrl, json.dumps(params), headers)
    response = urllib2.urlopen(request)
    return json.loads(response.read())['result']

def judgePost(title,content,url):
    postUrl = JUDGE_URL
    params = {"title":title,"content": content,"url":url}
    headers = { 'Content-Type':'application/json'}
    request = urllib2.Request( postUrl, json.dumps(params), headers)
    response = urllib2.urlopen(request)
    return json.loads(response.read())['sentimentType']

def keySummaryPost(title,content,url):
    postUrl = KEYSUMMARY_URL
    params = {"title":title,"content": content,"url":url}
    headers = { 'Content-Type':'application/json'}
    request = urllib2.Request( postUrl, json.dumps(params), headers)
    response = urllib2.urlopen(request)
    result = json.loads(response.read())
    return result['keyWords'],result['summary']

def areaPost(title,content,url):
    postUrl = AREA_URL
    params = {"title":title,"content": content,"url":url}
    headers = { 'Content-Type':'application/json'}
    request = urllib2.Request( postUrl, json.dumps(params), headers)
    response = urllib2.urlopen(request)
    result = json.loads(response.read())
    return result['organization'],result['area'],result['province']








