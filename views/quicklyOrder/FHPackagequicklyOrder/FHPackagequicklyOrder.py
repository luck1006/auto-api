# /usr/bin/python
# -*- coding:utf-8 -*-
"""
# project:autoapi
# user:: liju
@author: liju
@time: 2019-9-30 13:35
"""

# -*- coding: utf-8 -*-
import datetime
import json
import logging
import random
import time

from flask import Blueprint, request

from views.interfaceAuto.interface import cors_response
from views.quicklyOrder.FHPackagequicklyOrder.FHData import FHPackageInfo1

from views.quicklyOrder.FHPackagequicklyOrder.FHPackageSrc import Begin_Session,Login, FHPackage_getDefaultRecommend, \
    FHPackage_CheckPriceAndPackage, FHPackage_addOrder, FHPackage_getInsurance, FHPackage_getPromotion, \
    FHPackage_stepOne, CancelOrder



""" 
机酒打包流程，包括推荐、购物车、预定下单(包含优惠和保险）这一套流程
"""

FHPackageOrder = Blueprint('FHPackageOrder', __name__, url_prefix="")
class FHPackahequicklyOrder:
    def __init__(self, tdata, envdata, cParam=None,session=None):
        self.__success = False
        self.__msg = ""
        self.__orderId = ""
        # 初始化响应结果数据对象,所有接口响应结果以key-value形式存储
        self.__tdata = tdata
        self.__envdata = envdata
        CParam = {"cc": 1602, "ct": 20, "dt": 1, "ov": 20, "p": 19326, "v": "10.13.0"}
        self.Begin_Session = Begin_Session(cParam, session)
        self.Login = Login(cParam, session)
        self.FHPackage_getDefaultRecommend = FHPackage_getDefaultRecommend(CParam, session)
        self.CheckPriceAndPackage = FHPackage_CheckPriceAndPackage(cParam, session)
        self.FHPackage_addOrder = FHPackage_addOrder(cParam)
        self.FHPackage_getInsurance = FHPackage_getInsurance(cParam)
        self.FHPackage_getPromotion = FHPackage_getPromotion(cParam)
        self.FHPackage_StepOne = FHPackage_stepOne(cParam)
        self.CancelOrder = CancelOrder()

    @property
    def tdata(self):
        return self.__tdata

    @tdata.setter
    def tdata(self, value):
        self.__tdata = value

    @property
    def envdata(self):
        return self.__envdata

    @envdata.setter
    def envdata(self, value):
        self.__envdata = value

    def run(self):
        """
        机酒打包业务流程启动，action字段代表这一串业务里可以在哪里终止，预留字段
        :param action: 业务终止位置
        :return: 返回测试结果
        """

        try:
            ###先进行登陆,获取sessionId
            self.Begin_Session.setReqParam()
            self.Begin_Session.sendrequest(self.envdata)

            sessionId = self.Begin_Session.getSessionId()

            self.Login.setReqParam(sessionId)
            self.Login.sendrequest(self.envdata)

            """
            先生成随机出发日期和返回日期
            出发日期距离当前时间1个月至1个半月，不能占用距离较近的资源
            返回日期：出发日期后随机加1-5天
            """
            now = datetime.datetime.now()
            start_delta = datetime.timedelta(days=30)
            start_days = now + start_delta

            startint = random.randint(0, 15)
            start_delta1 = datetime.timedelta(days=startint)
            journeyDepartDate = (start_days + start_delta1)
            logging.debug(
                "行程开始时间是:" + "journeyDepartDate:{}".format(journeyDepartDate.date()))

            touristduration = random.randint(1, 5)
            end_delta11 = datetime.timedelta(days=touristduration)
            journeyEndDate = (journeyDepartDate + end_delta11)
            logging.debug(
                "行程返回时间是:" + "journeyEndDate:{}".format(journeyEndDate.date()))

            ###推荐接口如果没有查询到数据会在185秒（推荐缓存3分钟加5秒）之后开启第2次查询
            i = 1
            while i < 3:
                self.FHPackage_getDefaultRecommend.setReqParam(
                    self.tdata['JourneyInfoList']['bookCityCode'],
                    self.tdata['JourneyInfoList']['bookCityName'],
                    self.tdata['JourneyInfoList'][
                        "departCityCode"],
                    self.tdata['JourneyInfoList'][
                        "departCityName"],
                    str(journeyDepartDate.date()),
                    self.tdata['JourneyInfoList']["adultNum"],
                    self.tdata['JourneyInfoList']["childNum"], 0,
                    2,
                    self.tdata['JourneyInfoList']["cabinType"],
                    self.tdata['JourneyInfoList'][
                        "departCityCode"],
                    self.tdata['JourneyInfoList'][
                        "departCityName"],
                    self.tdata['JourneyInfoList']["destCityCode"],
                    self.tdata['JourneyInfoList']["destCityName"],
                    str(journeyDepartDate.date()),
                    str(journeyEndDate.date()),
                    sessionId)
                self.FHPackage_getDefaultRecommend.sendrequest(self.envdata)
                ResComResult = self.FHPackage_getDefaultRecommend.checkFHResourceComplete()
                if ResComResult == True:
                    logging.debug("推荐接口查询的信息信息完整")
                    break
                else:
                    i = i + 1
                    logging.debug("推荐接口查询的信息不全重新执行，总共执行两次,3分钟后开启第" + str(i + 1) + "次查询")
                    time.sleep(185)

            ### 检查机票基本信息
            if self.FHPackage_getDefaultRecommend.checkflight() is True:
                if self.FHPackage_getDefaultRecommend.checkdepartflightistransit() is False:
                    logging.debug("推荐去程航班直达")
                    logging.debug("推荐去程航班直达" + "推荐机票是：" + str(
                        self.FHPackage_getDefaultRecommend.getFlightInfo()[1][
                            'FlightNo1']) + "推荐机票舱等是:" + str(
                        self.FHPackage_getDefaultRecommend.getFlightInfo()[2]['FlightCabin1']))

                else:
                    logging.debug("推荐去程航班需要中转，航班信息如下")

                if self.FHPackage_getDefaultRecommend.checkdestflightistransit() is False:
                    logging.debug("推荐返程航班直达")
                    logging.debug("推荐去程航班直达" + "推荐机票是：" + str(
                        self.FHPackage_getDefaultRecommend.getFlightInfo()[3][
                            'FlightNo2']) + "推荐机票舱等是:" + str(
                        self.FHPackage_getDefaultRecommend.getFlightInfo()[4]['FlightCabin2']))
                else:
                    logging.debug("推荐返程航班直达")
                logging.debug(
                    "推荐机票总价:" + str(self.FHPackage_getDefaultRecommend.getFlightInfo()[0]['totalPrice']))
                logging.debug(
                    "推荐机票信息:" + str(self.FHPackage_getDefaultRecommend.getFlightInfo()[1:]))

                ### 检查酒店信息
                if self.FHPackage_getDefaultRecommend.checkHotel() is True:
                    ### 检查酒店基本信息
                    logging.debug("推荐酒店名称是: " + str(
                        self.FHPackage_getDefaultRecommend.getHotelInfo()[0][
                            'HotelName']) + "  价格计划名称: " + str(
                        self.FHPackage_getDefaultRecommend.getHotelInfo()[3][
                            'ratePlanName']) + "  总价: " + str(
                        self.FHPackage_getDefaultRecommend.getHotelInfo()[4][
                            'totalPrice']) + "  入住时间: " + str(
                        self.FHPackage_getDefaultRecommend.getHotelInfo()[1][
                            'checkInDate']) + "  离店时间: " + str(
                        self.FHPackage_getDefaultRecommend.getHotelInfo()[2]['checkOutDate']))

                    ### 机酒信息完整则开始验仓验价
                    self.CheckPriceAndPackage.setReqParam(self.tdata['JourneyInfoList']['bookCityCode'],
                                                                         self.tdata['JourneyInfoList']['bookCityName'],
                                                                         self.tdata['JourneyInfoList'][
                                                                             'departCityCode'],
                                                                         self.tdata['JourneyInfoList'][
                                                                             'departCityName'],
                                                                         self.tdata['JourneyInfoList'][
                                                                             'departCityCode'],
                                                                         self.tdata['JourneyInfoList'][
                                                                             'departCityName'],
                                                                         self.tdata['JourneyInfoList']['destCityCode'],
                                                                         self.tdata['JourneyInfoList']['destCityName'],
                                                                         str(journeyDepartDate.date()),
                                                                         str(journeyEndDate.date()),
                                                                         sessionId)
                    self.CheckPriceAndPackage.sendrequest(self.envdata)
                    if self.CheckPriceAndPackage.getCheckResult() == True:
                        logging.debug(
                            "验仓验价成功，资源变化信息如下  :" + str(self.CheckPriceAndPackage.getCheckDesc()))

                        ###获取验仓验价和打包的结果备用于下单
                        productId = self.CheckPriceAndPackage.getProductId()

                        ### 验价成功开始下单先执行stepone接口再执行addorder接口
                        self.FHPackage_StepOne.setReqParam(productId, str(journeyDepartDate.date()),
                                                                    str(journeyEndDate.date()),
                                                                    self.tdata['JourneyInfoList']['bookCityCode'],
                                                                    self.tdata['JourneyInfoList']['departCityCode'],
                                                                    self.tdata['JourneyInfoList']['destCityCode'],
                                                                    self.tdata['JourneyInfoList']['adultNum'],
                                                                    self.tdata['JourneyInfoList']['childNum'],
                                                                    sessionId)
                        self.FHPackage_StepOne.sendrequest(self.envdata)
                        ### bookid生成成功则继续下单
                        bookId = self.FHPackage_StepOne.getBookId()
                        if bookId:
                            logging.debug(
                                "打包预定第一步stepone执行结束，bookId是  :" + str(bookId))

                            ### 下单之前请求保险信息和优惠信息
                            self.FHPackage_getInsurance.setReqParam(productId, str(journeyDepartDate.date()),
                                                                             str(journeyEndDate.date()),
                                                                             self.tdata['JourneyInfoList'][
                                                                                 'bookCityCode'],
                                                                             self.tdata['JourneyInfoList'][
                                                                                 'departCityCode'],
                                                                             self.tdata['JourneyInfoList'][
                                                                                 'destCityCode'],
                                                                             self.tdata['JourneyInfoList']['adultNum'],
                                                                             self.tdata['JourneyInfoList']['childNum'],
                                                                             sessionId)
                            self.FHPackage_getInsurance.sendrequest(self.envdata)

                            self.FHPackage_getPromotion.setReqParam(productId, str(journeyDepartDate.date()),
                                                                             str(journeyEndDate.date()),
                                                                             self.tdata['JourneyInfoList'][
                                                                                 'bookCityCode'],
                                                                             self.tdata['JourneyInfoList'][
                                                                                 'departCityCode'],
                                                                             self.tdata['JourneyInfoList'][
                                                                                 'destCityCode'],
                                                                             self.tdata['JourneyInfoList']['adultNum'],
                                                                             self.tdata['JourneyInfoList']['childNum'],
                                                                             sessionId)
                            self.FHPackage_getPromotion.sendrequest(self.envdata)

                            if self.FHPackage_getInsurance.CheckResult() == True and self.FHPackage_getPromotion.CheckResult() == True:
                                RandomInsurance = self.FHPackage_getInsurance.GetRandomInsurance()[0]
                                InsurancePrice = self.FHPackage_getInsurance.GetRandomInsurance()[1]

                                RandomPromotion = self.FHPackage_getPromotion.GetRandomPromotion()[0]
                                PromotionPrice = self.FHPackage_getPromotion.GetRandomPromotion()[1]

                                self.FHPackage_addOrder.setReqParam(productId, str(journeyDepartDate.date()),
                                                                             str(journeyEndDate.date()),
                                                                             self.tdata['JourneyInfoList'][
                                                                                 'bookCityCode'],
                                                                             self.tdata['JourneyInfoList'][
                                                                                 'departCityCode'],
                                                                             self.tdata['JourneyInfoList'][
                                                                                 'destCityCode'],
                                                                             self.tdata['JourneyInfoList']['adultNum'],
                                                                             self.tdata['JourneyInfoList']['childNum'],
                                                                             bookId, RandomPromotion, RandomInsurance,
                                                                             0,
                                                                             self.tdata['ContractInfo'], "",
                                                                             self.tdata['TouristInfoList'], True,
                                                                             False,[],[],
                                                                             sessionId)
                                self.FHPackage_addOrder.sendrequest(self.envdata)
                                if self.FHPackage_addOrder.getOrderResult() == True:
                                    data = self.FHPackage_addOrder.getOrderInfo()
                                    print("data info is " + str(data))
                                    print(data['productName'] +
                                                  "  订单生成成功，订单号是:" + str(data['orderId']) + "  订单类型是" + str(
                                        data['orderType']))
                                    time.sleep(10)
                                    # self.CancelOrder.setReqParam(data['orderId'])
                                    # self.CancelOrder.sendrequest()
                                    self.success = True
                                    self.msg = "订单打包成功"
                                    self.orderId = str(data['orderId'])

                                else:
                                    logging.debug("订单生成失败")
                                    self.success = False
                                    self.msg = "订单打包失败"
                                    self.orderId = ''
                            else:
                                logging.debug("没有获取保险信息或者优惠信息")
                                self.success = False
                                self.msg = "订单打包失败"
                                self.orderId = ''
                        else:
                            logging.debug("订单第一步stepone没有成功，没有获取bookid")
                            self.success = False
                            self.msg = "订单打包失败"
                            self.orderId = ''
                    else:
                        logging.debug(
                            "验仓验价失败  :" + str(self.CheckPriceAndPackage.getCheckDesc()))
                        self.success = False
                        self.msg = "验仓验价失败"
                        self.orderId = ''

                    ### 推荐接口没有返回酒店数据则用例失败
                else:
                    logging.error("推荐接口没有返回酒店数据");
                    self.success = False
                    self.msg = "推荐接口没有查询到酒店数据"
                    self.orderId = ''

                    ### 推荐接口没有返回机票数据则用例失败
            else:
                logging.error("推荐接口没有返回机票数据");
                self.success = False
                self.msg = "推荐接口没有查询到机票数据"
                self.orderId = ''

        except Exception as e:
            self.success = False
            self.msg = "出现异常"
            self.orderId = ''

        finally:
            logging.info("finally scope")
            resp = cors_response({"success": self.success, "msg": self.msg, "orderId": self.orderId})
            return resp

