# -*- coding: utf-8 -*-
import scrapy
from pipetest.items import PipetestItem

class babyspiderSpider(scrapy.Spider):
    name = 'babySpider'
    start_urls = ['http://paper.people.com.cn/rmrb/html/2017-09/11/nbs.D110000renmrb_01.htm']

    def parse(self, response):
        item=PipetestItem()
        item['text']=response.xpath('//p/text()').extract()
        urls=response.xpath('//li/a/@href').extract()
        del urls[0]
        yield item
        if urls is not None:
            for url in urls:
                url="http://paper.people.com.cn/rmrb/html/2017-09/11/"+url
                yield scrapy.Request(url,callback=self.parse)