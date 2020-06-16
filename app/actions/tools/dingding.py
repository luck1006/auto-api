# -*- coding: UTF-8 -*-
# https://open-doc.dingtalk.com/microapp/serverapi2/qf2nxq 钉钉机器人文档
import requests
import json

true = True
false = False
null = None


def dd(message, url):
    '''
    dingding发送
    :return:
    '''
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }
    payload = json.dumps(message, ensure_ascii=False)
    print(payload)
    try:
        response = requests.post(url, headers=headers, data=payload.encode('utf-8'))
        print(response.text)
        if response.json()['errmsg'] == 'ok':
            print('钉钉发送成功')
        else:
            print('钉钉发送异常')
    except BaseException as e:
        print(e)