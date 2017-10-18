# !/usr/bin/env python
# -*- coding:utf-8 -*-
import scrapy, re, json, sys,random,os
reload(sys)
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.setdefaultencoding('utf-8')
  
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
import urllib2
import time
from scrapy.selector import Selector

from ..items import PaperspiderItem
from ..util.conn_mysql import conn_mysql

mysql_conn = conn_mysql()

class paperSpider(Spider):
    name = 'paperSpider'
    start_urls = []
    def __init__(self, pages=1, *args, **kwargs):
        super(paperSpider, self).__init__(*args, **kwargs)
        self.item = dict()
        mysqlop = mysql_conn.cursor()
        mysqlop.execute("SET NAMES utf8")
        mysqlop.execute("SET CHARACTER_SET_CLIENT=utf8")
        mysqlop.execute("SET CHARACTER_SET_RESULTS=utf8")
        mysql_conn.commit()
        mysqlop.execute("SELECT source_name,url,template,type,id FROM t_source_used where type='paper' and template !='' ")
        keywords = mysqlop.fetchmany(size=10000000)
        today = time.strftime("%Y-%m-%d", time.localtime( time.time() ) )
        today = today.split("-")
        thisYear = today[0]
        thisMonth = today[1]
        thisDay = today[2]
        for item in keywords:
            source_name=item[0]
            url=item[1]
			self.sourceId = item[4]
            self.selector = json.loads(item[2])
            url = url.format(thisYear,thisMonth,thisDay)
            print(url)
            rooturl = url[0:url.rfind("/")+1]
            self.start_urls.append(
                        {'url': url, 'selector': self.selector, 'source_name': source_name, 'rooturl':rooturl, 'type': item[3]})
        random.shuffle(self.start_urls)	

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url['url'], meta={'source_name': url['source_name'],'rooturl':url['rooturl'], 'selector': url['selector']})

    def parse(self, response):
        if response.status in [200]:
            self.selector = response.meta['selector']
            source_name = response.meta['source_name']
            rooturl = response.meta['rooturl']
            response = response.replace(body=response.body.replace('<em>', '').replace('</em>', ''))
            banmianURLs = Selector(response).xpath(self.selector['urlBanmian']).extract()
            for banmianurl in banmianURLs:
                url2 = rooturl+str(banmianurl)
                print url2
                yield Request(url2, meta={'source_name': source_name,'rooturl':rooturl, 'selector': self.selector},callback=self.parse_news)

    def parse_news(self, response):
        self.selector = response.meta['selector']
        source_name = response.meta['source_name']
        rooturl = response.meta['rooturl']
        response = response.replace(body=response.body.replace('<em>', '').replace('</em>', ''))
        wenzhangURLs = Selector(response).xpath(self.selector['urlWenzhang']).extract()
        for wenzhangURL in wenzhangURLs:
            url3 = rooturl+str(wenzhangURL)
            print url3
            yield Request(url3, meta={'source_name': source_name, 'selector': self.selector, 'url':url3},callback=self.parse_body)

    def parse_body(self, response):
        self.selector = response.meta['selector']
        source_name = response.meta['source_name']
        url = response.meta['url']
        response = response.replace(body=response.body.replace('<em>', '').replace('</em>', ''))
        title = Selector(response).xpath(self.selector['title']).extract()
        content = Selector(response).xpath(self.selector['content']).extract()
        title = ''.join(title)
        content = ''.join(content).strip()
        data = response.body
        item = PaperspiderItem()
        item['title'] = title
        item['url'] = url
        item['publishTime'] = ''
        item['content'] = content
        item['htmlbody'] = base64.b64encode(data)
        item['siteName'] = source_name
		item['sourceId'] = self.sourceId
        return item
