#!/usr/bin/env python3

import itchat
import requests

# 图灵机器人KEY
KEY = ''
# 群组名称
GROUPS = ('')
# 好友名称
FRIENDS = ('', '')


def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': 'wechat-robot'
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return


@itchat.msg_register([itchat.content.TEXT, itchat.content.PICTURE], isGroupChat=True, isFriendChat=True)
def tuling_reply(msg):
    if manger_jur(msg):
        if (msg['MsgType'] == 1):
            defaultReply = 'I received: ' + msg['Text']
            reply = get_response(msg['Text'])
            return reply or defaultReply
        elif (msg['MsgType'] == 47):
            NickName = msg['User']['NickName']
            reply = u"%s,过分了啊！欺负我变形金刚？" % NickName
            return reply
    else:
        print(msg['User']['NickName'] + ': ' + msg['Text'])


# 指定群名or好友昵称
def manger_jur(msg):
    if msg['User']['NickName'] in GROUPS \
            or msg['User']['NickName'] in FRIENDS:

        return True
    else:
        return False


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()
