# -*- coding:UTF-8 -*-
# @Author  : huangfang

from app.actions.tools import BaseApplication
from app.actions.tools import InterfaceKeyword
import json
from views.productOrder.Order_params.Menpiao_Order_params import Menpiao_Order_params
from flask import Blueprint

#设置蓝图
menpiao = Blueprint('menpiao', __name__)
@menpiao.route('/menpiao')

def getmenpiao():
    try:
        url = 'http://public-api.bj.pga.tuniu-sit.org/pga-web/nws/order/add'
        menpiaopara = Menpiao_Order_params()

        params = menpiaopara.Menpiao_Order_params()
        resp_dict = Menpiao_Create_Order(url, params)
        CheckResponse = Menpiao_CheckResponse(resp_dict)
        orderId = Menpiao_GET_orderId(CheckResponse)
        menpiao_orderId = {'orderId': orderId}
        response = ({"success": "true", "msg": "OK", "data": {"menpiao_orderId": menpiao_orderId}})
        print("response is", response)
    except Exception as e:
        raise e
        response = ({"success": "false", "msg": "操作失败～～"})
    response = json.dumps(response)
    return response

def Menpiao_Create_Order(url,params):


        headers = {"Content-Type": "application/json"}

        params=json.loads(params)

        p=InterfaceKeyword.InterfaceKeyword().Put(url,params,headers)

        return p


def Menpiao_CheckResponse(rsp):

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


def Menpiao_GET_orderId(params):
        if params:
            orderId = params['data'][0]['orderId']
            return orderId
        else:
            print("返回结果为空")
            return False





#if __name__ == '__main__':
    #menpiao = Menpiao_Order()
    # gentuanpara = GenTuan_Order_params_gentuandabao()
    # url='http://public-api.bj.pga.tuniu-sit.org/pga-web/nws/order/add'

    # params = gentuanpara.GenTuan_Order_params_gentuandabao()

    # resp_dict = gentuan.GenTuan_Create_Order_dabao(url,params)
    # print 'resp_dict==',resp_dict

    # CheckResponse = gentuan.GenTuan_CheckResponse(resp_dict)
    # print 'CheckResponse==',CheckResponse

    # orderId = gentuan.GenTuan_GET_orderId(CheckResponse)
    # print 'orderId==',orderId'''

    #print (menpiao.Create_Order_ID_menpiao())



