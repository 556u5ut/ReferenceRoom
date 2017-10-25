# -*- coding: utf-8 -*-
import scrapy
from fayuan.items import XingJueItem

class xingCaiSpider(scrapy.Spider):
    name = 'xingCaiSpider'
    start_urls = ['http://www.court.gov.cn/paper/default/index/keyword/%E8%A1%8C%E6%94%BF%E8%A3%81%E5%AE%9A%E4%B9%A6/caseid//starttime//stoptime.html']
    for page in range(55,60):
        start_urls.append("http://www.court.gov.cn/paper/default/index/keyword/%E8%A1%8C%E6%94%BF%E8%A3%81%E5%AE%9A%E4%B9%A6/caseid//starttime//stoptime//page/"+str(page)+".html")

    def parse(self, response):
        wenshuUrls = response.xpath("//div[@class='l']/ul/li/a/@href").extract()
        for url in wenshuUrls:
            url = "http://www.court.gov.cn"+url
            yield scrapy.Request(url,callback=self.parse_wenshu)

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