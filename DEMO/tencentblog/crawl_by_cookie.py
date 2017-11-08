#coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2
import cookielib
import lxml.html
from lxml import etree
import time
import json

#从文件读取cookie，仅搜索页cookie可用
def read_cookie():
    #微博cookie存放文件名
    filename = 'tencent_weibo_cookie.txt'
    try:
        with open(filename, 'r') as fi:
            cookie = fi.read()
            return cookie
    except:
        return None

def crawl():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    headers['Cookie'] = read_cookie()
    #起始页, 总共爬多少页
    start, pages = 1, 5
    opener = urllib2.build_opener()
    #微博计数
    textCount = 0
    for page in range(start, start+pages):
        #每隔多少秒爬一页
        time.sleep(2)
        #搜索页面
        url = 'http://search.t.qq.com/index.php?k=%E7%9F%B3%E6%B2%B9&pos=211&p=' + str(page)
        request = urllib2.Request(url, None, headers)
        response = opener.open(request)
        #读取网页内容，用CSS提取
        textCount = response_css(textCount, response)
    return opener

#用CSS提取utf-8编码网页内容
def response_css(textCount, response):
    #若网页内容不是utf-8编码，舍弃
    try:
        s = response.read()
        tree = lxml.html.fromstring(s.decode('utf-8'))
    except:
        print '--- skip one page'
        return textCount
    divBox = tree.cssselect('div.msgBox')
    for box in divBox:
        textCount += 1
        print '--- {0} ---'.format(textCount)
        #默认输出数据
        try:
            #用户名
            print box.cssselect('div.userName > strong')[0].text_content()
            #内容，源网页编码有乱码，u'\u200b'为乱码，打印需要删除
            print box.cssselect('div.msgCnt')[0].text_content().replace(u'\u200b', '')
            #时间，多种显示格式
            # 57分钟前
            # 昨天 08:26
            # 7月4日 14:18
            print box.cssselect('a.time')[0].text_content()
            #全部转播和评论
            try:
                #若没有转播与评论
                print box.cssselect('a.zfNum > b.relayNum')[0].text_content()
            except:
                print '0'
            #点赞
            try:
                #若网页出错，没有生成该模块，实际有值也写为0
                print box.cssselect('div.funBox > a > span')[0].text_content()
            except:
                print '0'
        except:
            textCount -= 1
    return textCount

if __name__ == '__main__':
    crawl()
