import requests
import json, time
import datetime
import smtplib
import sys, re
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from views.wangyi import WangYi
from flask import Blueprint
from flask import request
from flask import g, jsonify
from app.actions.tools.sendEmail import send_email
from app.actions.tools.shortUrl.shortUrl import short_url

# 接口文档 https://dev.yunxin.163.com/docs/product/%E7%82%B9%E6%92%AD/%E6%9C%8D%E5%8A%A1%E7%AB%AFAPI%E6%96%87%E6%A1%A3?pos=toc-4

wangyi = Blueprint('wangyi', __name__, url_prefix="/wangyi")
# 短链参数用于统计
tag = 'pndora-video'


@wangyi.before_request
def before():
    wy = WangYi()
    setattr(g, 'wy', wy)


@wangyi.route('/app/vod/type/list', methods=['POST'])
def wy_query_file_list(*args):
    try:
        # 优先取方法入参 其次取url中参数
        data = json.dumps(args[0])
    except Exception as e:
        data = request.get_data()
    path = '/app/vod/type/list'
    # data = {"currentPage": 1, "pageSize": 100}
    # print(data)
    res = requests.post(g.wy.host + path, data=data, headers=g.wy.headers)
    # print(res.text)
    data = res.json()['ret']['list']
    a = []
    for i in data:
        # 104296769 sprint验收视频文件夹
        if i['parentTypeId'] == 104296769:
            a.append(i)
    requestId = res.json()['requestId']
    code = res.json()['code']
    response = {"requestId": requestId, "code": code, "data": a[::-1]}
    return json.dumps(response)


@wangyi.route('/app/vod/video/list', methods=['POST'])
def wy_query_video_list(*args):
    try:
        data = json.dumps(args[0])
    except:
        data = request.get_data()

    # data = {"currentPage": 1, "pageSize": 1, "status": 0, "type": 104326805}
    path = '/app/vod/video/list'
    res = requests.post(g.wy.host + path, data=data, headers=g.wy.headers)
    resp = json.loads(res.text)
    for i in resp['ret']['list']:
        try:
            i['shdMp4Url'] = short_url(i['shdMp4Url'], tag)
        except:
            i['origUrl'] = short_url(i['origUrl'], tag)
    return json.dumps(resp)


@wangyi.route('/ddForHour', methods=['POST'])
def sprint_vedio_hour_ding():
    '''
    每小时发送新增
    :return:
    '''
    now = int(time.time() * 1000)
    p = {"currentPage": 1, "pageSize": 100, "status": 0, "type": video_new_type()}
    res = requests.post(url='https://vcloud.163.com/app/vod/video/list', data=json.dumps(p), headers=g.wy.headers)
    res = json.loads(res.text)
    data = res['ret']['list']
    l = []
    text = ''
    for i in data:
        # 取代码执行时间1小时内视频 漏发可以改下面的时间
        if now - i['createTime'] <= 60 * 60 * 1000:
            l.append(i)
    if l != []:
        for i in l:
            videoName = i['videoName'].replace('_', '\_')
            try:
                # 优先取mp4地址 否则取原地址
                origUrl = short_url(i['shdMp4Url'], tag)
            except:
                origUrl = short_url(i['origUrl'], tag)
            text += f'- [{videoName}]({origUrl})  \n'
        content = {
            "msgtype": "markdown",
            "markdown": {
                "title": "新增Sprint验收视频",
                "text": '#### 新增Sprint验收视频,  \n' + text
            },
            "at": {
                "isAtAll": True
            }
        }
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
        xtcpyfbu = 'https://oapi.dingtalk.com/robot/send?access_token=e92b55cb2a7e9c90bb579a507d80057b5e1ae891412a947e167efa6c4d6be63f'
        dalao = 'https://oapi.dingtalk.com/robot/send?access_token=1d5ade2c149c4991726ab5c9cbc6ddc99d727690805d3ec5c7bca995397fe3a6'
        test = 'https://oapi.dingtalk.com/robot/send?access_token=a8d9fb85b4b3ddaef60b7a3b634c683a80e6f839b726db10bbd2c408a639d7dc'
        for url in [xtcpyfbu, dalao]:
            # for url in [test]:
            requests.post(url=url, headers=headers, data=json.dumps(content).encode('utf-8'))
        return 'OK'
    else:
        return 'no'


def video_new_type():
    '''
    获取最新文件夹
    :return:
    '''
    data = {"currentPage": 1, "pageSize": 100}
    r = wy_query_file_list(data)
    typeId = json.loads(r)['data'][0]['typeId']
    return str(typeId)


@wangyi.route('/video/email', methods=['POST'])
def sprint_video_email():
    week = datetime.datetime.now().isocalendar()
    dan_shuang_zhou = week[1] % 2
    # 迭代第二周发送
    if dan_shuang_zhou == 0:
        para = {"currentPage": 1, "pageSize": 200, "status": 0, "type": video_new_type()}
        res = wy_query_video_list(para)
        data = json.loads(res)
        tds = ''
        dic = {}
        try:
            if data['ret']['totalRecords'] > 0:
                for d in data['ret']['list']:
                    videoName = d['videoName']
                    try:
                        # 优先取mp4地址 否则取原地址
                        origUrl = short_url(d['shdMp4Url'], tag)
                    except:
                        origUrl = short_url(d['origUrl'], tag)
                    team = re.split('-|_', videoName)[0].lower()
                    try:
                        dic[team].append({"videoName": videoName, "origUrl": origUrl})
                    except Exception as e:
                        dic[team] = []
                        dic[team].append({"videoName": videoName, "origUrl": origUrl})

                for k, v in dic.items():
                    tds = tds + f'''<tr><td><h3><br>{k}</h3></td></tr>'''
                    for data in v:
                        td = f'''<tr><td><a href="{data['origUrl']}">{data['videoName']}<br></a></td></tr>'''
                        tds += td
                to_addr = 'g-grouprd@tuniu.com'
                cc = 'kongqiushi@tuniu.com,tanghaitao@tuniu.com,guqining@tuniu.com,shenhaiming@tuniu.com,wutao@tuniu.com'
                m = f'''Dear  all：<br><br>  本迭代Sprint Demo 结束，详见下方视频内容 <br> <html><head></head><body><table ><tbody>{tds}</tbody></table></body></html>'''
                # send_email_exchange(to_addr, subject='本迭代验收视频汇总', message=m)
                send_email(to_addr, cc=cc, subject='本迭代验收视频汇总', message=m)
                return 'ok'
        except Exception as e:
            print(e)
        return 'Exception'
    else:
        return 'false'
