#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re,os,requests,pymysql

class Spider:
    def __init__(self, host, user, passwd, db):
        # self.url_set = []
        self.img_path = 'www.7rcm.com'
        self.url = 'http://www.7rcm.com/index.php?r=post/Index&catalog=news_center&page='
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.mysql = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, charset='utf8',cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.mysql.cursor()

    def run(self):
        try:
            for i in range(71, 73):
                self.GetUrl(self.url+str(i))
        except KeyboardInterrupt as e:
            print('[E] 退出')


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

    def GetUrl(self,url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        }
        req = requests.get(url, headers=headers)
        html = req.content.decode('utf-8')
        for var in re.findall(r'<dl class="news_dl">.*?</dl>', html, re.S):
            pic = re.findall(r'<img src=".*?">',var,re.S)[0]
            pic_d = 'http://www.7rcm.com/'+ pic.replace('<img src="', '').replace('">','').replace('\r\n', '').replace('\t', '').replace(' ', '')
            pic = pic.replace('<img src="', '').replace('uploads/','/caiji/').replace('">','').replace('\r\n', '').replace('\t', '').replace(' ', '')
            self.Download(pic_d)
            title = re.findall(r'<strong><em></em>.*?</strong>',var,re.S)[0]
            title = '短视频剪辑：'+title.replace('<strong><em></em>', '').replace('</strong>','').replace('\r\n', '').replace('\t', '').replace(' ', '')
            desc = re.findall(r'<p>.*?</p>',var,re.S)[0]
            desc = desc.replace('<p>','').replace('</p>','').replace('\r\n', '').replace('\t', '').replace('影匠传奇','巨推科技').replace('七人传媒','巨推传媒').replace('010-52907209','010-86399611')
            url = re.findall(r'<a href=".*?"',var,re.S)[0]
            url_one = 'http://www.7rcm.com'+url.replace('<a href="','').replace('\r\n','').replace('\t','').replace('"','')
            req_one = requests.get(url_one, headers=headers)
            html_one = req_one.content.decode('utf-8')
            for var in re.findall(r'<div class="news_content">.*?</div>', html_one, re.S):
                imgObj = re.findall(r'<img src=".*?"', var, re.S)
                if imgObj:
                    img = imgObj[0]
                    img = 'http://www.7rcm.com'+img.replace('<img src="','').replace('"','')
                    self.Download(img)
                content = ''
                for content_one in re.findall(r'<p.*?</p>', var, re.S):
                    content += content_one.replace('/uploads/','/caiji/').replace('\r\n', '').replace('\t', '').replace('影匠传奇','<a href="https://www.jutui.org">巨推科技</a>').replace('七人传媒','<a href="/">巨推传媒</a>').replace('010-52907209','010-86399611').replace('<div class="copyright">版权声明：本文来源于网络，文章版权属原作者所有。若涉及版权问题，敬请与我们联系删除。</div>','')
            insertStr = "'"+pymysql.escape_string(title)+"','"+pic+"','"+pymysql.escape_string(content)+"','"+pymysql.escape_string(desc)+"'"
            sqlStr = 'insert into jutui_content(title,img,content,description) value(' + insertStr + ')'
            self.cursor.execute(sqlStr)
            print(title)

Spider = Spider('127.0.0.1', 'root', '', 'jutui360')
Spider.run()
