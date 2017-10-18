# 报纸爬虫

## 目前已经支持的报纸
- 人民日报、		http://paper.people.com.cn/rmrb/html/2017-05/31/node_1921.htm
- 中国能源报、		http://paper.people.com.cn/zgnyb/html/2017-05/22/node_2221.htm
- 经济日报、		http://paper.ce.cn/jjrb/html/2017-06/02/node_2.htm
- 工人日报、		http://media.workercn.cn/sites/media/grrb/2017_05/31/GR0100.htm
- 光明日报、		http://epaper.gmw.cn/gmrb/html/2017-05/31/nbs.D110000gmrb_01.htm
- 经济参考报、		http://dz.jjckb.cn/www/pages/webpage2009/html/2017-05/31/node_2.htm 
- 中国青年报、		http://zqb.cyol.com/html/2017-05/31/nbs.D110000zgqnb_01.htm
- 科技日报、		http://digitalpaper.stdaily.com/http_www.kjrb.com/kjwzb/html/2017-06/01/node_121.htm
- 中国石化新闻报	http://202.149.227.159/zgshb/html/2017-06/02/node_2.htm


## 配置的模版
1. 人民日报、	
```
{
"urlBanmian":"//*[@id=\"pageLink\"]/@href",
"urlWenzhang":"//*[@id=\"titleList\"]/ul/li[*]/a/@href",
"title": "//div[@class=\"text_c\"]/h1/text()",
"content":"//div[@id=\"ozoom\"]/p/text()"
}
```

2. 中国能源报、	
```
{
"urlBanmian":"//*[@id=\"pageLink\"]/@href",
"urlWenzhang":"//area[@shape=\"polygon\"]/@href",
"title": "//div[@class=\"text_c\"]/h1/text()",
"content":"//div[@id=\"articleContent\"]/p/text()"
}
```
3. 经济日报、	
```
{
"urlBanmian":"//div[@id=\"bmdh\"]/table/tbody/tr[*]/td[2]/a/@href",
"urlWenzhang":"//div[@style=\"display:inline\"]/parent::a/@href",
"title": "//td[@class=\"font01\"]/text()",
"content":"//div[@id=\"ozoom\"]/founder-content/p/text()"
}
```
4. 工人日报、
```
{
"urlBanmian":"//div[@id=\"page_content\"]/table/tr/td[*]/a/@href",
"urlWenzhang":"//area[@shape=\"poly\"]/@href",
"title": "//div[@class=\"text_c\"]/h1/text()",
"content":"//div[@id=\"ozoom\"]/div/span/p/text()"
}
```
	
5. 光明日报、
```
{
"urlBanmian":"//a[@id=\"pageLink\"]/@href",
"urlWenzhang":"//div[@id=\"titleList\"]/ul/li[*]/a/@href",
"title": "//div[@class=\"text_c\"]/h1/text()",
"content":"//div[@id=\"articleContent\"]/p/text()"
}
```
	
6. 经济参考报、
```
{
"urlBanmian":"//div[@id=\"bmdh\"]/table/tbody/tr[*]/td[2]/a/@href",
"urlWenzhang":"//ul[@class=\"ul02_l\"]/li[*]/a/@href",
"title": "//td[@class=\"hei16b\"]/text()",
"content":"//td[@class=\"black14\"]/founder-content/p/text()"
}
```
7. 中国青年报、
```
{
"urlBanmian":"//a[@id=\"pageLink\"]/@href",
"urlWenzhang":"//div[@id=\"titleList\"]/ul/li[*]/a/@href",
"title": "//div[@class=\"text_c\"]/h1/text()",
"content":"//div[@id=\"ozoom\"]/p/text()"
}
```
8. 科技日报、
```
{
"urlBanmian":"//a[@id=\"pageLink\"]/@href",
"urlWenzhang":"//div[@class=\"title\"]/ul/li[*]/a/@href",
"title": "//div[@class=\"biaoti\"]/text()",
"content":"//div[@id=\"ozoom\"]/p/text()"
}
```	

9. 中国石化新闻报
```
{
"urlBanmian":"//ol[@id='breakNewsList1']/li[*]/a/@href",
"urlWenzhang":"//ol[@id='breakNewsList']/li[*]/a/@href",
"title": "//div[@class='newstitle']/h2/text()",
"content":"//div[@class='newscontent']/p/text()"}
```


