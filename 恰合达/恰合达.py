import re,os,requests,json,pymysql,threading,time
from urllib.request import urljoin
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
        self.cursor.execute('select id,url from url where status = 0')
        result = self.cursor.fetchall()
        try:
            for url in result:
                imglist = self.imgpath(url['url'])
                brand_all = self.loadContent(url['url'])
                brand_all['create_t'] = str(int(time.time()))
                if 'canshu' in brand_all:
                    oneStr = "'"+brand_all['brand_name']+"','"+brand_all['title']+"','"+brand_all['cat']+"','"+imglist+"','"+brand_all['canshu']+"',"+brand_all['create_t']
                else:
                    oneStr = "'"+brand_all['brand_name']+"','"+brand_all['title']+"','"+brand_all['cat']+"','"+imglist+"','"+''+"',"+brand_all['create_t']
                sqlStr = 'replace into zhoucheng_new(brand,`name`,cat_name,img,canshu,create_t) value('+oneStr+')'
                self.cursor.execute('update url set status = 1 where id ='+str(url['id']))
                self.cursor.execute(sqlStr)
                print('[+]'+str(time.strftime("%H:%M:%S"))+'----'+str(url['id'])+'----'+brand_all['title'])
        except KeyboardInterrupt as e:
            print('[E] 退出')
    
    # 图片路径数据
    def imgpath(self,url,home_url = 'http://www.yhdfa.com/index.php?s=/home/type/index.html'):
        img_list = []
        img_url = {}
        html = requests.get(url).content.decode('utf-8')
        for index, img in enumerate(re.findall('Uploads/Picture/Code/.*?.jpg', html)):
            img = urljoin(home_url, img)
            filename = self.DownloadImg(img,'imgs')
            img_url[index] = filename
        img_list.append(img_url)
        return pymysql.escape_string(json.dumps(img_list))

    # 下载图片
    def DownloadImg(self,url, img_path):
        file_name = os.path.splitext(url)[0]
        file_suffix = os.path.splitext(url)[1]
        file_list = file_name.split('/')
        img_name = file_list.pop()
        img_brand = file_list.pop()
        img_paths = img_path + '/' + img_brand
        if not os.path.exists(img_paths):
            os.mkdir(img_paths)
        filename = '{}/{}{}'.format(img_paths, img_name, file_suffix)
        if not os.path.exists(filename):
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            res = requests.get(url, headers=headers)
            with open(filename, 'wb') as f:
                f.write(res.content)
        return filename

    ## 通过PhantomJS 获取js动态渲染的内容源码    
    def loadContent(self,url):
        brand_all = {}
        file_name = os.path.splitext(url)[0]
        file_list = file_name.split('/')
        brand_all['brand_name'] = file_list.pop()
        self.driver.get(url)
        base_msg = self.driver.page_source
        base_msg = base_msg.replace('\\', '')
        canshu = re.findall(r'<div id="caizhi_list".*?<div class="clear"></div>',base_msg,re.S)
        if canshu:
        	canshuStr = ''
        	canshuarr = re.findall(r'<div class="inline">.*?</div>',canshu[0],re.S)
        	for can in canshuarr:
        		canshuStr += can
        		brand_all['canshu'] = pymysql.escape_string(json.dumps(canshuStr))
        else:
            brand_all['canshu'] = ''
        cat_msg=self.driver.find_elements_by_xpath('//div[@class="ser-nav"]/a')
        for item in cat_msg:
            cat  = item.text
            if '首页' in cat:
                continue
            if '选型' in cat:
                continue
            brand_all['cat'] = cat
        title_msg = self.driver.find_elements_by_xpath('//h2[@id="foodname"]')
        for item in title_msg:
            title = item.text
            brand_all['title'] = title
        return brand_all

Spider = Spider('127.0.0.1','root','','zhoucheng')
Spider.GetUrl()
