import time
import os, os.path
from pathlib import Path


def get_dir(path):
    dir = os.listdir(path)
    return dir


def search(path, str):
    # 如果文件存在 fp为文件路径
    filelist = []
    for x in os.listdir(path):
        filelist.append(x)
    a = [x for x in filelist if str in x]
    #print(a)
    return a


def check(path, str):
    #print(path)
    #print(str)
    res = search(path, str)
    #print(res)
    if res:
        pass
    else:
        warn = 'cant find"' + str + '"in' + path + '\n'
        file_miss_log(warn)
        #print(warn)
        return warn


def file_miss_log(l1):
    f = open("file-miss-log.txt", mode='a')
    f.write(l1)
    f.close()


def heartbeatchange(path, list):
    date = time.strftime("%Y-%m-%d")
    #print(date)
    reslist = []
    # print(list)
    path2 = path + '/' + date
    #生成当日报表的储存目录
    #print(path2)
    mypath = Path(path2)
    if mypath.is_dir():
        for i in range(len(list)):
            res = check(path2, list[i])
            #print(res)
            reslist.append(res)
    else:
        os.mkdir(path2)
        #没有目录新建一个的话，铁定返回三个warn
        for i in range(len(list)):
            res = check(path2, list[i])
            #print(res)
            reslist.append(res)

    return reslist


if __name__ == '__main__':
    path = r'C:\Users\Administrator\Desktop\XXX'#附件保存目录 attachment save folder
    inputlist = ['日报表','产销存','动态表']#表名总有几个固定的关键字，没有就gg算了 no fixed char in filename means "gg"
    date = time.strftime("%Y-%m-%d")
    #print(date)
    aa = heartbeatchange(path, inputlist)
    print(aa)
