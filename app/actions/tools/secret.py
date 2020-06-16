#  -*-  coding: utf-8  -*-
from Crypto.Cipher import AES

from binascii import b2a_hex, a2b_hex


def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


# 加密函数
def encrypt(text):
    key = 'passwordpassword'.encode('utf-8')
    mode = AES.MODE_CBC
    text = add_to_16(text)
    cryptos = AES.new(key, mode, iv=key)
    cipher_text = cryptos.encrypt(text)
    # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
    return b2a_hex(cipher_text)


# 解密后，去掉补足的空格用strip() 去掉
def decrypt(text):
    key = 'passwordpassword'.encode('utf-8')
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv=key)
    plain_text = cryptos.decrypt(a2b_hex(text))
    return plain_text.decode().rstrip('\0')

if __name__ == '__main__':

    e = encrypt("sunchuanxin").decode()  # 加密
    d = decrypt(e)  # 解密
    print("加密:", e)
    print("解密:", d)