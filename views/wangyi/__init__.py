from hashlib import sha1
import time


class WangYi(object):
    def __init__(self):
        self.AppKey = '9acdb1730b8ae5bc753b380addd61920'
        self.AppSecret = '406a6b66dd58'
        self.Nonce = 'tuniu520'
        self.CurTime = str(int(time.time()))
        self.host = 'https://vcloud.163.com'
        pwd = self.AppSecret + self.Nonce + self.CurTime
        s1 = sha1()
        s1.update(pwd.encode())
        CheckSum = s1.hexdigest()
        self.CheckSum = CheckSum
        self.headers = {
            'AppKey': self.AppKey,
            'Nonce': self.Nonce,
            'CurTime': self.CurTime,
            'CheckSum': self.CheckSum,
            'cache-control': "no-cache",
            'Content-Type': 'application/json;charset=utf-8'
        }