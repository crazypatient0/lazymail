# -*- coding:utf-8 -*-
import time
import os
import checkmiss
from datetime import datetime
import requests
import tip
import pymysql
import datetime
def runpy():
    print('开始执行')
    re = os.system("python mail3.py")
    return re


def att():
    #print('run function att()')
    attempt = runpy()
    if attempt==0:
        return True
    else:
        return False


def sleeptime():
    #读取当时的系统时间
    curTime = datetime.datetime.now()
    #设置想要触发的目标时间，此处设置为17:48:30
    desTime = curTime.replace(hour=9, minute=0, second=0, microsecond=0)
    delta = desTime-curTime
    #把时间差转换成以秒为单位的时间
    skipSeconds = int(delta.total_seconds())
    sleepSeconds = skipSeconds+(24 * 60 * 60)  # 设置触发周期，此处设置为1天
    m, s = divmod(sleepSeconds, 60)
    h, m = divmod(m, 60)
    next_check_time = "%02d:%02d" % (h, m)
    warn = "next check time %s after " % next_check_time
    return sleepSeconds, warn


def doFirst():

    #读取当时的系统时间
    curTime = datetime.datetime.now()
    #设置想要触发的目标时间，此处设置为17:48:30
    desTime = curTime.replace(hour=9, minute=30, second=0, microsecond=0)
    delta = desTime-curTime
    #把时间差转换成以秒为单位的时间
    skipSeconds = int(delta.total_seconds())
    #print(skipSeconds)
    if skipSeconds == 0:
        return True
    else:
        if skipSeconds < 0:
            skipSeconds += 24*60*60 #设置触发周期，此处设置为1天
            m, s = divmod(skipSeconds, 60)
            h, m = divmod(m, 60)
            next_check_time = "%02d:%02d" % (h, m)
            print("next check time %s after" % next_check_time)
            time.sleep(s)
        return False


def heartbeatcheck(path, list):
    print('ok----begin check file')
    print('----------------------')
    res = checkmiss.heartbeatchange(path, list)
    setres = set(res)
    if len(setres)==1:
        print('----------all file download----------')
        return False
    else:
        f = open("file-miss-log.txt", mode='a')
        for i in range(len(res)):
            #print(type(res[i]).__name__)
            if type(res[i]).__name__ == 'str':
                print(res[i])
                tip.push(res[i])
                f.write(res[i])
        f.close()
        return True

def log():
    today1 = today.strftime("%Y-%m-%d")
    conn = pymysql.connect(host="localhost", user="root", password="1234", database="test")
    cursor = conn.cursor()
    sql = 'INSERT INTO dcs (rq,states) VALUES ("' + today1 + '","ok")'
    cursor.execute(sql)
    conn.commit()

def loop(path, list):
    while True:
        if doFirst():
            while True:
                try:
                    att()
                    tip.itchat.auto_login(hotReload=True)
                    tip.itchat.send_msg("老子登陆了哦")
                    res = heartbeatcheck(path, list)
                    while res:
                        print('waiting for check')
                        time.sleep(15*60)
                        att()
                        time.sleep(30)
                        res2 = heartbeatcheck(path, list)
                        if res2:
                            continue
                        else:
                            break
                    try:
                        os.system("python dailychart.py")
                    except BaseException:
                        msg = 'something wrong in 日报表, 请求人工支援'
                        print(msg)
                        tip.push(msg)
                        raise RuntimeError('testError')
                    try:
                        os.system("python stockchart.py")
                    except BaseException:
                        msg = 'something wrong in 动态表, 请求人工支援'
                        print(msg)
                        tip.push(msg)
                        raise RuntimeError('testError')
                    try:
                        os.system("python productionchart.py")
                    except BaseException:
                        msg = 'something wrong in 产销存, 请求人工支援'
                        print(msg)
                        tip.push(msg)
                        raise RuntimeError('testError')

                    #print(re4)
                    #msg = 'all-done-sleep\n%s'%sleeptime()[1]
                    #print(msg)
                    #tip.push(msg)
                    #tip.itchat.logout()
                except BaseException:
                    time.sleep(60*10)
                    continue
                else:
                    break
            msg = 'all-done-sleep\n%s'%sleeptime()[1]
            print(msg)
            log()
            tip.push(msg)
            tip.itchat.logout()
            try:
                requests.get(url, headers=headers)
            except BaseException:
                pass
            time.sleep(30)
            try:
                requests.get(url, headers=headers)
            except BaseException:
                pass
            time.sleep(sleeptime()[0]-60)
            #time.sleep(1)
        time.sleep(1)



if __name__ == '__main__':
    path = r'C:\Users\Administrator\Desktop\data'
    inputlist = ['日报表', '产销存', '动态表', '月报表']
    str3 = '产销存'
    db_date = ''
    url = "https://www.zj-elfa.xyz:3000/beebee"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36",
        }
    today = datetime.date.today()
    loop(path, inputlist)
