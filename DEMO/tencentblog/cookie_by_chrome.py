#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from selenium import webdriver
import json
import time

#帐号与密码
user = ''
password = ''

#有时候会定向到腾讯主页，再运行一次即可

#下载chrome driver
driver = webdriver.Chrome()

#设置浏览器窗口的位置和大小
driver.set_window_position(0, 0)
#最大化后可以点击‘使用帐号密码登录’选项
driver.maximize_window()

#打开一个页面（QQ空间登录页）
#driver.get('http://t.qq.com/')
driver.get('https://xui.ptlogin2.qq.com/cgi-bin/xlogin?appid=46000101&style=23&lang=&low_login=1&hide_border=1&hide_title_bar=1&hide_close_icon=1&border_radius=1&self_regurl=http%3A//reg.t.qq.com/index.php&proxy_url=http://t.qq.com/proxy_t.html&s_url=http%3A%2F%2Ft.qq.com&daid=6')
#登录表单在页面的框架中，所以要切换到该框架

#driver.switch_to.frame('login_div')
#通过使用选择器选择到表单元素进行模拟输入和点击按钮提交
driver.find_element_by_id('switcher_plogin').click()
#帐户
driver.find_element_by_id('u').clear()
driver.find_element_by_id('u').send_keys(user)
#密码
driver.find_element_by_id('p').clear()
driver.find_element_by_id('p').send_keys(password)
driver.find_element_by_id('login_button').click()

#登录之后的页面需要加载一部分页面内容才能继续操作，否则会报错
#若出错，可加长该部分的时间
time.sleep(0.5)

#搜索关键字
search_key = u'石油'
driver.find_element_by_id('searchKey').clear()
driver.find_element_by_id('searchKey').send_keys(search_key)
x=driver.find_element_by_xpath("//div[@class='hd']/a[@href='#'and@class='close_pop']")
if x:
    x.click()
driver.find_element_by_class_name('inputBtn').click()

#存搜索界面的cookie，只有搜索界面的cookie能用
cookie = driver.get_cookies()
#提取cookie字符串
cookie = [item["name"] + "=" + item["value"] for item in cookie]  
cookiestr = ';'.join(item for item in cookie)

#存微博cookie文件名
filename = 'tencent_weibo_cookie.txt'
with open(filename, 'w') as fi:
    fi.write(cookiestr)

#退出窗口
driver.quit()
