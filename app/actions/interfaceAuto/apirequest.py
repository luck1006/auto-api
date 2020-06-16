# coding:utf-8
import requests
import json
from app.actions.interfaceAuto.GetParmsValue import GetParmsValue
from collections import OrderedDict
import ast
import logging
from app.actions.interfaceAuto.interface_tsp import *

from urllib import parse
from app.actions.interfaceAuto.interface_tsp import *

requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False

class Interface:
    #1，get 类型接口请求
    def getinterfaceone(self, rest, data, env, headers, dParam='', isBase64Encode=False, isBase64Decode=False):
        getparmsvalue = GetParmsValue()
        rest= getparmsvalue.get_parms_value(rest, env)
        #dff: 20190628 对d参数进行处理
        param = {}
        if dParam is not None and dParam != '':
            dParam = getparmsvalue.get_parms_value(dParam, env)
            param['d'] = dParam
            # dff: 20190628 将请求d参数编码
            encodeParam = parse.urlencode(param)
            rest = rest +'&'+ encodeParam

        try:
            if (data != '' and data != None):
                data = getparmsvalue.get_parms_value(data, env)
                #20190727-dff；增加入参base64编码处理
                if isBase64Encode:
                    data = base64Encode(data)

                if (headers != ''):
                    if ('{{' in headers):
                        headers = getparmsvalue.get_parms_value(headers, env)
                    headers = eval(headers)

                r = requests.get(rest, headers=headers, params=data)
                try:
                    r = json.loads(r.text, object_pairs_hook=OrderedDict)
                    z = json.dumps(r, ensure_ascii=False)
                except:
                    z=r.text
            else:
                if (headers != ''):
                    headers = eval(headers)
                r = requests.get(rest, headers=headers)
                try:
                    r = json.loads(r.text, object_pairs_hook=OrderedDict)
                    z = json.dumps(r, ensure_ascii=False)
                except:
                    z=r.text
            # dff-20191009: 对出参需要base64解码进行处理
            if isBase64Decode:
                z = base64Decode(z)
        except Exception as e:
            print(e)
            logging.info(e)
            z = '调用的get 请求方法异常'
        return z
    #2，post类型接口请求
    def postinterfaceone(self, rest, data, env, headers, dParam='', isBase64Encode=False, isBase64Decode=False):
        getparmsvalue = GetParmsValue()
        rest = getparmsvalue.get_parms_value(rest, env)

        #dff: 20190628 对d参数进行处理
        param = {}
        if dParam is not None and dParam != '':
            dParam = getparmsvalue.get_parms_value(dParam, env)
            param['d'] = dParam
            # dff: 20190628 将请求d参数编码
            encodeParam = parse.urlencode(param)
            rest = rest +'&'+ encodeParam

        try:
            if (data != '' and data != None):
                data = getparmsvalue.get_parms_value(data, env)
                #20190727-dff；增加入参base64蓄电池处理
                if isBase64Encode:
                    data = base64Encode(data)
                if (headers != ''):
                    if ('{{' in headers):
                        headers = getparmsvalue.get_parms_value(headers, env)
                    headers = ast.literal_eval(headers)
                r = requests.post(rest, data=data.encode('utf-8'), headers=headers)
                try:
                    #按照接口返回数据返回，不进行重新排序
                    r = json.loads(r.text, object_pairs_hook=OrderedDict)
                    z = json.dumps(r, ensure_ascii=False)
                except:
                    z=r.text
            else:
                if (headers != ''):
                    # headers = eval(headers)
                    headers = json.loads(headers)
                r = requests.post(rest, headers=headers)
                try:
                    r = json.loads(r.text, object_pairs_hook=OrderedDict)
                    z = json.dumps(r, ensure_ascii=False)
                except:
                    z=r.text
            # print(rest,data,z)

            # dff-20191009: 对出参需要base64解码进行处理
            if isBase64Decode:
                z = base64Decode(z)
        except Exception as e:
            logging.info(e)
            print(e)
            z='调用的post 请求方法异常'
        return z
    #3，put类型接口请求
    def putinterfaceone(self, rest, data, env, headers, dParam='', isBase64Encode=False, isBase64Decode=False):
        getparmsvalue = GetParmsValue()
        rest = getparmsvalue.get_parms_value(rest, env)

        #dff: 20190628 对d参数进行处理
        param = {}
        if dParam is not None and dParam != '':
            dParam = getparmsvalue.get_parms_value(dParam, env)
            param['d'] = dParam
            # dff: 20190628 将请求d参数编码
            encodeParam = parse.urlencode(param)
            rest = rest +'&'+ encodeParam

        try:
            if (data != '' and data != None):
                data = getparmsvalue.get_parms_value(data, env)
                #20190727-dff；增加入参base64蓄电池处理
                if isBase64Encode:
                    data = base64Encode(data)
                if (headers != ''):
                    if ('{{' in headers):
                        headers = getparmsvalue.get_parms_value(headers, env)
                    headers = ast.literal_eval(headers)
                r = requests.put(rest, data=data.encode('utf-8'), headers=headers)
                try:
                    #按照接口返回数据返回，不进行重新排序
                    r = json.loads(r.text, object_pairs_hook=OrderedDict)
                    z = json.dumps(r, ensure_ascii=False)
                except:
                    z=r.text
            else:
                if (headers != ''):
                    # headers = eval(headers)
                    headers = json.loads(headers)
                r = requests.put(rest, headers=headers)
                try:
                    r = json.loads(r.text, object_pairs_hook=OrderedDict)
                    z = json.dumps(r, ensure_ascii=False)
                except:
                    z=r.text
            # print(rest,data,z)

            # dff-20191009: 对出参需要base64解码进行处理
            if isBase64Decode:
                z = base64Decode(z)
        except Exception as e:
            logging.info(e)
            print(e)
            z='调用的put 请求方法异常'
        return z


# if __name__ == '__main__':
#     i=Interface()
#     s=i.getinterfaceone('http://mall-booking.api.tuniu-sit.org/booking/book/getBookingBaseInfo?{"productId": 301444081,"packageId": 1268047,"departDate":"","destDate":"","departCityCode":0,"adultNum":1,"childNum":0,"roomNum":1,"hasCustomAttr": 1,"travellerList": []}','',
#                       'sit',"{'x-authen-user':'71656257'}")
#
#     # print(s)
