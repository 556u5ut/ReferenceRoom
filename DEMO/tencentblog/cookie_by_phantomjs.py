#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from selenium import webdriver
import json
import time
import re

user = '568793056'
password = 'lwn18710990068@'

driver = webdriver.PhantomJS()
driver.maximize_window()

login_url = 'http://t.qq.com/'
loop_url = 'http://www.qq.com/'
#获取登录主页时可能会请求到腾讯网的主页，请求时间不定
driver.get(login_url)
while loop_url == driver.current_url:
    print 'relogin_url: %s' % login_url
    driver.delete_cookies()
    driver.get(login_url)

driver.switch_to_frame('login_div')
driver.find_element_by_id('switcher_plogin').click()

driver.find_element_by_id('u').clear()
driver.find_element_by_id('u').send_keys(user)
driver.find_element_by_id('p').clear()
driver.find_element_by_id('p').send_keys(password)
driver.find_element_by_id('login_button').click()

search_key = u'石油'
#搜索可能出错，设置重试次数
loop_count = 5
while loop_count:
    loop_count -= 1
    try:
        #需要sleep一段时间
        time.sleep(1)
        driver.find_element_by_id('searchKey').clear()
        driver.find_element_by_id('searchKey').send_keys(search_key)
        break
    except:
        # 若跳转到了腾讯主页，则退出
        if driver.current_url == loop_url:
            sys.exit('jump_url: %s' % loop_url)

#重试完后退出
if loop_count == 0:
    sys.exit('restart...')

driver.find_element_by_class_name('inputBtn').click()

cookie = driver.get_cookies()
cookie = [item["name"] + "=" + item["value"] for item in cookie]  
cookiestr = ';'.join(item for item in cookie)  

filename = 'tencent_weibo_cookie.txt'
with open(filename, 'w') as fi:
    fi.write(cookiestr)

driver.quit()
print 'cookie done...'
