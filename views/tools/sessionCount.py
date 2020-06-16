# -*- coding: utf-8 -*-

import requests
import json
import socket
from . import tool
from flask import jsonify

hostname = socket.gethostname()


@tool.route('/sessionCount', methods=['GET'])
def sesscount():
    url = 'http://10.40.191.78:10213/message/manager/node/status'
    if 'local' not in hostname:
        d = requests.get(url)
    else:
        proxies = {'http': 'http://sunchuanxin:tuniu@qwer1@o2p-proxy.tuniu.org:8080'}
        d = requests.get(url, proxies=proxies)
    resp = json.loads(d.text)
    res = resp['data']
    count = 0
    text = ''
    for i in res:
        num = res[i]['sessionCount']
        count += num
        txt = res[i]['hostname'] + ':' + str(num) + '\n'
        text += txt
    total = count
    resp['data']['total'] = total
    with open('./views/tools/tmp.txt', 'r+') as f:
        n = f.read()
        if total > int(n):
            f.seek(0)
            f.write(str(total))

            content = {
                "msgtype": "text",
                "text": {
                    "content": f"sessionCount峰值:{total}\n {text} "
                },
                "at": {
                    "atMobiles": [

                    ]
                }
            }
            headers = {
                'Content-Type': "application/json",
                'cache-control': "no-cache"
            }
            requests.post(
                url="https://oapi.dingtalk.com/robot/send?access_token=a8d9fb85b4b3ddaef60b7a3b634c683a80e6f839b726db10bbd2c408a639d7dc",
                headers=headers, data=json.dumps(content).encode('utf-8'))
    return jsonify(resp)
