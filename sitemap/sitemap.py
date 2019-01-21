#--* utf-8 *--
import os
# 链接地址文件路径（最好是绝对路径）
path = '/Users/qiaoshuai/Desktop/sitemap/urls'
domain = 'www.gzpgs88.cn'
num = 0
for file in os.listdir(path):
    pathname = path+'/'+file
    if file == '.DS_Store':
        continue
    # 网站提交地址
    cmd = "curl -H 'Content-Type:text/plain'"+' --data-binary @'+pathname+' "http://data.zz.baidu.com/urls?site="'+domain+'"&token=YNnUyTRcXGksCBtR"'
    os.system(cmd)
    print(num)
    num = num+1
