# _*_ coding: utf-8 _*_
import os
import poplib
from pathlib import Path
from email.parser import Parser
from email.utils import parseaddr
from datetime import datetime, date
from email.header import decode_header


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        if charset == 'gb2312':
            charset = 'gb18030'
        value = value.decode(charset)
    return value

def get_email_headers(msg):
    headers = {}
    for header in ['From', 'To', 'Cc', 'Subject', 'Date']:
        value = msg.get(header, '')
        if value:
            if header == 'Date':
                headers['Date'] = value
            if header == 'Subject':
                subject = decode_str(value)
                headers['Subject'] = subject
            if header == 'From':
                hdr, addr = parseaddr(value)
                name = decode_str(hdr)
                from_addr = u'%s <%s>' % (name, addr)
                headers['From'] = from_addr
            if header == 'To':
                all_cc = value.split(',')
                to = []
                for x in all_cc:
                    hdr, addr = parseaddr(x)
                    name = decode_str(hdr)
                    to_addr = u'%s <%s>' % (name, addr)
                    to.append(to_addr)
                headers['To'] = ','.join(to)
            if header == 'Cc':
                all_cc = value.split(',')
                cc = []
                for x in all_cc:
                    hdr, addr = parseaddr(x)
                    name = decode_str(hdr)
                    cc_addr = u'%s <%s>' % (name, addr)
                    cc.append(to_addr)
                headers['Cc'] = ','.join(cc)
    return headers

def get_email_content(message, savepath):
    attachments = []
    for part in message.walk():
        filename = part.get_filename()
        if filename:
            filename = decode_str(filename)
            data = part.get_payload(decode=True)
            abs_filename = os.path.join(savepath, filename)
            attach = open(abs_filename, 'wb')
            attachments.append(filename)
            attach.write(data)
            attach.close()
    return attachments
#上面3个函数是从大佬地方抄来的，用就是了
def loglog(l1,l2,l3,l4,l5):
    f = open("log.txt",mode='a')
    f.write(l1)
    f.write(l2)
    f.write(l3)
    f.write(l4)
    f.write(l5)
    f.close()

def main():
    # 账户信息
    email = 'qqmail'
    password = 'authcode'  # 是授权码不是密码，详情请百度
    pop3_server = 'pop.qq.com'
    # 连接到POP3服务器，带SSL的:
    server = poplib.POP3_SSL(pop3_server, 995, timeout=10)
    # 可以打开或关闭调试信息:
    server.set_debuglevel(0)
    # POP3服务器的欢迎文字:
    # print(server.getwelcome())
    # 身份认证:
    server.user(email)
    server.pass_(password)
    # stat()返回邮件数量和占用空间:

    msg_count, msg_size = server.stat()
    print('-----------------------------')
    print('message count:', msg_count)
    print('-----------------------------')
    # b'+OK 237 174238271' list()响应的状态/邮件数量/邮件占用的空间大小

    for i in range(1, msg_count + 1):
        resp, byte_lines, octets = server.retr(i)
        # 转码
        str_lines = []
        for x in byte_lines:
            str_lines.append(x.decode())
        # 拼接邮件内容server.quit()
        msg_content = '\n'.join(str_lines)
        # 把邮件内容解析为Message对象
        msg = Parser().parsestr(msg_content)
        headers = get_email_headers(msg)
        if headers:
            path = r'C:\Users\Administrator\Desktop\XXXX'  # 自定义一个路径
            rq = headers['Date'][5:16]
            rq = rq.strip()
            rq2 = str(rq).replace("Jan", "1").replace("Feb", "2").replace("Mar", "3").replace("Apr", "4").replace("May",
                                                                                                                  "5").replace(
                "Jun", "6").replace("Jul", "7").replace("Aug", "8").replace("Sep", "9").replace("Oct", "10").replace(
                "Nov", "11").replace("Dec", "12").replace(" ", "-")
            rq3 = datetime.strptime(rq2, "%d-%m-%Y")  # 修改了一下日期格式，按需自取
            rq4 = str(rq3)[0:10]
            path2 = path + '/' + rq4
            mypath = Path(path2)
            if mypath.is_dir():
                attachments = get_email_content(msg, path2)
            else:
                os.mkdir(path2)
                attachments = get_email_content(msg, path2)
            l1 = '-----------------------------\n'
            l2 = str(rq4) + '\n'
            l3 = 'subject:%s\n' % headers['Subject']
            l4 = 'attachments:%s\n' % attachments
            l5 = '-----------------------------\n'
            print(l1)
            print(l2)
            print(l3)
            print(l4)
            print(l5)
            # 打印一下 有意想不到的好处！print for unexpectable benifit!
            loglog(l1, l2, l3, l4, l5)
            # 写日志是个没卵用的好习惯！loglog has no egg use!
            server.dele(i)
            # 这太重要了，读取邮件以后删掉这封邮件，下次就不会重复读取， 也不需要去辨别flag看已读未读！nice try!
    server.quit()
    # 主动quit 免得出幺蛾子！

if __name__ == '__main__':
    main()