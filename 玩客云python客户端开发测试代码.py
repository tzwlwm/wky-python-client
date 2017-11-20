#以下测试代码由明日编写（QQ：198317745，赚钱宝、玩客交流Q群：527622951）
#其中pwd的加密方式与sign值的获取方式学习参照了“不朽玩客云客户端”的相关代码，在此对该作者表示感谢！！！
#玩客云python客户端开发代码存放于GitHub站点（链接：https://github.com/tzwlwm/wky-python-client）
#不朽玩客云客户端源代码位于GitHub站点（链接：https://github.com/Immortalt/imt-wanke-client）

#MD5函数
def md5(s):
    import hashlib
    return hashlib.md5(s.encode('utf-8')).hexdigest().lower()


#获取pwd值（密码MD5后加密再取MD5值）
def GetPwd(passwd):
    s = md5(passwd)
    s = s[0:2] + s[8] + s[3:8] + s[2] +s[9:17] + s[27] + s[18:27] + s[17] + s[28:]
    return md5(s)


#获取sign值
def GetSign(body, k=''):
    l = []
    while len(body) != 0:
        v = body.popitem()
        l.append(v[0]+ '=' + v[1])
    l.sort()
    t = 0
    s = ''
    while t != len(l):
        s = s + l[t] + '&'
        t = t+1
    s = s + 'key=' + k
    sign = md5(s)
    return sign


import requests
import json
headers = {'user-agent': "Mozilla/5.0"}
#登陆
#https://account.onethingpcs.com/user/login?appversion=1.4.8    （POST）
phone = '13000000000'    #测试时请替换为已注册玩客云的手机号
deviceid = md5(phone)[0:16].upper()
imeiid = str(pow(int(phone), 2))[0:14]
pwd = GetPwd('12345678')    #测试时请替换为对应手机号的密码
body = dict(deviceid = deviceid, imeiid = imeiid, phone = phone, pwd = pwd, account_type = '4')
sign = GetSign(body)
body = dict(deviceid = deviceid, imeiid = imeiid, phone = phone, pwd = pwd, account_type = '4', sign = sign)
url = 'https://account.onethingpcs.com/user/login?appversion=1.4.8'
cookies = None
r = requests.post(url = url, data = body, verify = False, headers = headers, cookies = cookies, timeout = 10)
sessionid = r.cookies.get('sessionid')
userid = r.cookies.get('userid')


#获取近期收益
#https://account.onethingpcs.com/wkb/income-history    （POST）
url = 'https://account.onethingpcs.com/wkb/income-history'
body = dict(page='0', appversion='1.4.8', sign=sign)
cookies = dict(sessionid=sessionid, userid=userid, origin='1')
r = requests.post(url=url, data=body, verify = False, headers=headers, cookies=cookies, timeout=10)
result = json.loads(r.content.decode('utf-8'))


#提币记录
#https://account.onethingpcs.com/wkb/outcome-history?page=0    （POST）
url='https://account.onethingpcs.com/wkb/outcome-history?page=0'
body = None
cookies = dict(sessionid = sessionid, userid = userid, origin='1')
r = requests.post(url=url, data=body, verify = False, headers=headers, cookies=cookies, timeout=10)
result = json.loads(r.content.decode('utf-8'))

