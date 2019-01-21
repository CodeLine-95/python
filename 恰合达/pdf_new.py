#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,pymysql

# for dir in os.listdir('/Users/qiaoshuai/Downloads/pdf'):
#     print(dir.split('.')[0])

mysql = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='zhoucheng', charset='utf8',cursorclass=pymysql.cursors.DictCursor)
cursor = mysql.cursor()

cursor.execute('select id,url from url')
result = cursor.fetchall()
url_set = set()
for dict in result:
    url_set.add(dict['url'])

for url in url_set:

    cursor.execute('replace into url_new(url) value("'+url+'")')