# /usr/bin/python
# -*- coding:utf-8 -*-
"""
# project:autoapi
# user:: liju
@author: liju
@time: 2019-7-3 10:29
"""

import json
import logging
from urllib import parse

import requests
from flask import Blueprint
from flask import request, make_response

# 注册蓝图
from views.interfaceAuto.interface import cors_response

FindInternalInterface = Blueprint('FindInternalInterface', __name__, url_prefix="")


class findInternalInterface:
    def __init__(self, urlData=None, env=None):
        self.__urlData = urlData
        self.__env = env
        self.__responsedata = None

    ### 调用Tadis系统获取所有应用的生产IP
    def getIps(self):
        # 预先设置需要用到IP的系统
        applicationlist = ['mob-portal-prd', 'mob-portal-pre', 'mob-res-pre', 'mob-res-pro', 'mob-tour-pre',
                           'mob-tour-production']
        # Tardis Url
        url = "https://tardis.tuniu.io/systems/apis/containers?"
        # 定义list用来存放系统跟IP键值
        applicationIp = []
        Ips = {}
        # 组织入参
        for i in range(0, len(applicationlist)):
            param = {"code": applicationlist[i]}
            # 将请求参数编码
            encodeParam = parse.urlencode(param)
            # # 组织全部请求路径
            fullUrl = url + encodeParam
            # 请求接口获取返
            s = requests.session()
            resp = s.get(fullUrl)
            status_code = resp.status_code
            if status_code == 500 or status_code == 404:
                responsedata = resp.text
            else:
                try:
                    responsedata = resp.json()
                except Exception as e:
                    logging.error("返回的原始结果json解码失败，响应就不是json格式的")
                    responsedata = resp.text
            if not responsedata is None:
                Ips = {applicationlist[i]: responsedata['data'][0]['ip']}
                applicationIp.append(Ips)
            i = i + 1
        print(applicationIp)
        return applicationIp

    def getIpsbyCode(self, code):
        # Tardis Url
        url = "https://tardis.tuniu.io/systems/apis/containers?"
        # 定义list用来存放系统跟IP键值
        applicationIp = []
        Ips = {}
        # 组织入参
        param = {"code": code}
        # 将请求参数编码
        encodeParam = parse.urlencode(param)
        # # 组织全部请求路径
        fullUrl = url + encodeParam
        # 请求接口获取返
        s = requests.session()
        resp = s.get(fullUrl)
        status_code = resp.status_code
        print("status_code   " + str(status_code))
        if status_code == 500 or status_code == 404:
            logging.error("通过应用名称获取IP接口500或者404")
        else:
            try:
                responsedata = resp.json()
                if responsedata['success'] == True:
                    return responsedata['data'][0]['ip']
                else:
                    logging.error("指定TAG不存在或已删除,请重新选择应用名称")
            except Exception as e:
                logging.error("返回的原始结果json解码失败，响应就不是json格式的")

    def getIpbyUrl(self, urlData, env):
        url = str(urlData)
        """先用冒号把http或者https切割出来,切割结果返回至list"""
        firstlist = url.split(':')
        # print("getIpbyUrl firstlist is " + firstlist)
        secondlist = str(firstlist[1]).split('?')
        # print("getIpbyUrl firstlist is "+ secondlist)
        thirdlist = str(secondlist[0]).split('/')
        # print("getIpbyUrl firstlist is " +thirdlist)
        application = thirdlist[3]
        producttionname = []
        # 给env做个转化，因为有的应用取的名字是prd，有的是production
        Tpaddress = []
        if str(env) == 'prd':
            applicationname1 = "mob-" + str(application) + "-" + 'prd'
            producttionname.append(applicationname1)
            applicationname2 = "mob-" + str(application) + "-" + 'production'
            producttionname.append(applicationname2)
            applicationname3 = "mob-" + str(application) + "-" + 'pro'
            producttionname.append(applicationname3)
        else:
            applicationname3 = "mob-" + str(application) + "-" + 'pre'
            producttionname.append(applicationname3)
        for i in range(0, len(producttionname)):
            Ip = self.getIpsbyCode(producttionname[i])
            if not Ip is None:
                # print("oooooooooooooo  " +Ip)
                return Ip

    def composeUrl(self, urlData, env, postparams=None):
        url = str(urlData)
        # 通过输入的url 和 env 获取应用服务对应的Ip地址
        Ip = str(self.getIpbyUrl(urlData, env))
        # postparams有值则走post请求
        if not postparams is None and postparams != '':
            print("有post参数 走post切割url方法")
            if isinstance(postparams, str):
                postparams = json.loads(postparams)
            if isinstance(postparams, dict):
                try:
                    pparams = json.dumps(postparams,separators=(',', ':'))
                except ValueError:
                    logging.info("post参数不是json格式字符串")
            else:
                logging.info("post参数请输入json格式字符串参数")

            """先用冒号把http或者https切割出来,切割结果返回至list"""
            param = {}
            param["d"] = pparams
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
            newUrl = 'http' + ':' + '//' + Ip + str('/') + str(thirdlist[3]) + str('/') + 'debug' + str(
                '/') + secondpart + '?' +secondlist[1]+'&'+ parse.urlencode(param) + '&noCache=true'
            print("测试 1111  post的切割是否正确"  + "   切割的C参是secondlist[1]:" + str(secondlist[1])  + "   切割的d参是parse.urlencode(param): "  + str(parse.urlencode(param)))
        else:
            print("没有post参数 走get切割url方法")
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
                newUrl = 'http' + ':' + '//' + Ip + str('/') + str(secondlist[3]) + str('/') + 'debug' + str(
                    '/') + secondpart + secondlist[lenurl - 1] + '&noCache=true'
        print("newUrl is : " + newUrl)
        return newUrl

    def sendrequest(self, urlData, env, postparams=None):
        newUrl = self.composeUrl(urlData, env, postparams)
        self.session = requests.session()
        resp = self.session.get(newUrl)
        self.__status_code = resp.status_code
        if resp.status_code == 500 or resp.status_code == 404:
            self.__responsedata = resp.text
        else:
            try:
                self.__responsedata = resp.json()
            except Exception as e:
                logging.error("返回的原始结果json解码失败，可能并不是异常，而是响应就不是json格式的")
                self.__responsedata = resp.text
        logging.info("request url:" + resp.url)
        logging.debug("respone data:" + json.dumps(self.__responsedata, ensure_ascii=False))
        print(json.dumps(self.__responsedata))
        # print(json.dumps(self.__responsedata, indent=1))
        return self.__responsedata

    def getInternalInterfaceList(self, responsedata):
        """由于内部debug返回的responsedata中的个别key名字太长无法引用，重新组装dict，将key更换成pebblei的格式"""
        InternalPebbleList = []
        InternalTspList = []
        PebbleDict = {}
        TspDict = {}
        if isinstance(responsedata, dict):
            # responsedata = json.loads(json.dumps(responsedata))
            # responsedata = responsedata
            if responsedata != "":
                if not responsedata['requestLogs'] is None:
                    if not responsedata['requestLogs']['dependentPebbles'] is None:
                        dependentPebbles = responsedata['requestLogs']['dependentPebbles']
                        for values in dependentPebbles.values():
                            InternalPebbleList.append(values)
                        for i in range(0, len(InternalPebbleList)):
                            PebbleDict.update({"Pebble" + str(i): InternalPebbleList[i]})

                    if not responsedata['requestLogs']['dependentTsps'] is None:
                        """目前还没有找到调用BOH接口采用TSP方式的"""
                        dependentTsps = responsedata['requestLogs']['dependentTsps']
                        for values in dependentTsps.values():
                            InternalTspList.append(values)
                        for i in range(0, len(InternalTspList)):
                            TspDict.update({"Tsp" + str(i): InternalTspList[i]})
            else:
                return None
            if len(InternalPebbleList) == 0 and len(InternalTspList) == 0:
                """代表没有调用内部接口"""
                logging.info("没有查到有内部接口调用")
                return None
            else:
                print("PebbleList is:   " + str(PebbleDict) + "TspList is:   " + str(TspDict))
            return PebbleDict, TspDict

