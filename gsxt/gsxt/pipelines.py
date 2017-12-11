# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import re

class GsxtPipeline(object):
    def __init__(self):
        self.file=codecs.open('text.json','w',encoding='utf-8')
    def process_item(self, item, spider):
        str = item['text']
        judAuth_CH = re.findall('''.*?judAuth_CN":"(.*?)","judDate.*?''',str)
        
        line=json.dumps(judAuth_CH,ensure_ascii=False)+"\n"
        self.file.write(line)
        return item
    def spider_closed(self, spider):
         self.file.close()