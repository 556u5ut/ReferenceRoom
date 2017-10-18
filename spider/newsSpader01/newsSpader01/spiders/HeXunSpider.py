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
from bs4 import BeautifulSoup

from ..items import Newsspader01Item
from ..util.myLog import MyLog
from ..util.conn_mysql import conn_mysql

reload(sys)  
sys.setdefaultencoding('utf-8')  
ml = MyLog()
mysql_conn = conn_mysql()

class HeXunSpider(scrapy.Spider):
    name = "HeXunSpider"
    allowed_domains = ["hexun.com"]
    ml.info('---HeXunSpider----')
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
        key = urllib.quote(time_item[0].encode('gbk'))
        start_urls.append('http://news.search.hexun.com/news?key='+key+'&t=day&s=1')

    def parse(self, response):
        data = response.body  
        soup = BeautifulSoup(data, "lxml")
        tagsdiv = soup.find('div',attrs={'class':'searchResult'})
        tagsdivs = tagsdiv.find_all('div',attrs={'class':'newslist-a mt30 clearfix'})
        for tags in tagsdivs:
            div1 = tags.find('div',attrs={'class':'news-l-t'})
            title = div1.find('a').get_text()
            url = div1.find('a').get('href')
            datetime = div1.find('span').get_text()
            timeArray2 = time.strptime(datetime, "%Y-%m-%d %H:%M:%S")
            publishTime = int(time.mktime(timeArray2))
            yield Request(url, meta={'url':url,'title':title, 'publishTime':publishTime}, callback=self.parse_body)

    def parse_body(self, response):
        url = response.meta['url']
        title = response.meta['title']
        publishTime = response.meta['publishTime']
        data = response.body  
        soup = BeautifulSoup(data, "lxml")
        tagsdiv = soup.find('div',attrs={'class':'art_contextBox'})
        tagsps = tagsdiv.find_all('p')
        content = ''
        for tagsp in tagsps:
            content += tagsp.get_text().strip()
        item = Newsspader01Item()
        item['title'] = title
        item['url'] = url
        item['publishTime'] = publishTime
        item['content'] = content
        item['htmlbody'] = base64.b64encode(data)
        item['siteName'] = '和迅网新闻'
        return item
























