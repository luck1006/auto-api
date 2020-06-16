# -*- coding: utf-8 -*-
# TIME:         上午11:21
# Author:       xutaolin
import requests
import json
from app.actions.interfaceAuto.GetParmsValue import GetParmsValue
from collections import OrderedDict
import ast
import datetime
from urllib import parse

requests.adapters.DEFAULT_RETRIES = 10
s = requests.session()
s.keep_alive = False


class batchRequest:

    def getinterfaceone(self, rest, data, env, headers, dParam=''):
        getparmsvalue = GetParmsValue()
        rest = getparmsvalue.get_parms_value(rest, env)
        success=True

        #dff: 20190701 对d参数进行处理
        param = {}
        if dParam is not None and dParam != '':
            dParam = getparmsvalue.get_parms_value(dParam, env)
            param['d'] = dParam
            # dff: 20190701 将请求d参数编码
            encodeParam = parse.urlencode(param)
            rest = rest +'&'+ encodeParam

        try:
            if (data != '' and data != None):
                data = getparmsvalue.get_parms_value(data, env)

                if (headers != ''):
                    if ('{{' in headers):
                        headers = getparmsvalue.get_parms_value(headers, env)
                    headers = eval(headers)
                r = requests.get(rest, headers=headers, params=data.encode('utf-8'))
                #接口运行时间
                time = r.elapsed.microseconds/1000
                try:
                    r = json.loads(r.text, object_pairs_hook=OrderedDict);
                    z = json.dumps(r, ensure_ascii=False)
                except:
                    z=r.text
            else:
                if (headers != ''):
                    headers = eval(headers)
                r = requests.get(rest, headers=headers)
                # 接口运行时间
                time = r.elapsed.microseconds/1000
                try:
                    r = json.loads(r.text, object_pairs_hook=OrderedDict)
                    z = json.dumps(r, ensure_ascii=False)
                except:
                    z=r.text
        except Exception as e:
            print(e)
            z = '调用的get 请求方法异常'
            time=0
            success = False

        #返回dict（接口返回值以及接口运行时间）
        response={}
        response['res']=z
        response['time']=time
        response['success']=success
        return response

    def postinterfaceone(self, rest, data, env, headers, dParam=''):
        getparmsvalue = GetParmsValue()
        rest = getparmsvalue.get_parms_value(rest, env)
        success=True
        #dff: 20190701 对d参数进行处理
        param = {}
        if dParam is not None and dParam != '':
            dParam = getparmsvalue.get_parms_value(dParam, env)
            param['d'] = dParam

            # dff: 20190701 将请求d参数编码
            encodeParam = parse.urlencode(param)
            rest = rest +'&'+ encodeParam

        try:
            if (data != '' and data != None):
                data = getparmsvalue.get_parms_value(data, env)
                if (headers != ''):
                    if ('{{' in headers):
                        headers = getparmsvalue.get_parms_value(headers, env)
                    headers = ast.literal_eval(headers)

                # r = requests.post(rest, data=data_json, headers=headers)
                r = requests.post(rest, data=data.encode('utf-8'), headers=headers)
                # 接口运行时间
                time = r.elapsed.microseconds/1000
                try:
                    #按照接口返回数据返回，不进行重新排序
                    r = json.loads(r.text, object_pairs_hook=OrderedDict)
                    z = json.dumps(r, ensure_ascii=False)
                except:
                    z=r
            else:
                if (headers != ''):
                    # headers = eval(headers)
                    headers = json.loads(headers)

                r = requests.post(rest, headers=headers)
                # 接口运行时间
                time = r.elapsed.microseconds/1000

                try:
                    r = json.loads(r.text, object_pairs_hook=OrderedDict)
                    z = json.dumps(r, ensure_ascii=False)
                except:
                    z=r
        except Exception as e:
            print(e)
            z = '调用的post 请求方法异常'
            time=0

        # 返回dict（接口返回值以及接口运行时间）
        response = {}
        response['res'] = z
        response['time'] = time
        response['success'] = success
        return response
#
if __name__ == '__main__':
    i=batchRequest()
    s=i.getinterfaceone('http://mall-booking.api.tuniu-sit.org1/booking/book/getBookingBaseInfo?{"productId": 301444081,"packageId": 1268047,"departDate":"","destDate":"","departCityCode":0,"adultNum":1,"childNum":0,"roomNum":1,"hasCustomAttr": 1,"travellerList": []}','',
                      'sit',"{'x-authen-user':'71656257'}")

    print(s)
