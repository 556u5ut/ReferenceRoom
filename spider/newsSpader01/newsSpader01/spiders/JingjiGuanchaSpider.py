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
import HTMLParser

from ..items import Newsspader01Item
from ..util.myLog import MyLog
from ..util.conn_mysql import conn_mysql
from ..util.config import PAGE

reload(sys)  
sys.setdefaultencoding('utf-8')  
ml = MyLog()
mysql_conn = conn_mysql()
htmlparser = HTMLParser.HTMLParser()

class JingjiGuanchaSpider(scrapy.Spider):
    name = "JingjiGuanchaSpider"
    #allowed_domains = ["sinopecnews.com.cn",""]
    #rooturl = 'http://app.eeo.com.cn/?app=search&controller=index&action=searchall&p=0&w=%E7%BB%8F%E6%B5%8E%E7%A0%94%E7%A9%B6'
    ml.info('---JingjiGuanchaSpider----')
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
            for page in range(PAGE):
                start_urls.append('http://app.eeo.com.cn/?app=search&controller=index&action=searchall&p='+str(page)+'&w='+key)

    def parse(self, response):
        data = response.body  
        soup = BeautifulSoup(data, "lxml")
        tagsul = soup.find('ul',attrs={'class':'new_list'})
        tagslis = tagsul.find_all('li',attrs={'class':' li_blue font16 mtcs'})
        for tagsli in tagslis:
            title = tagsli.find('a').get_text()
            url = tagsli.find('a').get('href')
            datetime = tagsli.find('span').get_text()
            datetime = htmlparser.unescape(datetime)
            timeArray2 = time.strptime(datetime, u"%Y年%m月%d日 %H:%M")
            publishTime = int(time.mktime(timeArray2))
            yield Request(url, meta={'url':url,'title':title, 'publishTime':publishTime}, callback=self.parse_body)

    def parse_body(self, response):
        url = response.meta['url']
        title = response.meta['title']
        publishTime = response.meta['publishTime']
        data = response.body  
        soup = BeautifulSoup(data, "lxml")
        tagsdiv = soup.find('div',attrs={'class':'xx_boxsing'})
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
        item['siteName'] = '经济观察网'
        return item









