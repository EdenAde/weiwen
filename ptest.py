#coding:utf-8
# from pyquery import PyQuery as pyq
# import requests
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
# from pyquery import PyQuery as pyq
# import re
# import time
# from BeautifulSoup import *
# from selenium import webdriver
# from selenium.webdriver.common.by import By

import base64
# doc = pyq(url=r'http://opac.nlc.cn/F/6S28J759DXN9PGJ2SC155TLFRSDI9F6K728N1X2NM9K6S9315E-02178?func=find-b&find_code=ISB&request=9787504566959&local_base=NLC01&filter_code_1=WLN&filter_request_1=&filter_code_2=WYR&filter_request_2=&filter_code_3=WYR&filter_request_3=&filter_code_4=WFM&filter_request_4=&filter_code_5=WSL&filter_request_5=',encoding="utf-8")
# cts2 = doc('td')
#
# cover = doc("img")
# #coversrc = cover.attr('src')
# pattern = re.compile(r"ISBN: (.*) CNY")
# pattern2 = re.compile(r"CNY(.*)\s")
#
# match = re.findall(pattern,doc.html())
# match2 = re.findall(pattern2,doc.html())
# print match[0]
# print match2[0]
#
# for i in cts2:
#     if (pyq(i).text() == 'ID 号'):
#         idhao = pyq(i).nextAll().text()
#         print idhao
#     if(pyq(i).text()=='题名与责任'):
#         title = pyq(i).nextAll().text()
#         print title
#     if (pyq(i).text() == '版本项'):
#         banci = pyq(i).nextAll().text()
#         print banci
#     if (pyq(i).text() == '出版项'):
#         publisher = pyq(i).nextAll().find('a').text()
#         print publisher
#     if (pyq(i).text() == '载体形态项'):
#         td4text = pyq(i).nextAll().text()
#         td4s = td4text.split(';')
#         print td4s
#     if (pyq(i).text() == '语言'):
#         eng = pyq(i).nextAll().text()
#         print eng
#     if (pyq(i).text() == '内容提要'):
#         td5 = pyq(i).nextAll().text()
#         print td5
#     if (pyq(i).text() == '中图分类号'):
#         td6 = pyq(i).nextAll().text()
#         print td6
#     if (pyq(i).text() == '著者'):
#         td7 = pyq(i).nextAll().text()
#         print td7



# def get_article_url():
#
#     driver = webdriver.PhantomJS(executable_path='/Users/guizhouyuntushidai/PycharmProjects/lehman/odoo10/others/phantomjs/bin/phantomjs')
#     #driver = webdriver.PhantomJS()
#     # executable_path为你的phantomjs可执行文件路径
#     driver.get("http://opac.nlc.cn/")
#     time.sleep(1)
#
#     source = driver.page_source.encode('utf-8', 'ignore')
#     bsObj = BeautifulSoup(driver.page_source)
#     form1,form2 = bsObj.findAll('form')
#     print form1['action']
    #print form1['action']
    #print(driver.find_element_by_id('comment-box').text.encode('GBK', 'ignore'))

    #open('163.txt', 'w').write(source)
    #r = driver.execute_script("return session")
    #print r


# def get_article_url2():
#     driver = webdriver.Firefox()
#     try:
#         driver.get("http://music.163.com/#/song?id=31877470")
#     except selenium.common.exceptions.TimeoutException:
#         print("time out of 10 s")
#         driver.execute_script('window.stop()')
#
#     print(u"休眠结束")
#     driver.switch_to.frame("contentFrame")
#     time.sleep(5)
#     # print(driver.find_element_by_id('comment-box').text.encode('GBK', 'ignore'))
#     bsObj = BeautifulSoup(driver.page_source)
#     source = driver.page_source.encode('GBK', 'ignore')
#     open('163.txt', 'w').write(source)  # 163.txt文件可以看到精彩评论的
#Guxsdo

str = "R3V4c2Rv5a6e5oiYIyM+6JGb57qi5YSS6JGXPuacuuaisOW3peS4muWHuueJiOekvj7ljJfkuqw+NTM0NjE6PkZRXDs8MTMzPjg5M+mhtT40PGZwPmZrbD7lrp7miJjns7vliJc+V1M2PDYxMzw1Pue9keermT7mnKzkuabkvZzogIXmmK/lm73lhoVHdXhzZG/poobln5/nmoTmnYPlqIHvvIzmnIk45bm05Lul5LiK55qER3V4c2Rv5byA5Y+R57uP6aqM77yM5LiN5LuF5Zyo5Li6R3V4c2Rv6LSh54yu5Luj56CB77yM6ICM5LiU5pKw5YaZ5LqG5aSa5pysR3V4c2Rv5pWZ56iL5Zyo5reY5a6d5LiK6ZSA5ZSu77yM5Y+W5b6X5LqG5LiN6ZSZ55qE6ZSA5ZSu5Lia57up77yM5omA5Lul5pys5Lmm55qE5p2D5aiB5oCn5piv5q+L5bq4572u55aR55qE44CC5YWo5Lmm5LiA5YWxNDbnq6DvvIzlrpfml6jmmK/mj5Dpq5jor7vogIXnmoTlrp7miJjog73lipvvvIzlhajkuabku6XkuIDkuKrnu7zlkIjmoYjkvovvvIjlm77kuabplIDllK7nvZHnq5nvvInotK/nqb/lhajkuabvvIzku6Xov63ku6PnmoTmlrnlvI/orrLop6PkuoblpoLkvZXliKnnlKhHdXhzZG/mnoTlu7rkuIDkuKrnu7zlkIjmgKfnmoTlm77kuabnlLXlrZDllYbliqHnvZHnq5njgILnrKw056ug6YeN54K55a+5R3V4c2Rv55qE5a6J6KOF5ZKM6YWN572u6L+b6KGM5LqG5LuL57uN77yb56ysNeeroOS+v+W8gOWni+aehOW7uue7vOWQiOahiOS+i+eahOi9ruW7k++8jOiuvuiuoeWQhOenjeWtl+auteetie+8m+esrDbnq6DorrLop6PkuoblpoLkvZXorr7nva7ot6/lvoTliKvlkI3jgIHlm77niYflkozmoLflvI/ooajvvJvnrKw356ug5ZKM56ysOOeroOWImeiusuino+S6huWmguS9leWItuS9nOS4u+mimOWSjOmmlumhte+8m+esrDnnq6Dku4vnu43kuoZYZWh1ZmR1d+eahOWfuuacrOmFjee9ru+8m+esrDrCgTQz56ug5YiZ6K6y6Kej5LqG5aaC5L2V5a6e546w56uZ5YaF5pCc57Si44CB5re75Yqg56S+5Yy65LqS5Yqo5Yqf6IO944CBU2RxaG925o6n5Lu255qE5L2/55So77yM5Lul5Y+K5aaC5L2V5a6a5Yi25Liq5Lq65Li76aG177yb56ysNDTnq6Dlkow0NeeroOWImeiusuino+S6hkd1eHNkb+eahFZIUuWSjOaAp+iDveS8mOWMlu+8m+esrDQ256ug5LuL57uN5LqG5ZWG5ZOB5pWw5o2u55qE5a+85YWl5ZKM5a+85Ye644CC"
# get_article_url()
str2 = base64.urlsafe_b64decode(str)

s = b"Drupal"
a = base64.b64encode(s)
print(a)
bb = base64.b64encode(a)
print(bb)
print (base64.b64encode(bb))

# str1 = 'djhui'
# str2 = base64.b64encode(str1)
# str3 = base64.b64decode(str2)

#print(base64.urlsafe_b64decode(str2))