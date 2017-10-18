# -*- coding: utf-8 -*-
import datetime
import time
import hashlib
import urllib2
import json
from util.postAPI import filterPost
from util.postAPI import judgePost
from util.postAPI import keySummaryPost
from util.postAPI import areaPost
from util.postAPI import wtiterES
from util.postAPI import writeText

import sys  
reload(sys)  
sys.setdefaultencoding( "utf-8" )  

class Newsspader01Pipeline(object):
    def process_item(self, item, spider):
        crawltime = str(int(time.mktime(datetime.datetime.now().timetuple())))
        id = hashlib.md5(item['url']).hexdigest()[:20]
        content = "".join(item['content'].decode('utf-8').split())
        crawlTime = ''.join([str(crawltime),"000"])
        publishTime = ''.join([str(item['publishTime']),"000"])
        # 周期性执行爬虫，5小时间隔，只爬取最近5小时内的新闻
        threeHourAgoTime = (datetime.datetime.now() - datetime.timedelta(hours = 5))
        timeStamp = int(time.mktime(threeHourAgoTime.timetuple()))
        threeHourAgoLong = ''.join([str(timeStamp),'000'])
        #threeHourAgoLong = '0000000000000'
        if publishTime > threeHourAgoLong:
            filterResult = filterPost(item['title'],content,item['url'])
            if filterResult == 1:
                judgeSentimentType = judgePost(item['title'],content,item['url'])
                keywords,summary = keySummaryPost(item['title'],content,item['url'])
                departId,area,province = areaPost(item['title'],content,item['url'])
                doc = {
                    "id": id,
                    "title": item['title'],
                    "url": item['url'],
                    "viewCount": 0,
                    "replyCount":0,
                    "keepCount":0,
                    "transCount": 0,
                    "praiseCount":0,
                    "content":  content,
                    "cateName": 'news',
                    "publishTime": publishTime,
                    "crawlTime": crawlTime,
                    "sourceName": item['siteName'],
                    "sentiment": judgeSentimentType,
                    "summary": summary,
                    "keywords":keywords,
                    "areaIds":area,
                    "provinceIds":province,
                    "author":'',
                    "departIds":departId
                }
                doc1 = {
                    "id": id,
                    "html":item['htmlbody']
                }
                wtiterES("public_sentiment",doc,id)
                wtiterES("snapshot",doc1,id)
                writeText(publishTime,crawlTime,'aaaaaaaaaa')
        return item


