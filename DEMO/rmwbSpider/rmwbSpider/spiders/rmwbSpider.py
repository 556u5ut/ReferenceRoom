# -*- coding: utf-8 -*-

from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy.spiders import Spider
from ..items import RmwbspiderItem

# -*- coding: utf-8 -*-

class rmwbSpider(Spider):

    name = 'rmwbSpider'

    start_urls = ['http://t.people.com.cn/indexV3.action' ]
	#模拟浏览器
    custom_settings = {'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3026.3 Safari/537.36'}

    def start_requests(self):
        return [Request("http://t.people.com.cn/indexV3.action", meta = {'cookiejar' : 1}, callback = self.parse)]

    def parse(self, response):
	#从userList读取用户名密码
	with open('userList.txt','r') as f:
	    while True:
		line = f.readline().strip('\n')
		if not line:
		    break
		    pass
		usr,password = [str(item) for item in line.split("\t")]
		#构造formdata的表单
		formadata = {
            	'password': '',
	    	    'userName': '',
	    	    '__checkbox_isremember':'true'
        	}
		formadata['password'] = password
		formadata['userName'] = usr
		print (formadata)
		#利用FormRequest提交表单
        	yield FormRequest.from_response(
				  meta = {'cookiejar' : response.meta['cookiejar']},
                                  response=response, 
                                  formdata=formadata, 
                                  callback=self.after_login, 
                                  )

    def after_login(self, response):
	Cookie = response.request.headers.getlist('Cookie')
	#将获取的cookie保存并利用登陆cookie请求搜索页
	with open('/home/chen/rmwbSpider/rmwbSpider/util/cookieList.txt','a+') as fp:
	    fp.write(str(Cookie) +"\n")	
	yield Request('http://t.people.com.cn/searchV3.action?searchInput=%CA%AF%D3%CD',meta = {'cookiejar' : response.meta['cookiejar']}, callback =self.sub_parse,dont_filter = True)
    def sub_parse(self, response):
	with open('石油.html', "wb") as f:
            f.write(response.body)
