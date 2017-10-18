# !/usr/bin/env python
# -*- coding:utf-8 -*-

import scrapy, re, json, sys  
  
# 导入框架内置基本类class scrapy.spider.Spider  
try:  
    from scrapy.spiders import Spider  
except:  
    from scrapy.spiders import BaseSpider as Spider  
  
# 导入爬取一般网站常用类class scrapy.contrib.spiders.CrawlSpider和规则类Rule  
from scrapy.spiders import CrawlSpider, Rule  
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor 
from scrapy import Request
import base64
import json
import urllib2
import urllib
import time
import json
import requests
from bs4 import BeautifulSoup
import HTMLParser

from ..items import Newsspader01Item
from ..util.myLog import MyLog
from ..util.conn_mysql import conn_mysql
from ..util.config import PAGE

reload(sys)  
sys.setdefaultencoding('utf-8')  
ml = MyLog()
mysql_conn = conn_mysql()

class SinaSearchSpider(scrapy.Spider):
    name = "SinaSearchSpider"
    #allowed_domains = ["sinopecnews.com.cn",""]
    ml.info('---SinaSearchSpider--')
    start_urls = []
    mysqlop = mysql_conn.cursor()
    mysqlop.execute("SET NAMES utf8")
    mysqlop.execute("SET CHARACTER_SET_CLIENT=utf8")
    mysqlop.execute("SET CHARACTER_SET_RESULTS=utf8")
    mysql_conn.commit()

    # get latest time from mysql
    mysqlop.execute("select keyword, type from key_words")
    times = mysqlop.fetchmany(size=10000000)
    for time_item in times:
            key = urllib.quote(time_item[0])
            ml.info("http://api.search.sina.com.cn/?c=news&q="+key+"&sort=time&highlight=0&num=10&ie=utf-8")
            start_urls.append("http://api.search.sina.com.cn/?c=news&q="+key+"&sort=time&highlight=0&num=10&ie=utf-8")

    def parse(self, response):
        data = response.body
        print data
        s = json.loads(data)
        ps = s['result']['ps']
        q = s['result']['q']
        pf = s['result']['pf']
        count = s['result']['count']
        num = s['result']['num']
        for page in range(PAGE):
            ml.info('http://api.search.sina.com.cn/?c=news&q='+q+'&pf='+pf+'&ps='+ps+'&page='+str(page))
            res1 = requests.get('http://api.search.sina.com.cn/?c=news&q='+q+'&pf='+pf+'&ps='+ps+'&page='+str(page))
            jsonObj1 = res1.text
            s1 = json.loads(jsonObj1)
            for obj in s1['result']['list']:
                title = obj['title']
                url = obj['url']
                datetime = obj['datetime']
				media = obj['media']
                timeArray2 = time.strptime(datetime, "%Y-%m-%d %H:%M:%S")
                publishTime = int(time.mktime(timeArray2))
                yield Request(url, meta={'url':url,'title':title, 'publishTime':publishTime,'media':media}, callback=self.parse_body)


    def parse_body(self, response):
        url = response.meta['url']
        title = response.meta['title']
        publishTime = response.meta['publishTime']
		media = response.meta['media']
        data = response.body  
        soup = BeautifulSoup(data, "lxml")
        tagsli = soup.find('div',attrs={'class':'article article_16'})
        content=''
        ps = tagsli.find_all('p')[:-1]
        for p in ps:
            content+=p.get_text().strip()+'\n'
        item = Newsspader01Item()
        item['title'] = title
        item['url'] = url
        item['publishTime'] = publishTime
        item['content'] = content
        item['htmlbody'] = base64.b64encode(data)
        item['siteName'] = media
        return item
