# 运行用例接口(不做任何入库操作也并不做任何校验，只是单纯的调用接口)
@FindInternalInterface.route('/FindPebble', methods=['GET', 'POST'])
def runpebble():
    # url = "https://api.tuniu.com/res/pack/saveInternalHotel/app?c=%7B%22cc%22%3A1602%2C%22ct%22%3A20%2C%22dt%22%3A1%2C%22ov%22%3A20%2C%22p%22%3A19326%2C%22v%22%3A%2210.11.0%22%7D"
    #     # param = {
    #     #     "hotel": {
    #     #         "hotelId": 711527,
    #     #         "checkIn": "2019-08-10",
    #     #         "checkOut": "2019-08-11",
    #     #         "adultNum": "2",
    #     #         "childNum": "0",
    #     #         "vendorId": 23690,
    #     #         "vendorRatePlanId": "304979059",
    #     #         "roomNum": 1,
    #     #         "roomId": 222126105
    #     #     },
    #     #     "packType": "2",
    #     #     "sessionId": "54cd52119c2a8ee71225315da472ff6f_",
    #     #     "operateType": "2",
    #     #     "replaceHotelUniqueFlag": "hotel|711527|true|222126105|0|23690|9401106|2019-07-29|2019-07-31|2|0"
    #     # }
    # url = "https://api.tuniu.com/portal/home/list/v3?c=%7B%22cc%22%3A1602%2C%22ct%22%3A10%2C%22p%22%3A14588%2C%22ov%22%3A20%2C%22dt%22%3A0%2C%22v%22%3A%2210.12.0%22%7D&d=%7B%22pageLimit%22%3A10%2C%22bottomOffset%22%3A-1%2C%22currentPage%22%3A1%2C%22needPlay%22%3Atrue%2C%22width%22%3A750%2C%22deviceNum%22%3A%22c6777549d3dca9d907271ee6ac3d189df00fdb49%22%2C%22getRecommendFlag%22%3Afalse%2C%22moduleName%22%3A%22%E5%85%A8%E9%83%A8%22%2C%22moduleId%22%3A%2215539527%22%2C%22abTest%22%3A%22bi%22%2C%22sessionId%22%3A%228aa78300422a479677185ec2119c52eb_%22%2C%22uniqueKey%22%3A%229EA881B7-E104-412A-BD96-5B57413B75B3%22%2C%22isFirst%22%3Atrue%7D"
    vp = findInternalInterface()
    url = request.get_json().get('url')
    env = request.get_json().get('env')
    postparams = request.get_json().get('postparams')
    print('url is ' + url + "env is: " + env + " postparans is " + postparams)
    try:
        resp = vp.sendrequest(url, env, postparams)
        response = vp.getInternalInterfaceList(resp)
        resp =cors_response({"success": True, "pebble": response[0], "tsp": response[1]})
    except:
        resp = cors_response({"success": False, "data": None})
    print("返回给客户端的Json是" + str(resp))
    return resp


