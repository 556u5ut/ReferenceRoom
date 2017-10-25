# -*- coding: utf-8 -*-
import scrapy
from fayuan.items import XingJueItem

class xingJueSpider(scrapy.Spider):
    name = 'xingJueSpider'
    start_urls = ['http://www.court.gov.cn/paper/default/index/keyword/%E5%88%91%E4%BA%8B%E5%86%B3%E5%AE%9A%E4%B9%A6/caseid//starttime//stoptime.html']

    def parse(self, response):
        wenshuUrls = response.xpath("//div[@class='l']/ul/li/a/@href").extract()
        for url in wenshuUrls:
            url = "http://www.court.gov.cn"+url
            yield scrapy.Request(url,callback=self.parse_wenshu)
        nextPageUrl = response.xpath("//li[@class='next']/a/@href").extract_first()
        if nextPageUrl is not None:
            nextPageUrl = "http://www.court.gov.cn"+nextPageUrl
            yield  scrapy.Request(nextPageUrl,callback=self.parse)

    def parse_wenshu(self,response):
        item = XingJueItem()
        item['title'] = response.xpath("//div[@class='title']/text()").extract_first()
        item['pubDate'] = response.xpath("//li[@class='fl print']/text()").extract_first()
        item['num'] = response.xpath(u"///div[@style='TEXT-ALIGN: right; LINE-HEIGHT: 25pt; MARGIN: 0.5pt 0cm;  FONT-FAMILY: 宋体;FONT-SIZE: 15pt; ']/text()").extract_first()
        textList = response.xpath(u"//div[@style='LINE-HEIGHT: 25pt; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 宋体; FONT-SIZE: 15pt;']/text()").extract()
        text = ''
        for line in textList:
            text = text + line
        item['text'] = text
        item['ending'] = response.xpath(u"//div[@style='TEXT-ALIGN: right; LINE-HEIGHT: 25pt; MARGIN: 0.5pt 36pt 0.5pt 0cm;FONT-FAMILY: 宋体; FONT-SIZE: 15pt; ']/text()").extract_first()

        if item['num'] is None:
            item['num'] = response.xpath(u"//div[@style='margin: 0.5pt 0cm; text-align: right; line-height: 25pt; font-family: 宋体; font-size: 15pt;' ]/text()").extract_first()
            textList = response.xpath(u"//div[@style='margin: 0.5pt 0cm; line-height: 25pt; text-indent: 30pt; font-family: 宋体; font-size: 15pt;']/text()").extract()
            text = ''
            for line in textList:
                text = text + line
            item['text'] = text
            item['ending'] = response.xpath(u"//div[@style='margin: 0.5pt 36pt 0.5pt 0cm; text-align: right; line-height: 25pt; font-family: 宋体; font-size: 15pt;']/text()").extract_first()

        if item['text']=="":
            item['num'] = response.xpath(u"//div[@style='font-size: 15pt; font-family: 宋体; text-align: right; margin: 0.5pt 0cm; line-height: 25pt']/text()").extract_first()
            textList = response.xpath(u"//div[@style='font-size: 15pt; font-family: 宋体; margin: 0.5pt 0cm; line-height: 25pt; text-indent: 30pt']/text()").extract()
            text=''
            for line in textList:
                text = text + line
            item['text'] = text
            item['ending'] = response.xpath(u"//div[@style='font-size: 15pt; font-family: 宋体; text-align: right; margin: 0.5pt 36pt 0.5pt 0cm; line-height: 25pt']/text()").extract_first()
        yield item