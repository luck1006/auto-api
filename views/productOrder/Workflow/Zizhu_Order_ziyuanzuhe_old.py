# -*- coding:UTF-8 -*-
# @Author  : huangfang

from app.actions.tools import BaseApplication
from app.actions.tools import InterfaceKeyword
import json
from views.productOrder.Order_params.Zizhu_Order_params_zizhuziyuanzuhe import Zizhu_Order_params_zizhuziyuanzuhe
from app.models.models import *
from flask import Blueprint
#设置蓝图


# @BaseApplication.container
class Zizhu_Order_ziyuanzuhe(BaseApplication.BaseApplication):

    def Zizhu_Create_Order_ziyuanzuhe(self,url,params):

        headers = {"Content-Type": "application/json"}

        params=json.loads(params)

        p=InterfaceKeyword.InterfaceKeyword().Put(url,params,headers)

        return p


    def Zizhu_CheckResponse(self,rsp):
        #print type(rsp),rsp
        #print rsp['text'],rsp['code']CheckResponse
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


    def Zizhu_GET_orderId(self,params):
        if params:
            orderId = params['data'][0]['orderId']
            return orderId
        else:
            print("返回结果为空")
            return False

    def Create_Order_ID_zizhu_ziyuanzuhe(self):
        try:
            zizhu = Zizhu_Order_ziyuanzuhe()
            url = 'http://public-api.bj.pga.tuniu-sit.org/pga-web/nws/order/add'
            zizhupara = Zizhu_Order_params_zizhuziyuanzuhe()

            params = zizhupara.Zizhu_Order_params_zizhuziyuanzuhe()
            resp_dict = self.Zizhu_Create_Order_ziyuanzuhe(url, params)
            CheckResponse = self.Zizhu_CheckResponse(resp_dict)
            orderId = self.Zizhu_GET_orderId(CheckResponse)
            ziyuanzuhe_orderId = {'orderId': orderId}
            response = ({"success": "true", "msg": "OK", "data": {"ziyuanzuhe_orderId": ziyuanzuhe_orderId}})
        except Exception as e:
            raise e
            response = ({"success": "false", "msg": "操作失败～～"})

        return response




if __name__ == '__main__':
    zizhu = Zizhu_Order_ziyuanzuhe()
    # zizhupara = Zizhu_Order_params_zizhudabao()
    # url='http://public-api.bj.pga.tuniu-sit.org/pga-web/nws/order/add'

    # params = zizhupara.Zizhu_Order_params_zizhudabao()

    # resp_dict = zizhu.Zizhu_Create_Order_dabao(url,params)
    # print 'resp_dict==',resp_dict

    # CheckResponse = zizhu.Zizhu_CheckResponse(resp_dict)
    # print 'CheckResponse==',CheckResponse

    # orderId = zizhu.Zizhu_GET_orderId(CheckResponse)
    # print 'orderId==',orderId'''

    print (zizhu.Create_Order_ID_zizhu_ziyuanzuhe())