# @FindInternalInterface.route('/FindTsp', methods=['GET', 'POST'])
# def runTsp():
#     url = "https://api.tuniu.com/res/pack/saveInternalHotel/app?c=%7B%22cc%22%3A1602%2C%22ct%22%3A20%2C%22dt%22%3A1" \
#           "%2C%22ov%22%3A20%2C%22p%22%3A19326%2C%22v%22%3A%2210.11.0%22%7D "
#     param = {
#         "hotel": {
#             "hotelId": 711527,
#             "checkIn": "2019-08-10",
#             "checkOut": "2019-08-11",
#             "adultNum": "2",
#             "childNum": "0",
#             "vendorId": 23690,
#             "vendorRatePlanId": "304979059",
#             "roomNum": 1,
#             "roomId": 222126105
#         },
#         "packType": "2",
#         "sessionId": "54cd52119c2a8ee71225315da472ff6f_",
#         "operateType": "2",
#         "replaceHotelUniqueFlag": "hotel|711527|true|222126105|0|23690|9401106|2019-07-29|2019-07-31|2|0"
#     }
#     vp = findInternalInterface()
#     resp = vp.sendrequest(url, 'prd', param)
#     Tsp = vp.getInternalInterfaceList(resp)[1]
#     return Tsp


# if __name__ == "__main__":
#     vp = findInternalInterface()
#     # url1 = "https://api.tuniu.com/res/pack/getDefaultRecommend/app?d=%7B%22packType%22%3A%222%22%2C%22bookCityCode%22%3A1602%2C%22bookCityName%22%3A%22%E5%8D%97%E4%BA%AC%22%2C%22departCityCode%22%3A0%2C%22departCityName%22%3A%22%22%2C%22departDate%22%3A%222019-07-29%22%2C%22adultNum%22%3A2%2C%22childNum%22%3A0%2C%22isInternational%22%3A0%2C%22journeyType%22%3A2%2C%22journeyList%22%3A%5B%7B%22cabinType%22%3A1%2C%22startCityCode%22%3A0%2C%22startCityName%22%3A%22%22%2C%22destCityCode%22%3A200%2C%22destCityName%22%3A%22%E5%8C%97%E4%BA%AC%22%2C%22journeyDepartDate%22%3A%222019-07-29%22%2C%22journeyEndDate%22%3A%222019-07-31%22%7D%5D%2C%22sessionId%22%3A%2254cd52119c2a8ee71225315da472ff6f_%22%7D&c=%7B%22cc%22%3A1602%2C%22ct%22%3A20%2C%22dt%22%3A1%2C%22ov%22%3A20%2C%22p%22%3A19326%2C%22v%22%3A%2210.11.0%22%7D"
#     # # url3 = "https://api.tuniu.com/res/pack/getDefaultRecommend/app?d=%7B%22packType%22%3A%222%22%2C%22bookCityCode%22%3A1602%2C%22bookCityName%22%3A%22%E5%8D%97%E4%BA%AC%22%2C%22departCityCode%22%3A0%2C%22departCityName%22%3A%22%22%2C%22departDate%22%3A%222019-08-01%22%2C%22adultNum%22%3A2%2C%22childNum%22%3A0%2C%22isInternational%22%3A0%2C%22journeyType%22%3A2%2C%22journeyList%22%3A%5B%7B%22cabinType%22%3A1%2C%22startCityCode%22%3A0%2C%22startCityName%22%3A%22%22%2C%22destCityCode%22%3A200%2C%22destCityName%22%3A%22%E5%8C%97%E4%BA%AC%22%2C%22journeyDepartDate%22%3A%222019-08-01%22%2C%22journeyEndDate%22%3A%222019-08-03%22%7D%5D%2C%22sessionId%22%3A%2254b60a2f3b45e7cc657de6a800e07b36_%22%7D&c=%7B%22cc%22%3A1602%2C%22ct%22%3A20%2C%22dt%22%3A1%2C%22ov%22%3A20%2C%22p%22%3A11210%2C%22v%22%3A%2210.11.0%22%7D"
#     # url4 = "https://api.tuniu.com/portal/home/list/v3?c=%7B%22cc%22%3A1602%2C%22ct%22%3A10%2C%22p%22%3A14588%2C%22ov%22%3A20%2C%22dt%22%3A0%2C%22v%22%3A%2210.12.0%22%7D&d=%7B%22pageLimit%22%3A10%2C%22bottomOffset%22%3A-1%2C%22currentPage%22%3A1%2C%22needPlay%22%3Atrue%2C%22width%22%3A750%2C%22deviceNum%22%3A%22c6777549d3dca9d907271ee6ac3d189df00fdb49%22%2C%22getRecommendFlag%22%3Afalse%2C%22moduleName%22%3A%22%E5%85%A8%E9%83%A8%22%2C%22moduleId%22%3A%2215539527%22%2C%22abTest%22%3A%22bi%22%2C%22sessionId%22%3A%228aa78300422a479677185ec2119c52eb_%22%2C%22uniqueKey%22%3A%229EA881B7-E104-412A-BD96-5B57413B75B3%22%2C%22isFirst%22%3Atrue%7D"
#     # param ={"hotel":{"hotelId":711527,"checkIn":"2019-08-10","checkOut": "2019-08-11","adultNum":"2","childNum":"0","vendorId":23690,"vendorRatePlanId":"304979059","roomNum":1,"roomId":222126105 },"packType":"2","sessionId":"54cd52119c2a8ee71225315da472ff6f_","operateType":"2","replaceHotelUniqueFlag":"hotel|711527|true|222126105|0|23690|9401106|2019-07-29|2019-07-31|2|0"}
#     # param = {         "hotel": {             "hotelId": 711527,             "checkIn": "2019-08-10",             "checkOut": "2019-08-11",             "adultNum": "2",             "childNum": "0",             "vendorId": 23690,             "vendorRatePlanId": "304979059",             "roomNum": 1,             "roomId": 222126105         },         "packType": "2",         "sessionId": "54cd52119c2a8ee71225315da472ff6f_",         "operateType": "2",         "replaceHotelUniqueFlag": "hotel|711527|true|222126105|0|23690|9401106|2019-07-29|2019-07-31|2|0"     }
#     # vp = findInternalInterface()
#     # fullUrl1 = vp.composeUrl(url4, 'prd')
#     # fullUrl2 = vp.composeUrl(url2, 'prd', param)
#     resp1 = vp.sendrequest(url2, 'prd', param)
#     # resp2 = vp.sendrequest(url4, 'prd')
#     vp.getInternalInterfaceList(resp1)
#     # dependentPebbles = resp2['requestLogs']['dependentPebbles']
#     # print("222222222" +  str(dependentPebbles))
#     # list = vp.getInternalInterfaceList(resp2)
#     # pebble = list[0]
#     # print("pebble" + str(len(pebble)) + str(pebble))
#     # Tsp = list[1]
#     # print("tsp" + str(len(Tsp)) + str(Tsp))
#     # pebblelist = resp2
#     # TSPList = resp2
#
#     # # vp.getInternalInterfaceList(resp1)
#     # # vp.getInternalInterfaceList(resp2)
#     # vp.getIps()
#     # vp.getIpsbyCode('mob-res-pre')
#     # vp.getIpbyUrl(url4,'prd')
#     # vp.getIpbyUrl(url1)


        # url5 = "https://api.tuniu.com/res/pack/saveInternalFlight/app?c=%7B%22cc%22%3A1602%2C%22ct%22%3A20%2C%22dt%22%3A1%2C%22ov%22%3A20%2C%22p%22%3A14584%2C%22v%22%3A%2210.15.0%22%7D"
        # param5 = {
        #     "adultNum": 1,
        #     "childNum": 1,
        #     "flight": {
        #         "cabinCodes": "E#V",
        #         "flightNos": "CZ6172#CZ6197",
        #         "priceInfoId": "",
        #         "queryId": "Y2l0eUtleXM9U0hBLVdVSCNXVUgtU0hBLGRlcGFydHVyZURhdGU9MjAxOS0wOS0xOSxkZXBhcnR1cmVEYXRlcz0wIzEscGFzc2VuZ2VyUXVhbnRpdHk9MSMxIzAjMCxwaHlzaWNhbENhYmluPW51bGw\u003d",
        #         "specVendorId": "",
        #         "vendorId": "1"
        #     },
        #     "sessionId": "4eed619ff2ebfe31985d6462ef22d6d0_"
        # }
        # vp = findInternalInterface()
        # fullUrl2 = vp.composeUrl(url5, 'prd', param5)
        # resp1 = vp.sendrequest(url5, 'prd', param5)
        # vp.getInternalInterfaceList(resp1)

        # url2 = "https://api.tuniu.com/res/pack/saveInternalHotel/app?c=%7B%22cc%22%3A1602%2C%22ct%22%3A20%2C%22dt%22%3A1%2C%22ov%22%3A20%2C%22p%22%3A19326%2C%22v%22%3A%2210.11.0%22%7D"
        # param2 = {
        #     "hotel": {
        #         "hotelId": 711527,
        #         "checkIn": "2019-08-10",
        #         "checkOut": "2019-08-11",
        #         "adultNum": "2",
        #         "childNum": "0",
        #         "vendorId": 23690,
        #         "vendorRatePlanId": "304979059",
        #         "roomNum": 1,
        #         "roomId": 222126105
        #     },
        #     "packType": "2",
        #     "sessionId": "54cd52119c2a8ee71225315da472ff6f_",
        #     "operateType": "2",
        #     "replaceHotelUniqueFlag": "hotel|711527|true|222126105|0|23690|9401106|2019-07-29|2019-07-31|2|0"
        # }
        # vp = findInternalInterface()
        # fullUrl2 = vp.composeUrl(url2, 'prd', param2)
        # resp1 = vp.sendrequest(url2, 'prd', param2)
        # vp.getInternalInterfaceList(resp1)
        #
        # #
        # # url4 = "https://api.tuniu.com/portal/home/list/v3?c=%7B%22cc%22%3A1602%2C%22ct%22%3A10%2C%22p%22%3A14588%2C%22ov%22%3A20%2C%22dt%22%3A0%2C%22v%22%3A%2210.12.0%22%7D&d=%7B%22pageLimit%22%3A10%2C%22bottomOffset%22%3A-1%2C%22currentPage%22%3A1%2C%22needPlay%22%3Atrue%2C%22width%22%3A750%2C%22deviceNum%22%3A%22c6777549d3dca9d907271ee6ac3d189df00fdb49%22%2C%22getRecommendFlag%22%3Afalse%2C%22moduleName%22%3A%22%E5%85%A8%E9%83%A8%22%2C%22moduleId%22%3A%2215539527%22%2C%22abTest%22%3A%22bi%22%2C%22sessionId%22%3A%228aa78300422a479677185ec2119c52eb_%22%2C%22uniqueKey%22%3A%229EA881B7-E104-412A-BD96-5B57413B75B3%22%2C%22isFirst%22%3Atrue%7D"
        # # vp = findInternalInterface()
        # # fullUrl2 = vp.composeUrl(url4, 'pre')
        # # resp1 = vp.sendrequest(url4, 'prd')
        # # vp.getInternalInterfaceList(resp1)