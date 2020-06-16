#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import base64
import json
from app.actions.tools.BaseCommon import BaseCommon

class BaseInterface(BaseCommon):
    # def __init__(self):
    #     self.loggers = self.logger().getLogger(__name__)

    # loggers = BaseCommon().logger().getLogger(__name__)
    #
    #param
    #@url:http:www.tuniu.com
    #@params
    #@headers:{"Content-Type":"application/json"}
    #retrun
    #@r.status_code:HTTP状态码
    #@r.url:请求的URL
    #@r.headers:获取Headers
    #@r.text:响应内容
    #
    def get(self,url,params,headers):
        try:
            #self.loggers.debug("type:get,"+"params:"+params+"headers:"+str(headers))
            # return requests.request("get", url, params=params,headers=headers)
            return requests.get(url, params=params,headers=headers)
        except BaseException as e:
            print (e)

    def post(self,url,params,headers):
        try:
            self.loggers.debug("type:post," + "params:" + str(params) + "headers:" + str(headers))
            return requests.post(url,data=params,headers=headers)
            # return requests.request("post", url, params=params,headers=headers)
        except BaseException as e:
            print (e)

    def put(self,url,params,headers):
        try:
            #self.loggers.debug("type:put," + "params:" + str(params) + "headers:" + str(headers))
            return requests.put(url,data=params,headers=headers)
            # return requests.request("put", url, params=params,headers=headers)
        except BaseException as e:
            print (e)

    def pebblepost1(self,url,params,headers):
        try:
            self.loggers.debug("~~~~~params:" + params + "headers:" + headers)
            return requests.session().post(url, data=json.dumps(params).decode("utf-8"),headers=headers)
        except BaseException as e:
            print (e)
    def pebblepost(self,url,params,headers):
        r = requests.session().post(url, data=json.dumps(params).decode("utf-8"), headers=headers)
        self.loggers.debug("params:" + str(params) + "headers:" + str(headers))
        return r

    #功能:解密
    #作者:tangmingyuan
    #时间:2018.02.13
    def base64Decode(self,s):
        try:
            #self.loggers.debug(s)
            return base64.b64decode(s)
        except BaseException as e:
            print (e)

    #功能:加密
    #作者:tangmingyuan
    #时间:2018.02.13
    def base64Encode(self,s):
        try:
            #self.loggers.debug(s)
            ss=s.encode("utf-8")
            return base64.b64encode(ss)
        except BaseException as e:
            print (e)

    def dumps(self,s):
        return json.dumps(s)

    def loads(self,s):
        return json.loads(s)

    def length(self,lst):
        return len(lst)

    def readFile(self,path):
        try:
            f = open(path, 'r')
            return f.read()
        finally:
            if f:
                f.close()