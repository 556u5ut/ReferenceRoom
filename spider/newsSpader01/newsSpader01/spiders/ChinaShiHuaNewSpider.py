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
from ..util.config import PAGE

reload(sys)  
sys.setdefaultencoding('utf-8')  
ml = MyLog()
mysql_conn = conn_mysql()

class ChinaShiHuaNewSpider(scrapy.Spider):
    name = "ChinaShiHuaNewSpider"
    allowed_domains = ["sinopecnews.com.cn"]
    ml.info('---ChinaShiHuaNewSpider----')
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
        if time_item[1] == '0':
            key = urllib.quote(time_item[0])
            for page in range(PAGE):
                start_urls.append('http://www.sinopecnews.com.cn:9999/search/servlet/SearchServlet.do?contentKey='+key+'&sort=date&pageNo='+str(page))
        elif time_item[1] == '1':
            key = urllib.quote(time_item[0])
            shiyou = urllib.quote('石油')
            for page in '1','2','3','4','5':
                start_urls.append('http://www.sinopecnews.com.cn:9999/search/servlet/SearchServlet.do?contentKey='+key+'+'+shiyou+'&sort=date&pageNo='+str(page))

    def parse(self, response):
        data = response.body  
        soup = BeautifulSoup(data, "lxml")
        times = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        yearMonth = times[:7]
        day = times[8:]
        tagstable = soup.find('table',attrs={'cellspacing':'2'})
        if tagstable != None:
            tagstrs = tagstable.find_all('tr')
            for tagstr in tagstrs:
                if(tagstr.find('img')):
                    continue
                tagsp = tagstr.find_all('p')
                if len(tagsp)<1:
                    continue
                url = tagsp[1].find('a').get('href')
                if 'news' not in url[25:]:
                    continue
                if yearMonth not in url or day not in url:
                    continue
                tagsSpans = tagsp[1].find_all('span')
                yield Request(url, meta={'url':url}, callback=self.parse_body)

    def parse_body(self, response):
        url = response.meta['url']
        data = response.body  
        soup = BeautifulSoup(data, "lxml")
        tagsdiv = soup.find('div',attrs={'id':'content'})
        tagsTables = tagsdiv.find_all('table')
        # 0 标题 ；1 时间 来源 ； 6 正文 ；
        title = tagsTables[0].find('b').get_text()
        timeSource = tagsTables[1].find('td').get_text().strip()
        datetime1 =  timeSource[:10]+' 00:00:00'
        content = ''
        tagsps = tagsTables[5].find_all('p')
        for tagsp in tagsps:
            content += tagsp.get_text().strip()
        ml.info(url)
        ml.info(title)
        ml.info(datetime1)
        ml.info(content)
        timeArray = time.strptime(datetime1, "%Y-%m-%d %H:%M:%S")
        publishTime = int(time.mktime(timeArray))
        item = Newsspader01Item()
        item['title'] = title
        item['url'] = url
        item['publishTime'] = publishTime
        item['content'] = content
        item['htmlbody'] = base64.b64encode(data)
        item['siteName'] = '中国石化新闻网'
        return item





    
    


