#!/usr/bin/python3
# encoding: utf-8

import urllib.request
import json


TOKEN_URL = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
# 企业的id，在管理端->"我的企业" 可以看到
CORP_ID = "CORP_ID"
# 某个自建应用的id及secret, 在管理端 -> 企业应用 -> 自建应用, 点进相应应用可以看到
APP_ID=1000002
CORP_SECRET = "CORP_SECRET"

class Wechat(object):
    "send monitor message by wechat"
    def __init__(self):
        self.CORP_ID = CORP_ID
        self.CORP_SECRET = CORP_SECRET
        self.APP_ID = APP_ID
        self.BASEURL = 'https://qyapi.weixin.qq.com/cgi-bin/'
        self.TOKEN_URL = 'gettoken?corpid={0}&corpsecret={1}'.format(self.CORP_ID, self.CORP_SECRET)
        
    # 获取认证 token
    def Get_Token(self):
        try:
             response=urllib.request.urlopen('{0}{1}'.format(self.BASEURL,self.TOKEN_URL))
             access_token=json.loads(response.read().decode('utf-8'))['access_token']
             with open('token','w') as f:
                 f.write(access_token)
        except KeyError:
            raise KeyError
        return access_token

    # 本地 token
    def Local_Token(self):
        try:
            with open('token','r') as f:
                token = f.readline().strip()
                if token == '':
                    token = self.Get_Token()
                    return token
                else:
                    return token
        except IOError:
            token = self.Get_Token()
            return token

    # 获取报警人员名单
    def Get_User(self,dep_id=1,fchild=1):
        #token = self.Get_Token()
        token = self.Local_Token()
        send_url = '{0}user/list?access_token={1}&department_id={2}&fetch_child{3}'.format(self.BASEURL,token,dep_id,fchild,)
        respone=urllib.request.urlopen(url=send_url).read()
        stat = json.loads(respone)['userlist']
        user = ''
        for k in stat:
            user += '{0} '.format(k['mobile'])
        mobile = ','.join(user.split())
        with open('user.txt','w') as f:
            f.write(mobile)

    # 发送报警信息
    def Send_Message(self,content):
        self.content = {
                "touser": '@all',                        # 成员， @all及所有人
                "toparty": '1',                          # 部门，@all 及所有部门
                "msgtype": 'text',                       # 消息类型，文本，图片
                "agentid": self.APP_ID,                  # 企业应用 id
                "safe": "0",                             #
                "text": {
                    "content": content                   # 报警内容
                    }
                }
        token = self.Local_Token()
        # 构建告警信息，必须是 json 格式
        msg = messages_content=json.dumps(self.content)
        send_url = '{0}message/send?access_token={1}'.format(self.BASEURL,token)
        respone=urllib.request.urlopen(url=send_url, data=msg.encode("utf-8")).read()
        stat = json.loads(respone.decode())['errcode']
        if stat == 0:
            print('Succesfully Send To Wechat')
        else:
            token = self.Get_Token()
            send_url = '{0}message/send?access_token={1}'.format(self.BASEURL,token)
            respone=urllib.request.urlopen(url=send_url, data=msg).read()
            return respone

if __name__ == '__main__':
    msg = 'Warning 报警信息'
    wechat=Wechat()
    wechat.Send_Message(msg)