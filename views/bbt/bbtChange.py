from app.models.models import *
from flask import Blueprint, current_app, request, flash
import json
import requests
import time
from sqlalchemy import func, and_, desc
import logging
bbt = Blueprint('bbt', __name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

@bbt.route('/bbtChange', methods=['GET', 'POST'])
def getbbtChange():
    content = request.get_json()
    dd = []
    if content != None:
        a = json.dumps(content)
        logging.info(a)
        project = f"{content['repository']['project']['key']}-{content['repository']['name']}"
        branch = content['refChanges'][0]['refId']
        for changesets in content['changesets']['values']:
            name = changesets['toCommit']['author']['name']
            fromCommit = changesets['fromCommit']['displayId']
            toCommit = changesets['toCommit']['displayId']
            Message = changesets['toCommit']['message'].replace('* ', '\* ').replace('- ', '\- ')
            for value in changesets['changes']['values']:
                path = value['links']['self'][0]['href'].split('#')[0]
            d = {"name": name, "fromCommit": fromCommit, "toCommit": toCommit, "Message": Message, "path": path }
            db.session.add(bbt_change(project=project,
                                      name=name, branch=branch, from_commit=fromCommit, message=Message, to_commit=toCommit, url=path
                                      ))

            db.session.commit()
            dd.append(d)
        tt = ''
        for d in dd:
            for k, v in d.items():
                if k != 'path':
                    t = '- ' + k + '：  ' + v + '\n'
                    tt += t
                else:
                    tt = tt + f'- [查看详情]({d["path"]})\n ___________\n'
        text = f"**代码提交记录** \n - project: {project}  \n - branch: {branch}  \n ______\n  {tt}  \n"
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": "代码提交记录",
                "text": text
            },
            "at": {
                "atMobiles": ["17625905367"],
                "isAtAll": False
            }
        }
        url = "https://oapi.dingtalk.com/robot/send"
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
        querystring_test = {"access_token": "4795cedafc5db638429d58b92b9bb13f7664127a39d341655a7038752f7a6e15"}
        response = requests.post(url, data=json.dumps(payload).encode('utf-8'), headers=headers,
                                 params=querystring_test)
        return response.text

    return '!!!不要随便调哈!!!'
