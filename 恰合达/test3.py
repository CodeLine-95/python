#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re,os,datetime,requests,json,pymysql,threading
from urllib.request import urlopen,urlretrieve,urljoin
from selenium import webdriver

class Spider:
    def __init__(self, host, user, passwd, db):
        self.url_set = []
        self.url = 'http://www.yhdfa.com/index.php?s=/home/type/index.html'
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        self.driver = webdriver.PhantomJS(desired_capabilities=cap)
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.mysql = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, charset='utf8',cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.mysql.cursor()

    def GetUrl(self):
        for i in range(1,9130,1000):
            print(i)
            
        
    ## 通过PhantomJS 获取js动态渲染的内容源码    
    def loadContent(self,url):
        brand_all = {}
        brand_arr = {}
        file_name = os.path.splitext(url)[0]
        file_list = file_name.split('/')
        brand_all['brand_name'] = file_list.pop()
        self.driver.get(url)
        base_msg=self.driver.find_elements_by_xpath('//div[@id="caizhi_list"]//div')
        for item in base_msg:
            textStr = item.text
            if '产品种类' in textStr or '种类' in textStr:
                ProducTypes = textStr.replace('产品种类','')
                ProducTypes = textStr.replace('种类','')
                brand_arr['ProducTypes'] = ProducTypes

            if '形状图片' in textStr or '形状图片名称' in textStr:
                ShapePicture = textStr.replace('形状图片','')
                ShapePicture = textStr.replace('名称','')
                brand_arr['ShapePicture'] = ShapePicture

            if '材质' in textStr:
                material = textStr.replace('材质','')
                brand_arr['material'] = material

            if '类型' in textStr:
                types = textStr.replace('类型','')
                brand_arr['type'] = types

            if '精度等级' in textStr:
                PrecisionGrade = textStr.replace('精度等级','')
                brand_arr['PrecisionGrade'] = PrecisionGrade

            if '表面处理' in textStr:
                surface = textStr.replace('表面处理','')
                brand_arr['surface'] = surface

            if '轴公差' in textStr:
                AxisTolerance = textStr.replace('轴公差','')
                brand_arr['AxisTolerance'] = AxisTolerance

            if '轴端形状' in textStr:
                BearingShape = textStr.replace('轴端形状','')
                brand_arr['BearingShape'] = BearingShape

            if '轴身加工' in textStr:
                BearingProcessing = textStr.replace('轴身加工','')
                brand_arr['BearingProcessing'] = BearingProcessing

            if '制作工艺' in textStr:
                Manufacturing = textStr.replace('制作工艺','')
                brand_all['Manufacturing'] = Manufacturing

            if '轴固定方式' in textStr:
                AxialFixation = textStr.replace('轴固定方式','')
                brand_all['AxialFixation'] = AxialFixation

            if '外形' in textStr:
                appearance = textStr.replace('外形','')
                brand_all['appearance'] = appearance

            if '选择安装尺寸' in textStr:
                InstallationSize = textStr.replace('选择安装尺寸','')
                brand_all['InstallationSize'] = InstallationSize

            if '丝杠精度等级' in textStr:
                PrecisionGradeofScrew = textStr.replace('丝杠精度等级','')
                brand_all['PrecisionGradeofScrew'] = PrecisionGradeofScrew

            if '滑块长度' in textStr:
                SliderLength = textStr.replace('滑块长度','')
                brand_all['SliderLength'] = SliderLength

            if '滑块高度尺寸' in textStr:
                SliderHeightSize = textStr.replace('滑块高度尺寸','')
                brand_all['SliderHeightSize'] = SliderHeightSize

            if '防尘盖' in textStr:
                DustCover = textStr.replace('防尘盖','')
                brand_all['DustCover'] = DustCover

            if '孔类形' in textStr:
                Orifice = textStr.replace('孔类形','')
                brand_all['Orifice'] = Orifice

            if '安装形式' in textStr:
                Installation = textStr.replace('安装形式','')
                brand_all['Installation'] = Installation

            if '压把类型' in textStr:
                PressType = textStr.replace('压把类型','')
                brand_all['PressType'] = PressType

            if '底座类型' in textStr:
                baseType = textStr.replace('底座类型','')
                brand_all['baseType'] = baseType

            if '型材/专用配件' in textStr:
                Profile = textStr.replace('型材/专用配件','')
                brand_all['Profile'] = Profile

            if '型材系列' in textStr:
                series = textStr.replace('型材系列','')
                brand_all['series'] = series

        brand_all['canshu'] = brand_arr
        cat_msg=self.driver.find_elements_by_xpath('//div[@class="ser-nav"]/a')
        for item in cat_msg:
            cat  = item.text
            if '首页' in cat:
                continue
            if '选型' in cat:
                continue
            brand_all['cat'] = cat
            # brand_all['cat_type'] = item.text
        title_msg = self.driver.find_elements_by_xpath('//h2[@id="foodname"]')
        for item in title_msg:
            title = item.text
            brand_all['title'] = title
        # exit()
        # return json.dumps(brand_all)
        return brand_all


Spider = Spider('127.0.0.1','root','','zhoucheng')
Spider.GetUrl()

    



