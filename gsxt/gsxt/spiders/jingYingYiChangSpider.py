# -*- coding: utf-8 -*-
import scrapy
from gsxt.items import GsxtItem

class jingYingYiChangSpider(scrapy.Spider):
    name = 'jingYingYiChangSpider'
    start_urls = ['http://www.gsxt.gov.cn/corp-query-entprise-info-getTenAfficheBusExcepInInfo-130000.html?length=20&start=0']

    def parse(self, response):
        item = GsxtItem()
        item['text'] = response.xpath("//text()").extract_first()
        yield item