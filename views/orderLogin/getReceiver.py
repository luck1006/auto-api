# -*- coding: utf-8 -*-
# TIME:         8.24
# Author:       huanfang
# Explain：     获取发邮件的接受者


import datetime
from jira import JIRA
import json
from app.models.models import *
from flask import Blueprint,request
from flask import Flask

#蓝图，注册到app
getReceiver = Blueprint('getReceiver', __name__,)

#路由，具体业务接口
@getReceiver.route('/getReceiver')
def getgetReceiver():
    try:
        receiver_name = []
        result=db.session.query(Receiver.receiver_name).all()
        #print(result)
        for i in range(len(result)):
            data = {
                "receiver_name": result[i][0]
            }
            receiver_name.append(data)
        response = ({"success": "true", "msg": "OK", "data": {"receiver_name": receiver_name}})
        #print(response)

    except Exception as e:
        raise e
        response = {"success": "false", "msg": "查询失败~~"}
    response = json.dumps(response, ensure_ascii=False)
    return response


