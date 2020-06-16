# /usr/bin/python
# -*- coding:utf-8 -*-
"""
# project:autoapi
# user:: liju
@author: liju
@time: 2019-7-1 17:15
"""
import json
import logging

import requests


class findInternalInterface:
    def __init__(self, urlData=None, env=None):
        self.__urlData = urlData
        self.__env = env
        # 存储接口响应结果
        self.__responsedata = None

    def composeUrlforget(self, urlData, env):
        if isinstance(urlData, str):
            logging.info("domain is still string type")
        else:
            logging.info("domain is new type,dict type")
        url = str(urlData)
        """先用冒号把http或者https切割出来,切割结果返回至list"""
        firstlist = url.split(':')
        # print(firstlist)
        secondlist = str(firstlist[1]).split('/')
        # print(secondlist)
        lenurl = len(secondlist)
        i = 4
        secondpart = ''
        while i < lenurl:
            secondpart = secondpart + str(secondlist[i]) + (str('/'))
            print(str(secondlist))
            i = i + 1
        if env == 'prd':
            newUrl = 'http' + ':' + '//' + '10.41.7.160' + str('/') + str(secondlist[3]) + str('/') + 'debug' + str(
                '/') + secondpart + secondlist[lenurl - 1] + '&noCache=true'
        elif env == 'pre':
            newUrl = 'http' + ':' + '//' + '10.40.143.198' + str('/') + str(secondlist[3]) + str('/') + 'debug' + str(
                '/') + secondpart + secondlist[lenurl - 1] + '&noCache=true'
        elif env == 'sit':
            newUrl = 'http' + ':' + '//' + '10.28.67.234' + str('/') + str(secondlist[3]) + str('/') + 'debug' + str(
                '/') + secondpart + secondlist[lenurl - 1] + '&noCache=true'
        else:
            logging.debug('请输入正确的URL')
        print(newUrl)
        return newUrl

    def composeUrlforpost(self, urlData, env, postparams):
        url = str(urlData)
        if isinstance(postparams, dict):
            try:
                pparams = json.dumps(postparams)
            except ValueError:
                logging.info("post参数不是json格式字符串")
        else:
            logging.info("post参数请输入json格式字符串参数")

        """先用冒号把http或者https切割出来,切割结果返回至list"""
        firstlist = url.split(':')
        # print(firstlist)
        secondlist = str(firstlist[1]).split('?')
        thirdlist = str(secondlist[0]).split('/')
        print(thirdlist)
        lenurl = len(thirdlist)
        """从/切割的第5个开始加入，前2个是空格，第3个替换成域名，第4个后面固定加debug"""
        i = 4
        secondpart = ''
        while i < lenurl:
            secondpart = secondpart + str(thirdlist[i]) + (str('/'))
            # print(str(secondpart))
            i = i + 1
        if env == 'prd':
            newUrl = 'http' + ':' + '//' + '10.41.7.160' + str('/') + str(thirdlist[3]) + str('/') + 'debug' + str(
                '/') + secondpart + '?' + pparams + '&noCache=true'
        elif env == 'pre':
            newUrl = 'http' + ':' + '//' + '10.40.143.198' + str('/') + str(thirdlist[3]) + str('/') + 'debug' + str(
                '/') + secondpart + '?' + pparams + '&noCache=true'
        elif env == 'sit':
            newUrl = 'http' + ':' + '//' + '10.28.67.234' + str('/') + str(thirdlist[3]) + str('/') + 'debug' + str(
                '/') + secondpart + '?' + pparams + '&noCache=true'
        else:
            logging.debug('请输入正确的环境')
        print(newUrl)
        return newUrl

    def sendrequest(self, fullUrl):
        self.session = requests.session()
        resp = self.session.get(fullUrl)
        self.__status_code = resp.status_code
        if resp.status_code == 500 or resp.status_code == 404:
            self.__responsedata = resp.text
        else:
            try:
                self.__responsedata = resp.json()
            except Exception as e:
                logging.error("返回的原始结果json解码失败，可能并不是异常，而是响应就不是json格式的")
                self.__responsedata = resp.text
        print(json.dumps(self.__responsedata, ensure_ascii=False))
        logging.info("request url:" + resp.url)
        logging.debug("respone data:" + json.dumps(self.__responsedata, ensure_ascii=False))
        return self.__responsedata


if __name__ == "__main__":
    # url = "https://api.tuniu.com/res/pack/getDefaultRecommend/app?d=%7B%22packType%22%3A%222%22%2C%22bookCityCode%22%3A1602%2C%22bookCityName%22%3A%22%E5%8D%97%E4%BA%AC%22%2C%22departCityCode%22%3A0%2C%22departCityName%22%3A%22%22%2C%22departDate%22%3A%222019-07-29%22%2C%22adultNum%22%3A2%2C%22childNum%22%3A0%2C%22isInternational%22%3A0%2C%22journeyType%22%3A2%2C%22journeyList%22%3A%5B%7B%22cabinType%22%3A1%2C%22startCityCode%22%3A0%2C%22startCityName%22%3A%22%22%2C%22destCityCode%22%3A200%2C%22destCityName%22%3A%22%E5%8C%97%E4%BA%AC%22%2C%22journeyDepartDate%22%3A%222019-07-29%22%2C%22journeyEndDate%22%3A%222019-07-31%22%7D%5D%2C%22sessionId%22%3A%2254cd52119c2a8ee71225315da472ff6f_%22%7D&c=%7B%22cc%22%3A1602%2C%22ct%22%3A20%2C%22dt%22%3A1%2C%22ov%22%3A20%2C%22p%22%3A19326%2C%22v%22%3A%2210.11.0%22%7D"
    # vp = findInternalInterface()
    # fullUrl = vp.composeUrlforget(url, 'prd')
    # vp.sendrequest(fullUrl)

    posturl = "https://api.tuniu.com/res/pack/saveInternalHotel/app?c=%7B%22cc%22%3A1602%2C%22ct%22%3A20%2C%22dt%22%3A1%2C%22ov%22%3A20%2C%22p%22%3A19326%2C%22v%22%3A%2210.11.0%22%7D"
    param = {
        "hotel": {
            "hotelId": 711527,
            "checkIn": "2019-07-29",
            "checkOut": "2019-07-31",
            "adultNum": "2",
            "childNum": "0",
            "vendorId": 23690,
            "vendorRatePlanId": "304979059",
            "roomNum": 1,
            "roomId": 222126105
        },
        "packType": "2",
        "sessionId": "54cd52119c2a8ee71225315da472ff6f_",
        "operateType": "2",
        "replaceHotelUniqueFlag": "hotel|711527|true|222126105|0|23690|9401106|2019-07-29|2019-07-31|2|0"
    }
    vp = findInternalInterface()
    fullUrl = vp.composeUrlforpost(posturl, 'prd', param)
    vp.sendrequest(fullUrl)
