import pymysql,os,time
import math
class Url:

    # def __init__(self, host, user, passwd, db):
    #     self.host = host
    #     self.user = user
    #     self.passwd = passwd
    #     self.db = db
    #     self.mysql = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    #     self.cursor = self.mysql.cursor()

    def run(self):
        # sqlStr = 'select id from zhoucheng'
        # self.cursor.execute(sqlStr)
        # res = self.cursor.fetchall()
        # count = math.ceil(len(res) / 2000)
        # all = []
        # for k in range(0, count):
        #     startsum = k * 2000
        #     endsum = (k + 1) * 2000
        #     list = res[startsum:endsum]
        #     all.append(list)

        path = '/Users/qiaoshuai/Desktop/python/urls'
        # for i in range(len(all)):
        #     fn = open(path+'/urls' + str(i) + '.txt', 'w')
        #     for f in all[i]:
        #         url = 'http://www.55zhoucheng.com/lingjian/show/' + str(f['id'])
        #         fn.write(url + "\n")
        #     fn.close()

        # if os.path.exists(path):
        domain = 'www.55zhoucheng.com'
        num = 0
        for file in os.listdir(path):
            pathname = path + '/' + file
            if file == '.DS_Store':
                continue
            # 网站提交地址
            cmd = "curl -H 'Content-Type:text/plain'" + ' --data-binary @' + pathname + ' "http://data.zz.baidu.com/urls?site="' + domain + '"&token=fPAlGeNXAUaDQiwm"'
            os.system(cmd)
            print(num)
            num = num + 1


# obj = Url('127.0.0.1','root','','zhoucheng')
obj = Url()
obj.run()