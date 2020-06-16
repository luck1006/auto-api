# encode=utf-8
import requests
from app.actions.tools import timer

week_day = timer.time_l()[4]


def send_dingding(excel_url):
    url = "https://oapi.dingtalk.com/robot/send"
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }


    # 质量组
    querystring={"access_token": "ef382a6a71def285fc424dc0b562bfb76fbd64c713eae709105ad9c347694ab2"}
    #测试群组
    querystring_test = {"access_token": "3f6ae6212f523ab593fa0eb749e119a47781a5f580ed0108598eb22a7d766ae4"}

    payload = '''{"msgtype":"link","at":{"atMobiles":[],"isAtAll":true},"link":{"text":"上周五到本周四工时报表","title":"线上BU每周工时报表","picUrl":"","messageUrl":"excel_url"}}'''.replace(
        'excel_url', excel_url)
    print(payload)


    # 发送到钉钉群
    response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers, params=querystring)

    print(response.url, response.text, '钉钉发送成功')
