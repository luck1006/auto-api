#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding = utf-8


import requests
import base64
import json
import sys,os
import importlib
importlib.reload(sys)
import base64


sys.path.append( '..'+ os.sep ) ## “ '..'+ os.sep ” => 向上一层
#sys.setdefaultencoding('utf-8')
from app.actions.tools.BaseInterface import BaseInterface

class InterfaceKeyword(BaseInterface):


    def base64Get(self,url,params,headers):
        params=self.base64Encode(json.dumps(params))
        #print("params is",type(params))

        #params=base64.b64encode(params).decode()
        params=params.decode("utf-8")
        r=self.get(url,params,headers)

        if r is not None:
            p={
                "code":str(r.status_code),
                "text":self.base64Decode((r.text))
            }

            if r.status_code == 200:
                print("请求成功，返回参数：" + str(p["text"]))
            else:
                print("请求成功，返回参数：" + str(p["text"]))
            return p
        else:
            p = {
                "code": str(r.status_code),
                "text": str(r)
            }
            return p

    def base64Get2(self,url,params):
        p=self.base64Get(url,params,"")
        return p

    def base64Get3(self,url,params,headers=""):
        p=self.base64Get(url,params,headers)
        return p

    def Get(self,url,params,headers):
        print("请求地址："+str(url))
        print("入参："+str(params).decode('unicode-escape'))
        if(type(params)!=str):
            params=json.dumps(params).decode('unicode-escape')
        r=self.get(url,params,headers)
        #requests.request("get", url, params=params,headers=headers)
        p={
            "code":str(r.status_code),
            "text":str(r.text)
        }

        if r.status_code == 200:
            print("请求成功，返回参数:"+self.base64Decode(r.text))
        else:
            print("请求失败，"+str(p))
        return p

    def base64Post(self,url,params,headers):
        print( "请求地址：" + str(url))
        print( "入参：" + json.dumps(params).decode('unicode-escape'))
        params=self.base64Encode(json.dumps(params).decode('unicode-escape'))
        r=self.post(url,params,headers)
        p={
            "code":str(r.status_code),
            "text":self.base64Decode(r.text)
        }
        if r.status_code == 200:
            print( "请求成功,返回参数:"+self.base64Decode(r.text))
        else:
            print( "请求失败，"+str(p))
        return p

    def base64Post2(self,url,params):
        p=self.base64Post(url,params,"")
        return p

    def base64Post3(self,url,params,headers=""):
        p=self.base64Post(url,params,headers)
        return p

    def Post(self,url,params,headers):
        print( "请求地址：" + str(url))
        print( "入参：" + str(params))
        params=str(json.dumps(params))

        r=self.post(url,params,headers)
        p={
            "code":str(r.status_code),
            "text":str(r.text)
        }
        if r.status_code == 200:
            print( "请求成功,返回参数:"+str(r.text))
        else:
            print( "请求失败，"+str(p))
        return p

    def Put(self,url,params,headers):
        print( "请求地址：" + str(url))
        print( "入参：" + str(params))
        params=str(json.dumps(params))

        r=self.put(url,params,headers)
        p={
            "code":r.status_code,
            "text":str(r.text)
        }

        if r.status_code == 200:
            print( "请求成功,返回参数:"+str(r.text))
        else:
            print( "请求失败，"+str(p))
        return p

    def pebblePost(self,url,params,headers):
        print("请求地址：" + str(url))
        print("入参：" + str(params))
        #params=json.dumps(params).decode("utf-8")

        r=self.pebblepost(url,params,headers)
        if r.status_code == 200:
            print("请求成功，返回参数："+str(r.text))
        else:
            print("请求失败，"+str(r))
        return r

    def config(self,path):
        File=self.readFile(path).split("\n")
        json={}
        for config in File:
            if(config!=""):
                t=config.split("=")
                json[t[0]]=t[1]
        return json

#i = InterfaceKeyword()
#i.base64Get("http://www.baidu.com","","")
