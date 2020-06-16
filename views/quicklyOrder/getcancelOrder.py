# /usr/bin/python
# -*- coding:utf-8 -*-
"""
# project:autoapi
# user:: liju
@author: liju
@time: 2019-9-30 13:36
"""

# 注册蓝图
import base64

import requests
from flask import Blueprint, request

from views.interfaceAuto.interface import cors_response

CancelOrder = Blueprint('CancelOrder', __name__, url_prefix="")



class getcancelOrder:
    def __init__(self, orderId=None, env=None):
        self.__orderId = orderId
        self.__responsedata = None

    # 运行用例接口(不做任何入库操作也并不做任何校验，只是单纯的调用接口)

    def runcase(self, orderId):
        self.pData = {
            "uid": "26683",
            "token": '',
            "nickname": "李菊",
            "r": 0.7413435727922948,
            "cancelType0": "5",
            "cancelType1": "502",
            "cancelType2": "50201",
            "cancelReason": "111",
            "repeatOrder": "",
            "intentionTime": "",
            "intention": "",
            "canceledName": "",
            "canceledTime": "",
            "isFreewill": 1,
            "cancelType": "50201",
            "repeatFlag": 0,
            "cancelTypeDetail": "系统测试订单",
            "orderId": orderId
        }
        fullUrl = "http://public-api.tof.tuniu.org/tof/manage/order/cancel?"
        self.session = requests.session()
        resp = self.session.post(fullUrl, json=self.pData)
        self.__status_code = resp.status_code
        if resp.status_code == 500 or resp.status_code == 404:
            self.__responsedata = "执行失败,返回" + str(resp.status_code)
        else:
            self.__responsedata = base64.b64decode(resp.text).decode()
        print(' --> ' + self.__responsedata)
        return self.__responsedata

@CancelOrder.route('/CancelOrder', methods=['GET', 'POST'])
def runpebble():
    vp = getcancelOrder()
    orderId = request.get_json().get('orderId')
    print('orderId is:  ' + orderId )
    try:
        response = vp.runcase(orderId)
        resp = response
    except:
        resp = cors_response({"success": False, "data": None})
    print("返回给客户端的Json是" + str(resp))
    return resp



# if __name__ == "__main__":
#     vp = getcancelOrder()
#     vp.runcase(1223117392)
