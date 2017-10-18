# -*- coding: utf-8 -*-
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
import time
from bs4 import BeautifulSoup

from ..items import Newsspader01Item
from ..util.myLog import MyLog
from ..util.config import PAGE

# 设置编码格式  
reload(sys)  
sys.setdefaultencoding('utf-8')  
ml = MyLog()
class ChinaEnergySpider(scrapy.Spider):
    name = "ChinaEnergySpider"
    allowed_domains = ["cnenergy.org"]
    ml.info('---ChinaEnergySpider----')
    start_urls = []
    start_urls.append('http://www.cnenergy.org/yq/sy/')
    for page in range(PAGE):
        start_urls.append('http://www.cnenergy.org/yq/shijian_3'+str(page)+'.html')

    def parse(self, response):
        ml.info("ChinaEnergySpider--parse---")
        data = response.body  
        soup = BeautifulSoup(data, "lxml")
        #tagsdiv = soup.find('div',attrs={'class':'main4_left_m'})
        tagsdivs = soup.find_all('div',attrs={'class':'main4_left_m1'}) 
        for tags in tagsdivs: 
            if(tags.find('img')):
                continue
            title = tags.find('div',attrs={'class':'main4_left_m1_t'}).find_all('a')[1].get_text()
            ml.info(title)
            urlhref = tags.find('div',attrs={'class':'main4_left_m1_t'}).find_all('a')[1].get('href')
            url = 'http://www.cnenergy.org/yq/sy/'+urlhref[2:]
            ml.info(url)
            publishTime = tags.find('div',attrs={'class':'m2'}).find('span',attrs={'class':'b2'}).get_text()   
            ml.info(publishTime)
            yield Request(url, meta={'title': title,'publishTime':publishTime,'url':url}, callback=self.parse_body)

    def parse_body(self, response):
        ml.info("ChinaEnergySpider--parse_body---")
        title = response.meta['title']
        datetime1 = response.meta['publishTime']
        timeArray1 = time.strptime(datetime1, "%Y-%m-%d %H:%M")
        publishTime = int(time.mktime(timeArray1))
        url = response.meta['url']
        data = response.body  
        soup = BeautifulSoup(data, "lxml")
        tagsdiv = soup.find('div',attrs={'class':'xlcontent'}).find_all('p')
        content = ''
        for tagsp in tagsdiv:
            content+=tagsp.get_text().strip()
        item = Newsspader01Item()
        item['title'] = title
        item['url'] = url
        item['publishTime'] = publishTime
        item['content'] = content
        item['htmlbody'] = base64.b64encode(data)
        item['siteName'] = '中国能源网'
        return item




















