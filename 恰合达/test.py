#!/usr/bin/env python
# -*- coding:utf-8 -*-
from urllib.request import urlopen,urlretrieve,urljoin
import requests,pymysql,json
import gzip
import re
import os
url = 'http://www.yhdfa.com/index.php?s=/home/type/index.html'
url_set = []
path = 'img'
mysql = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='zhoucheng', charset='utf8',cursorclass=pymysql.cursors.DictCursor)
cursor = mysql.cursor()
'''
列表去重函数
'''
def Repeat(lists):
    listArr = list(set(lists))
    listArr.sort(key=lists.index)
    return listArr

#/index.php?s=/home/series/series/typeno/A08.html
def GetUrl(url,home_url = 'http://www.yhdfa.com/index.php?s=/home/type/index.html'):
    global url_set
    html = requests.get(url).content.decode('utf-8')
    for url in re.findall('/index.php\?s=/home/series/series/typeno/\w+.html', html):
        url = urljoin(home_url,url)
        htmls =requests.get(url).content.decode('utf-8')
        for var in re.findall('/index.php\?s=/home/detail/detail/xlno/\w+.html',htmls):
            img_list = []
            img_url = {}
            var = urljoin(home_url,var)
            file_name = os.path.splitext(var)[0]
            file_list = file_name.split('/')
            brandname = file_list.pop()
            html = requests.get(var).content.decode('utf-8')
            for index,img in enumerate(re.findall('Uploads/Picture/Code/.*?.jpg',html)):
                img = urljoin(home_url,img)
                filename = DownloadImg(img,path)
                img_url[index] = filename
            img_list.append(img_url)
            sql = 'update zhoucheng set img="'+pymysql.escape_string(json.dumps(img_list))+'" where brand = "'+brandname+'"';
            cursor.execute(sql)
            print(brandname)

def DownloadImg(url,img_path):
    file_name = os.path.splitext(url)[0]
    file_suffix = os.path.splitext(url)[1]
    file_list = file_name.split('/')
    img_name = file_list.pop()
    img_brand = file_list.pop()
    img_paths = img_path+'/'+img_brand
    if not os.path.exists(img_paths):
        os.mkdir(img_paths)
    filename = '{}/{}{}'.format(img_paths,img_name,file_suffix)
    if not os.path.exists(filename):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        res = requests.get(url,headers=headers)
        with open(filename, 'wb') as f:
            f.write(res.content)
    return filename


GetUrl(url)
# img_url = Repeat(url_set)



    



