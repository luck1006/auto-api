# -*- coding: utf-8 -*-
import requests,sys
import json
from urllib import parse
import logging


""" 
@version: v1.0 
@author: monleylu
@time: 2018/2/24 10:11 
"""


class InterfaceBase:
    def __init__(self, urlData, cParam=None, dParam=None, params=None, pData=None,dataParams=None, session=None):
        self.__urlData = urlData
        self.__cParam = cParam
        self.__dParam = dParam
        self.__params = params
        self.__pData = pData
        self.__dataParams = dataParams
        self.__session = session
        # 存储接口响应结果
        self.__responsedata = None

    def sendrequest(self,env, **kwargs):
        """获取命令行数据"""
        # ParameterHandle.action(sys.argv)
        # 处理请求url
        self.env = env
        if isinstance(self.__urlData["domain"], str):
            logging.info("domain is still string type")
            url = "{protocol}://{domain}/{path}?".format(protocol=self.__urlData["protocol"],
                                                         domain=self.__urlData["domain"][env],
                                                         path=self.__urlData["path"])
        else:
            logging.info("domain is new type,dict type")
            url = "{protocol}://{domain}/{path}?".format(protocol=self.__urlData["protocol"],
                                                         domain=self.__urlData["domain"][env],#.split('-')[2]
                                                         path=self.__urlData["path"])
            # print('****', 'prd')
            print(url)
        # 请求方式
        method = self.__urlData["method"].upper()

        # 处理请求session
        if not self.session:
            logging.error("session为空，重新初始化一个http请求session（这不一定是错误，可能是需要使用新的连接发送请求特地设置）")
            self.session = requests.session()

        # 组织请求参数
        param = {}
        if not self.cParam is None:
            param["c"] = json.dumps(self.cParam, separators=(',', ':'))

        if not self.dParam is None:
            param["d"] = json.dumps(self.dParam, separators=(',', ':'))

        if not self.dataParams is None:
            param["dataparams"] = json.dumps(self.dataParams, separators=(',', ':'))

        # 将请求参数编码
        encodeParam = parse.urlencode(param)

        # 组织全部请求路径
        fullUrl = url + encodeParam
        # logging.info(fullUrl)

        # 当传递pdata数据时，以post方式发生
        data = self.pData

        if "GET" == method:
            resp = self.__session.get(fullUrl, params=self.params, **kwargs)
            self.__status_code = resp.status_code
            print(self.__status_code)
            if resp.status_code == 500 or resp.status_code == 404:
                self.__responsedata = resp.text
            else:
                try:
                    self.__responsedata = resp.json()
                except Exception as e:
                    logging.error("返回的原始结果json解码失败，可能并不是异常，而是响应就不是json格式的")
                    self.__responsedata = resp.text
        elif "POST" == method:

            try:
                # 如果data是dict格式，就判断是否是json格式
                if isinstance(data, dict):
                    json.loads(json.dumps(data))
                    resp = self.__session.post(fullUrl, json=data, **kwargs)
                #如果data不是dict格式，就直接以str方式传入
                else:
                    resp = self.__session.post(fullUrl, data=data, **kwargs)
            except Exception as e:
                resp = self.__session.post(fullUrl, data=data, **kwargs)

            self.__status_code = resp.status_code
            logging.debug("post data:" + json.dumps(data))
            if resp.status_code == 500 or resp.status_code == 404:
                self.__responsedata = resp.text
            elif resp.status_code == 504:
                self.__responsedata = resp.text
                logging.error("接口返回504")
            else:
                try:
                    self.__responsedata = resp.json()
                except Exception as e:
                    logging.error("返回的原始结果json解码失败，可能并不是异常，而是响应就不是json格式的")
                    self.__responsedata = resp.text

        logging.info("request url:" + resp.url)
        logging.debug("respone data:" + json.dumps(self.__responsedata,ensure_ascii=False))
        return self.__responsedata

    @property
    def urlData(self):
        return self.__urlData

    @property
    def cParam(self):
        return self.__cParam

    @cParam.setter
    def cParam(self, value):
        self.__cParam = value

    @property
    def dParam(self):
        return self.__dParam

    @dParam.setter
    def dParam(self, value):
        self.__dParam = value

    @property
    def params(self):
        return self.__params

    @params.setter
    def params(self, value):
        self.__params = value

    @property
    def pData(self):
        return self.__pData

    @pData.setter
    def pData(self, value):
        self.__pData = value

    @property
    def dataParams(self):
        return self.__dataParams

    @dataParams.setter
    def dataParams(self, value):
        self.__dataParams = value

    @property
    def session(self):
        return self.__session

    @session.setter
    def session(self, value):
        self.__session = value

    @property
    def responsedata(self):
        return self.__responsedata

    @responsedata.setter
    def responsedata(self, value):
        self.__responsedata = value
