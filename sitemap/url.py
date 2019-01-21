import math
import os
def fileContent(dirpath):
    arr = []
    with open(dirpath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f.readlines():
            line = line.replace('\n','')
            arr.append(line)
    return arr
arr = fileContent('/Users/qiaoshuai/Desktop/sitemap/zhoucheng.txt')
arr_count = len(arr)+1
count = math.ceil(len(arr)/2000)
all = list = []
for k in range(0,count):
    startsum = k*2000
    endsum = (k+1)*2000
    print(endsum)
    list = arr[startsum:endsum]
    all.append(list)

path = '/Users/qiaoshuai/Desktop/sitemap/urls'
if not os.path.exists(path):
    os.makedirs(path)
for i in range(len(all)):
    fn = open(path+'/urls'+str(i)+'.txt', 'w')
    for f in all[i]:
        fn.write(str(f) + "\n")
    fn.close()