# -*- coding:UTF-8 -*-
# coding = utf-8
#获取跟团产品的行程信息
import sys
import os
import json
import jsonpath
import base64

import random
import pymysql
sys.path.append(os.path.dirname(__file__) + os.sep + '..'+ os.sep + '..'+ os.sep) ## “ '..'+ os.sep ” => 向上一层
## os.path.dirname(__file__) 上一级目录
from app.actions.tools import interface_boh
import datetime
from app.actions.tools.commonData import productdata_gentuan
from app.actions.tools.CommonKeyword import CommonKeyword

#@BaseApplication.container
class Gentuan_BOH_train(interface_boh.interface_boh):

    #资源接口 BOH.NM.ProductController.getDetailResources
    def getDetailResources(self):

        #设置团期维当前时间+10天，查询产品资源信息
        startDate = (datetime.datetime.now()+datetime.timedelta(days=10)).strftime("%Y-%m-%d")
        productId = productdata_gentuan["productId_train"]
        #boh查询资源接口
        #跟团火车票+地接：210017619
        url = "http://pis-bohprice.api.tuniu-sit.org/boh/product/detail/resources"
        params  = {
            "productId": productId,
            "marketChannelCode": 100,
            "requestSourceCode": 2,
            "departDate": startDate,
            "clientType": "10002",
            "channelRelationId": "010000000000",
            "cacheFlag": "false"}
        print ("资源接口请求入参为",params)
        ss = self.base64getinterface(url,params)
        print ("资源接口返回结果为",ss)
        #self.comparestr(str(json.loads(ss['text'])['success']), "True")


        #获取行程id
        journeyId1 = str(jsonpath.jsonpath(json.loads(ss['text']), '$.data.rows[0].id')[0])
        journeyId2 = str(jsonpath.jsonpath(json.loads(ss['text']), '$.data.rows[1].id')[0])

        #获取行程资源id
        resId1=str(jsonpath.jsonpath(json.loads(ss['text']), '$.data.rows[1].journeyResources[1].resId')[0])
        resType=str(jsonpath.jsonpath(json.loads(ss['text']), '$.data.rows[1].journeyResources[1].resType')[0])
        resSubType=str(jsonpath.jsonpath(json.loads(ss['text']), '$.data.rows[1].journeyResources[1].resSubType')[0])

        #获取火车票资源id
        resId1_train=str(jsonpath.jsonpath(json.loads(ss['text']), '$.data.rows[0].journeyResources[0].resId')[0])
        resId2_train=str(jsonpath.jsonpath(json.loads(ss['text']), '$.data.rows[0].journeyResources[1].resId')[0])
        res1_train_type=str(jsonpath.jsonpath(json.loads(ss['text']), '$.data.rows[0].journeyResources[0].resType')[0])
        res2_train_type=str(jsonpath.jsonpath(json.loads(ss['text']), '$.data.rows[0].journeyResources[1].resType')[0])




        #将参数组装成字典
        rsp_dict = dict(journeyId1=journeyId1, journeyId2=journeyId2,resId1=resId1,resType=resType,resSubType=resSubType,resId1_train=resId1_train,resId2_train=resId2_train,res1_train_type=res1_train_type,res2_train_type=res2_train_type)
        return rsp_dict


if __name__ == '__main__':

    genp = Gentuan_BOH_train()
    params=genp.getDetailResources()
    #params2=genp.getDetail()
    print (params)













