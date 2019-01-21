#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re, os, datetime, requests, json, pymysql, json
from selenium import webdriver
import urllib.parse
import re
class Spider:
    def __init__(self, host, user, passwd, db):
        self.url_set = set()
        self.url = 'https://baike.baidu.com/item/'
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.mysql = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, charset='utf8',cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.mysql.cursor()

    ## 采集文字内容
    def select(self):
        sqlStr = 'select title as cat_name from cate_new'
        self.cursor.execute(sqlStr)
        Arr = self.cursor.fetchall()
        for oneArr in Arr:
            findOne = {}
            name = urllib.parse.quote(oneArr['cat_name'])
            name.encode('utf-8')
            html = self.getUrl('https://baike.baidu.com/item/'+name)
            # html = self.getUrl('https://baike.baidu.com/item/%E7%94%B5%E6%BA%90%E6%8F%92%E5%A4%B4')
            htmls = html.replace('\\', '')
            table = re.findall('<table log-set-param="table_view".*?</table>',htmls,re.S)
            for ta in table:
                # print(type(ta))
                htmls = htmls.replace(str(ta),'')
            # 简介内容
            content = ''
            for var in re.findall('<div class="para".*?</div>',htmls):
                content += var
            findOne['content'] = content
            # 关键字图片
            summary = re.findall(r'<div class="summary-pic".*?</div>',htmls,re.S)
            if summary:
                picarr = re.findall(r'src=".*?"',summary[0],re.S)
                pic = picarr[0].replace('src=','')
                pic = pic.replace('"','')
                findOne['pic'] = pic
            else:
                findOne['pic'] = ''
            images = re.findall(r'<div class="zhixin-item.*?</div>',htmls,re.S)
            lists = []
            for value in images:
                like = {}
                # 相关标题
                titlearr = re.findall(r'alt=".*?"',value,re.S)
                title = titlearr[0].replace('alt=','')
                title = title.replace('"','')
                # 相关图片
                imgarr = re.findall(r'src=".*?"',value,re.S)
                img = imgarr[0].replace('src=','')
                img = img.replace('"','')
                #拼接成字典
                like['liketitle'] = title
                like['likeimg'] = img
                lists.append(like)
            findOne['like'] = lists
            # print(json.dumps(findOne['like']));
            try:
                # oneStr = "'"+oneArr['cat_name']+"','"+pymysql.escape_string(findOne['content'])+"','"+findOne['pic']+"','"+pymysql.escape_string(json.dumps(findOne['like']))+"'"
                sqlStr = "update cate_new set likecontent = '"+pymysql.escape_string(json.dumps(findOne['like']))+"' where title = '"+oneArr['cat_name']+"'"
                self.cursor.execute(sqlStr)
                print(oneArr['cat_name'])
            except Exception as e:
                continue
            
    
    ## 打开js渲染的动态数据
    def getUrl(self,url):
        ua = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36"
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 200000
        cap["phantomjs.page.settings.loadImages"] = True
        cap["phantomjs.page.settings.disk-cache"] = True
        cap["phantomjs.page.settings.userAgent"] = ua
        cap["phantomjs.page.customHeaders.User-Agent"] = ua
        cap["phantomjs.page.customHeaders.Referer"] = "http://tj.ac.10086.cn/login/"
        self.driver = webdriver.PhantomJS(desired_capabilities=cap, service_args=['--ignore-ssl-errors=true'])
        self.driver.get(url)
        base_msg = self.driver.page_source
        self.driver.quit()
        return base_msg

Spider = Spider('127.0.0.1', 'root', '', 'zhoucheng')
Spider.select()
