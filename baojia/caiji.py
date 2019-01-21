#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests,re,pymysql

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Cookie': 'JSESSIONID=009F5F5AAF92A98BBF94310925D04429; Hm_lvt_2707ce99e993c6c477bb5d0b5e15d36c=1529457174; Hm_lpvt_2707ce99e993c6c477bb5d0b5e15d36c=1529457325; ksndb=success; Hm_lvt_583ee22dd97d57ccd5f3eeefe1b7eff4=1529457175; Hm_lpvt_583ee22dd97d57ccd5f3eeefe1b7eff4=1529457325; LiveWSPAT42147503=1529457180031687463036; LiveWSPAT42147503sessionid=1529457180031687463036; NPAT42147503fistvisitetime=1529457180355; NPAT42147503lastvisitetime=1529457325556; NPAT42147503visitecounts=1; NPAT42147503visitepages=5; NPAT42147503IP=%7C58.210.116.234%7C; NPAT42147503lastinvite=1529457325672; Market.mrobay.com=ksndb*820b208c3830415b80a5068b4eda0786'
}
mysql = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='zhoucheng', charset='utf8',cursorclass=pymysql.cursors.DictCursor)
cursor = mysql.cursor()
for i in range(1, 2968):
    url = 'http://zc.mrobay.com/xianhuo/?Cal=0-0-0-0-0-0-0-0-Page'+str(i)+'.html'
    # print(url)
    # 构造访问请求
    req = requests.get(url, headers=headers)
    html = req.content.decode('utf-8')
    for var in re.findall(r'onmouseover="do_zyselect.*?</tr>',html,re.S):
        brand = re.findall('">.*</a>',re.findall('<span onmouseover="show_spinfo_pm.*</span>',var,re.S)[0])
        brand = brand[0].replace("'",'').replace('</a>','').replace('">','')
        # print(brand)
        price = re.findall('<td style="text-align:center;">.*?</td>',var,re.S)
        price = price[0].replace('<td style="text-align:center;">','').replace('\r\n','').replace('\t','').replace(' ','').replace('</td>','').replace('￥','')
        # print(price)
        num = re.findall('<td style="text-align:center">.*?</td>',var,re.S)
        num = num[0].replace('<td style="text-align:center">','').replace('<!-- 供应量 -->','').replace('\r\n','').replace('\t','').replace('<!-- 求购量 -->','').replace(' ','').replace('</td>','').replace('<span>','').replace('</span>','')
        # print(num)
        branddict = {}
        branddict['brand'] = brand
        branddict['price'] = price
        branddict['num'] = num
        Str = '"'+branddict['brand']+'","'+branddict['price']+'","'+branddict['num']+'"'
        sqlStr = 'replace into price(brand,price,num) value (' + Str + ')'
        cursor.execute(sqlStr)
        print(str(i)+'--'+branddict['brand']+'--'+branddict['num']+'--'+branddict['price'])
    # exit()