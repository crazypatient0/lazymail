import itchat
from itchat.content import *


def friend():
    # 统计你的好友的男女比例
    # friends是一个类似列表的数据类型, 其中第一个是自己的信息， 除了第一个之外是你的好友信息.
    friends = itchat.get_friends()

    info = {}  # 'male':1, 'female':, 'other':          #存储信息
    for friend in friends[1:]:  # 获取好友信息
        if friend['Sex'] == 1:  # 判断好友性别，1为男性，2为女性，0为其他。
            info['male'] = info.get('male', 0) + 1
        elif friend['Sex'] == 2:
            info['female'] = info.get('female', 0) + 1
        else:
            info['other'] = info.get('other', 0) + 1
    print(info)


def push(msg):
    itchat.send(msg)  # 发送命令为hello 发送人为'filehelper'
    #itchat.send_file('etc/passwd', toUserName="filehelper")


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply(msg):
    myUserName = myname()
    if not msg['FromUserName'] == myUserName:
        # 群名 发消息人 信息
        #print(msg['User']['NickName'] + ' ' + msg['ActualNickName'] + ' ' + msg['Content'])
        if msg['User']['NickName'] == '测试群':
            itchat.send_image("C:\\Users\\Administrator\\Desktop\\wxlisten\\IMG_3498.PNG", myUserName)


@itchat.msg_register(itchat.content.TEXT, isFriendChat=True)
def general_reply(msg):
    #print('aa')
    msg.user.send('%s: %s' % (msg.type, msg.text))


@itchat.msg_register(itchat.content.PICTURE, isFriendChat=True)
def general_reply(msg):
    #print('aa')
    msg.user.send('%s: %s' % (msg.type, msg.text))

def myname():
    friends = itchat.get_friends()
    return friends[0].UserName


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.send_msg("老子登陆了哦")
    itchat.run()