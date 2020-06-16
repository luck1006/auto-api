# -*- coding:UTF-8 -*-
import sys
import os
import requests
import json
sys.path.append(os.path.dirname(__file__) + os.sep + '..'+ os.sep ) ## “ '..'+ os.sep ” => 向上一层
## os.path.dirname(__file__) 上一级目录
from app.actions.tools.BaseApplication import BaseApplication
from app.actions.tools import interface_pebble
from app.actions.tools.CommonKeyword import CommonKeyword
import base64


pebble = interface_pebble #初始化pebble接口方法
baseA=BaseApplication()

class interface_boh(BaseApplication):
    #通用base64GET接口
    def base64getinterface(self,url,params):
        # 接口地址
        url1 = url
        # 接口入参
        params1 = params

        aa =  self.base64Get(url1,params1,"")
        #self.comparestr(json.loads(aa['code']),200)
        return aa

    # 查询产品团期资源接口-boss3
    # BOH.NM.ProductController.getDetailResources
    def getDetailResources(self,productId,requestSourceCode,departDate,clientType,channelRelationId,cacheFlag):
        # 接口地址
        url = "http://pis-bohprice-pjbsst.api.tuniu-sst.org/boh/product/detail/resources"
        # 接口入参
        default  = {
                "productId": 210034683,
                "marketChannelCode": 0,
                "requestSourceCode": 3,
                "departDate": "2018-04-10",
                "clientType": "10002",
                "channelRelationId": "010000000000",
                "cacheFlag": "false"}
        default['productId']=productId
        default['requestSourceCode']=requestSourceCode
        default['departDate']=departDate
        default['clientType']=clientType
        default['channelRelationId']=channelRelationId
        default['cacheFlag']=cacheFlag

        return self.base64Get(url, default, "")

    #查询产品基本信息接口-boss3
    #BOH.NM.ProductDomainController.getPrdBasicInfo
    def getPrdBasicInfo(self,productId):
        #接口地址
        url = "http://pis-bohall-pjbsst.api.tuniu-sst.org/boh/cache/product/basic/info/query"
        #接口入参
        params={
            "productId":productId
        }
        return self.base64Get(url,params,"")
        #调用接口成功
        self.comparestr(str(json.loads(ss['text'])['success']), "True")

#ss = interface_boh().getDetailResources()

#print str(json.loads(ss)['success'])
#baseA.comparestr(str(json.loads(ss)['success']),"True")


