# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class rmwbspiderPipeline(object):
    def process_item(self, item, spider):
        file = open("items.txt", "a")  # 以追加的方式打开文件，不存在则创建
        # 因为item中的数据是unicode编码的，为了在控制台中查看数据的有效性和保存，
        # 将其编码改为utf-8
        item_string = str(item).decode("unicode_escape").encode('utf-8')
	
        file.write(item_string)
        file.write('\n')
        file.close()
        print item_string  #在控制台输出
