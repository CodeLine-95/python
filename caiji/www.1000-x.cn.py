#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re, os, datetime, requests, json, pymysql
from selenium import webdriver
import urllib.parse
import re


class Spider:
    def __init__(self, host, user, passwd, db):
        self.img_path = 'www.1000-x.cn'
        self.url = 'http://www.1000-x.cn/about/xin3/list_15_1.html'
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.mysql = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, charset='utf8',cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.mysql.cursor()

    ## 采集文字内容
    def select(self):
        self.GetUrl(self.url)

    #下载图片
    def Download(self,url):
        file_name = os.path.splitext(url)[0]
        file_suffix = os.path.splitext(url)[1]
        file_list = file_name.split('/')
        img_name = file_list.pop()
        img_brand = file_list.pop()
        img_paths = self.img_path + '/' + img_brand
        if not os.path.exists(img_paths):
            os.mkdir(img_paths)
        filename = '{}/{}{}'.format(img_paths, img_name, file_suffix)
        if not os.path.exists(filename):
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            res = requests.get(url, headers=headers)
            with open(filename, 'wb') as f:
                f.write(res.content)
        return filename

    def replaceCharEntity(self,htmlstr):
        CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                         'lt': '<', '60': '<',
                         'gt': '>', '62': '>',
                         'amp': '&', '38': '&',
                         'quot': '"', '34': '"', }

        re_charEntity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_charEntity.search(htmlstr)
        while sz:
            entity = sz.group()  # entity全称，如>
            key = sz.group('name')  # 去除&;后entity,如>为gt
            try:
                htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
            except KeyError:
                # 以空串代替
                htmlstr = re_charEntity.sub('', htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
        return htmlstr

    def repalce(self,s, re_exp, repl_string):
        return re_exp.sub(repl_string, s)

    def filter_tags(self,htmlstr):
        # 先过滤CDATA
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        re_br = re.compile('<br\s*?/?>')  # 处理换行
        re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        s = re_cdata.sub('', htmlstr)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_br.sub('\n', s)  # 将br转换为换行
        s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_comment.sub('', s)  # 去掉HTML注释
        # 去掉多余的空行
        blank_line = re.compile('\n+')
        s = blank_line.sub('\n', s)
        s = self.replaceCharEntity(s)  # 替换实体
        return s

    def GetUrl(self,url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        }
        req = requests.get(url, headers=headers)
        print(req)
        html = req.content.decode('utf-8')
        for var in re.findall(r'<div class="list">.*?</div>', html, re.S):
            pic = re.findall(r'<img src=".*?">',var,re.S)[0]
            pic_d = pic.replace('<img src="', '').replace('">','').replace('\r\n', '').replace('\t', '').replace(' ', '')
            pic = pic.replace('<img src="', '').replace('http://www.1000-x.cn/','').replace('uploads/','/caiji/').replace('">','').replace('\r\n', '').replace('\t', '').replace(' ', '')
            # self.Download(pic_d)
            titles = re.findall(r'<p>.*?</p>', var, re.S)
            title = self.filter_tags(titles[0])
            desc = self.filter_tags(re.search('<a.*?href="(.+)".*?>(.*?)</a>', titles[2]).group())
            href = re.search('<a.*?href="(.+)".*?>', var).group().replace('<a href="', '').replace('">', '')
            print(href)
            req_one = requests.get(href, headers=headers)
            html_one = req_one.content.decode('utf-8')
            content = re.findall(r'"article-text">.*?</div>', html_one, re.S)[0]
            print(content)
            # exit()

Spider = Spider('127.0.0.1', 'root', '', 'zhoucheng')
Spider.select()
