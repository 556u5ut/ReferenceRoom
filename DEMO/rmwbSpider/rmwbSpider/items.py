# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RmwbspiderItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    title= scrapy.Field()
    description = scrapy.Field()
    answer = scrapy.Field()
