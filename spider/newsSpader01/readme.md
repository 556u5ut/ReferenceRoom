
## ע�⣺
### ��1����ȡ
- ��util.config�����޸�PAGE=10
- ��pipeline����ȡ�� #threeHourAgoLong = '0000000000000' ��ע��

### ��2-n����ȡ
- ��util.config�����޸�PAGE=2
- ��pipeline����ע�� #threeHourAgoLong = '0000000000000' 

## ����
ʹ��scrapyd ����

�� newsSpader01 Ŀ¼ִ�����scrapyd-deploy scrapyNetworkInSearch 

Ȼ��ִ����ȡ����,��
```
curl http://localhost:6800/schedule.json -d project=newsSpader01 -d spider=ChinaShiHuaNewSpider
```

##�ű�
```
# coding=utf-8  
import urllib  
import urllib2  
  
spiderName1 = ['ChinaEnergySpider','ChinaShiHuaNewSpider','HeXunSpider','JingjiGuanchaSpider','SinaSearchSpider']
for spiderName2 in spiderName1:
	crawl(spiderName2)
  
# �������� 
def crawl(spiderName):
	test_data = {'project':'baidu', 'spider':spiderName}  
	test_data_urlencode = urllib.urlencode(test_data)  
	requrl = "http://localhost:6800/schedule.json"   
	req = urllib2.Request(url = requrl, data = test_data_urlencode)  
	res_data = urllib2.urlopen(req)  
	res = res_data.read()  # res ��str����  
	print res

# �鿴��־  
# ������get���� 
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