@FHPackageOrder.route('/FHPackageOrder', methods=['GET', 'POST'])
def runFHPackageOrder():
    envdata = request.get_json().get('envdata')
    print('orderId is:  ' + envdata)
    try:
        vp = FHPackahequicklyOrder(FHPackageInfo1,envdata)
        resp = vp.run()
        print('resp is:  ' + str(resp))
    except:
        resp = cors_response({"success": False, "msg": '生成订单失败，请重新生成或者查看日志', "orderId": ''})
    return resp

if __name__ == "__main__":
#     vp = VisitProduct(ProductSet["data"][0])
#     print("业务结果：\r\n" + str(vp.run()))
# if __name__ == "__main__":
#     # 必选机票+酒店 210598660
#     CParam = {"cc": 1602, "ct": 10, "p": 14588, "ov": 20, "dt": 0, "v": "9.53.0"}
    vp = FHPackahequicklyOrder(FHPackageInfo1,'pre')
    vp.run()
    print("业务结果：\r\ n" + json.dumps(vp.run(), ensure_ascii=False))
    # 必选只有打包资源 210341880
    # vp = VisitProduct(ProductSet["data"][2])
    # print("业务结果：\r\n" + json.dumps(vp.run(), ensure_ascii=False))
    # 必选机票+打包+酒店 210300427
    # vp = VisitProduct(ProductSet["data"][5])
    # print("业务结果：\r\n" + json.dumps(vp.run(), ensure_ascii=False))
    # 多酒店行程 210227984
    # vp = VisitProduct(ProductSet["data"][4])
    # print("业务结果：\r\n" + json.dumps(vp.run(), ensure_ascii=False))
