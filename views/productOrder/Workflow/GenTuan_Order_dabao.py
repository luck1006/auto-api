# -*- coding:UTF-8 -*-
# @Author  : huangfang

from app.actions.tools import BaseApplication
from app.actions.tools import InterfaceKeyword
import json
from views.productOrder.Order_params.GenTuan_Order_params_gentuandabao import GenTuan_Order_params_gentuandabao
from flask import Blueprint

#设置蓝图
gentuan_dabao = Blueprint('gentuan_dabao', __name__)
@gentuan_dabao.route('/gentuan_dabao')

def getgentuan_dabao():
    try:
        url = 'http://public-api.bj.pga.tuniu-sit.org/pga-web/nws/order/add'
        gentuanpara = GenTuan_Order_params_gentuandabao()

        params = gentuanpara.GenTuan_Order_params_gentuandabao()
        resp_dict = GenTuan_Create_Order_dabao(url, params)
        CheckResponse = GenTuan_CheckResponse(resp_dict)
        orderId = GenTuan_GET_orderId(CheckResponse)
        dabao_orderId = {'orderId': orderId}
        response = ({"success": "true", "msg": "OK", "data": {"dabao_orderId": dabao_orderId}})
        print("response is", response)
    except Exception as e:
        raise e
        response = ({"success": "false", "msg": "操作失败～～"})
    response = json.dumps(response)
    return response

def GenTuan_Create_Order_dabao(url,params):

        headers = {"Content-Type": "application/json"}

        params=json.loads(params)

        p=InterfaceKeyword.InterfaceKeyword().Put(url,params,headers)

        return p


def GenTuan_CheckResponse(rsp):

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


def GenTuan_GET_orderId(params):
        if params:
            orderId = params['data'][0]['orderId']
            return orderId
        else:
            print("返回结果为空")
            return False





#if __name__ == '__main__':
    #gentuan = GenTuan_Order_dabao()
    # gentuanpara = GenTuan_Order_params_gentuandabao()
    # url='http://public-api.bj.pga.tuniu-sit.org/pga-web/nws/order/add'

    # params = gentuanpara.GenTuan_Order_params_gentuandabao()

    # resp_dict = gentuan.GenTuan_Create_Order_dabao(url,params)
    # print 'resp_dict==',resp_dict

    # CheckResponse = gentuan.GenTuan_CheckResponse(resp_dict)
    # print 'CheckResponse==',CheckResponse

    # orderId = gentuan.GenTuan_GET_orderId(CheckResponse)
    # print 'orderId==',orderId'''

    #print (gentuan.Create_Order_ID_dabao())



