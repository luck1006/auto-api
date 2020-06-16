# -*- coding:UTF-8 -*-
# @Author  : huangfang

from app.actions.tools import BaseApplication
from app.actions.tools import InterfaceKeyword
import json
from views.productOrder.Order_params.Zizhu_Order_params_zizhutrain import Zizhu_Order_params_zizhutrain
from app.models.models import *
from flask import Blueprint

#设置蓝图
zizhu_train = Blueprint('zizhu_train', __name__)
@zizhu_train.route('/zizhu_train')

def getzizhu_train():
    try:
        url = 'http://public-api.bj.pga.tuniu-sit.org/pga-web/nws/order/add'
        zizhupara = Zizhu_Order_params_zizhutrain()
        params = zizhupara.Zizhu_Order_params_zizhutrain()
        resp_dict =Zizhu_Create_Order_train(url, params)
        CheckResponse =Zizhu_CheckResponse(resp_dict)
        orderId = Zizhu_GET_orderId(CheckResponse)
        train_orderId = {'orderId': orderId}
        response = ({"success": "true", "msg": "OK", "data": {"train_orderId": train_orderId}})
        print("response is", response)
    except Exception as e:
        raise e
        response = ({"success": "false", "msg": "操作失败～～"})
    response = json.dumps(response)
    return response


def Zizhu_Create_Order_train(url,params):

        headers = {"Content-Type": "application/json"}

        params=json.loads(params)

        p=InterfaceKeyword.InterfaceKeyword().Put(url,params,headers)

        return p


def Zizhu_CheckResponse(rsp):
        if rsp is not None:
            #print(rsp['text'])
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


def Zizhu_GET_orderId(params):
        if params:
            orderId = params['data'][0]['orderId']
            return orderId
        else:
            print("返回结果为空")
            return False





#if __name__ == '__main__':
   # zizhu = Zizhu_Order_train()
    # zizhupara = Zizhu_Order_params_zizhudabao()
    # url='http://public-api.bj.pga.tuniu-sit.org/pga-web/nws/order/add'

    # params = zizhupara.Zizhu_Order_params_zizhudabao()

    # resp_dict = zizhu.Zizhu_Create_Order_dabao(url,params)
    # print 'resp_dict==',resp_dict

    # CheckResponse = zizhu.Zizhu_CheckResponse(resp_dict)
    # print 'CheckResponse==',CheckResponse

    # orderId = zizhu.Zizhu_GET_orderId(CheckResponse)
    # print 'orderId==',orderId'''

    #print (zizhu.Create_Order_ID_zizhu_train())



