
## 注意：
### 第1次爬取
- 在util.config里面修改PAGE=10
- 在pipeline里面取消 #threeHourAgoLong = '0000000000000' 的注释

### 第2-n次爬取
- 在util.config里面修改PAGE=2
- 在pipeline里面注释 #threeHourAgoLong = '0000000000000' 

## 部署
使用scrapyd 部署

在 newsSpader01 目录执行命令：scrapyd-deploy scrapyNetworkInSearch 

然后执行爬取过程,如
```
curl http://localhost:6800/schedule.json -d project=newsSpader01 -d spider=ChinaShiHuaNewSpider
```

##脚本
```
# coding=utf-8  
import urllib  
import urllib2  
  
spiderName1 = ['ChinaEnergySpider','ChinaShiHuaNewSpider','HeXunSpider','JingjiGuanchaSpider','SinaSearchSpider']
for spiderName2 in spiderName1:
	crawl(spiderName2)
  
# 启动爬虫 
def crawl(spiderName):
	test_data = {'project':'baidu', 'spider':spiderName}  
	test_data_urlencode = urllib.urlencode(test_data)  
	requrl = "http://localhost:6800/schedule.json"   
	req = urllib2.Request(url = requrl, data = test_data_urlencode)  
	res_data = urllib2.urlopen(req)  
	res = res_data.read()  # res 是str类型  
	print res

# 查看日志  
# 以下是get请求 
"""
myproject = "baidu"  
requrl = "http://localhost:6800/listjobs.json?project=" + myproject   
req = urllib2.Request(requrl)  
  
res_data = urllib2.urlopen(req)  
res = res_data.read()  
print res
"""
```

> 10 */5 * * * /usr/bin/python /root/scrapyNetworkInSearch.py