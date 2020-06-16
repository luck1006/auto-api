# -*- coding:UTF-8 -*-
# @Author  : huangfang

from app.actions.tools import BaseApplication
from app.actions.tools import InterfaceKeyword
import json
from views.productOrder.Order_params.Zijia_Order_params import Zijia_Order_params
from flask import Blueprint

#设置蓝图
zijia = Blueprint('zijia', __name__)
@zijia.route('/zijia')

def getzijia():
    try:
        url = 'http://public-api.bj.pga.tuniu-sit.org/pga-web/nws/order/add'
        zijiapara = Zijia_Order_params()

        params = zijiapara.Zijia_Order_params()
        resp_dict = Zijia_Create_Order(url, params)
        CheckResponse = Zijia_CheckResponse(resp_dict)
        orderId = Zijia_GET_orderId(CheckResponse)
        zijia_orderId = {'orderId': orderId}
        response = ({"success": "true", "msg": "OK", "data": {"zijia_orderId": zijia_orderId}})
        print("response is", response)
    except Exception as e:
        raise e
        response = ({"success": "false", "msg": "操作失败～～"})
    response = json.dumps(response)
    return response


def Zijia_Create_Order(url,params):


        headers = {"Content-Type": "application/json"}

        params=json.loads(params)

        p=InterfaceKeyword.InterfaceKeyword().Put(url,params,headers)

        return p


def Zijia_CheckResponse(rsp):
        if rsp is not None:
            print(rsp['text'])
            if rsp['code']==200:
                text_base64Decode = InterfaceKeyword.InterfaceKeyword().base64Decode(rsp['text'])
                print ("text_base64Decode==",text_base64Decode)
                text = json.loads(text_base64Decode)
                if text["success"] == False:
                    print("返回失败，code为" + str(text["errorCode"]))
                    return False
                else:
                    return text
            else:
                print("返回状态"+rsp.status_code)
                return False

        else:
            print("返回结果为空")


def Zijia_GET_orderId(params):
        if params:
            orderId = params['data'][0]['orderId']
            return orderId
        else:
            print("返回结果为空")
            return False





#if __name__ == '__main__':
#    zijia = Zijia_Order()
#    zijiapara = Zijia_Order_params()
#    url='http://public-api.bj.pga.tuniu-sit.org/pga-web/nws/order/add'
#
#    params = zijiapara.Zijia_Order_params()
#
#    resp_dict = zijia.Zijia_Create_Order(url,params)
#    print ('resp_dict==',resp_dict)
#
#    # CheckResponse = zizhu.Zizhu_CheckResponse(resp_dict)
#    # print 'CheckResponse==',CheckResponse
#
#    # orderId = zizhu.Zizhu_GET_orderId(CheckResponse)
#    # print 'orderId==',orderId'''
#
#    print (zijia.Create_Order_ID_zijia())



