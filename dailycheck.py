# -*- coding:utf-8 -*-
import os
import tip
import time
import mail
import pymysql
import requests
import datetime
import checkmiss
from datetime import datetime


def runpy():
    print('开始执行')
    re = mail.main()
    return re


def att():
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
    #用res控制，如果文件存在，则会返回n个none，set（res）就是1
    if len(setres)==1:
        print('----------all file download----------')
        return False
    else:
        return True

def log():
    today1 = today.strftime("%Y-%m-%d")
    conn = pymysql.connect(host="localhost", user="root", password="1234", database="test")
    cursor = conn.cursor()
    sql = 'INSERT INTO dcs (rq,states) VALUES ("' + today1 + '","ok")'
    cursor.execute(sql)
    conn.commit()
    #在数据库里记一下，给小程序做查询控制的，按需取用


def loop(path, list):
    #主逻辑函数
    while True:
        if doFirst():
            while True:
                try:
                    att()
                    tip.itchat.auto_login(hotReload=True)
                    tip.itchat.send_msg("老子登陆了哦")
                    #到达设定时间时 先检测邮箱，自测了一个多月 att没有error过，所以吧att判断部分去掉了
                    #然后用itchat登陆微信，唯一的不足是得定期扫码，平时得在手机确认登陆，要是能绕过就完美了
                    res = heartbeatcheck(path, list)
                    #如果文件缺少，说明还没收到邮件 返回true
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
                        #检测文件缺少的话就睡15分钟再跑一遍
                    try:
                        os.system("python dailychart.py")#别问，问就是懒得
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
                    #如果从excel取数到mysql抛出错误，大概率是表格格式变了，睡眠十分钟等待人工修复
                    time.sleep(60*10)
                    continue
                else:
                    break
            msg = 'all-done-sleep\n%s'%sleeptime()[1]
            print(msg)
            log()
            tip.push(msg)
            tip.itchat.logout()
            #通知管理员，进程完美结束，下线
            try:
                requests.get(url, headers=headers)
            except BaseException:
                pass
            time.sleep(30)
            try:
                requests.get(url, headers=headers)
            except BaseException:
                pass
            #上面两个是小程序的调用api，有做小程序的大神吗，求带
            time.sleep(sleeptime()[0]-60)
            #time.sleep(1)
        time.sleep(1)



if __name__ == '__main__':
    path = r'C:\Users\Administrator\Desktop\XXX'#爱存哪里存哪里
    inputlist = ['日报表', '产销存', '动态表', '月报表']#附件关键字
    db_date = ''
    url = "小程序日报提醒控制api 请按需取用"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36",
        }
    today = datetime.date.today()
    loop(path, inputlist)
