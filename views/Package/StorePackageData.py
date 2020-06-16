# /usr/bin/python
# -*- coding:utf-8 -*-
"""
# project:autoapi
# user:: liju
@author: liju
@time: 2019-10-28 11:21
"""


import json
import logging
from urllib import parse

import requests
from flask import Blueprint
from flask import request, make_response

# 注册蓝图
from app import db
from app.models.models import  HotelData
from app.models.models import *
from views.interfaceAuto.interface import cors_response

StorePackageData = Blueprint('StorePackageData', __name__, url_prefix="")

class StorePackageData:
    def __init__(self, urlData=None, env=None):
        self.__urlData = urlData
        self.__env = env
        self.__responsedata = None

    ### 调用Tadis系统获取所有应用的生产IP
    def GetData(self):
        newUrl = "http://public-api.res.mob.tuniu.org/res/pack/statistics/appData?d={%22type%22:1}"
        self.session = requests.session()
        resp = self.session.get(newUrl)
        self.__status_code = resp.status_code
        print("code is " + str(resp.status_code))
        if resp.status_code == 500 or resp.status_code == 404:
            self.__responsedata = resp.text
        else:
            try:
                print("11111111111111"+str(self.__responsedata))
                self.__responsedata = resp.json()
            except Exception as e:
                logging.error("返回的原始结果json解码失败，可能并不是异常，而是响应就不是json格式的")
                self.__responsedata = resp.text
        logging.info("request url:" + resp.url)
        logging.debug("respone data:" + json.dumps(self.__responsedata, ensure_ascii=False))
        print(json.dumps(self.__responsedata))
        Flightdata  = FlightData(
        date_time = self.__responsedata['data']['dataInfo'][0]['date'],
        defaultRecommed = self.__responsedata['data']['dataInfo'][0]['flightRecommend'],
        defaultFailed = self.__responsedata['data']['dataInfo'][0]['flightRecommendLack'],
        defaultPercent =round( (self.__responsedata['data']['dataInfo'][0]['flightRecommendLack']/self.__responsedata['data']['dataInfo'][0]['flightRecommend'])*100,1),
        systemProduct = self.__responsedata['data']['dataInfo'][0]['flightRecommendPrd'],
        systemFailed =self.__responsedata['data']['dataInfo'][0]['flightRecommendPrdLack'],
        systemPercent =round((self.__responsedata['data']['dataInfo'][0]['flightRecommendPrdLack']/self.__responsedata['data']['dataInfo'][0]['flightRecommendPrd'])*100,1),
        checkPrice =self.__responsedata['data']['dataInfo'][0]['flightCheckPriceCar']+self.__responsedata['data']['dataInfo'][0]['flightCheckPriceBooking'],
        checkFailed = self.__responsedata['data']['dataInfo'][0]['flightCheckPriceCarFail']+self.__responsedata['data']['dataInfo'][0]['flightCheckPriceBookingFail'],
        checkPercent = round((self.__responsedata['data']['dataInfo'][0]['flightCheckPriceCarFail']+self.__responsedata['data']['dataInfo'][0]['flightCheckPriceBookingFail'])/(self.__responsedata['data']['dataInfo'][0]['flightCheckPriceCar']+self.__responsedata['data']['dataInfo'][0]['flightCheckPriceBooking'])*100, 1),
        shoppingCart = self.__responsedata['data']['dataInfo'][0]['flightCheckPriceCar'],
        shoppingFailed =self.__responsedata['data']['dataInfo'][0]['flightCheckPriceCarFail'],
        shoppingPercent =0,
        orderPage =self.__responsedata['data']['dataInfo'][0]['flightCheckPriceBooking'],
        orderFailed =self.__responsedata['data']['dataInfo'][0]['flightCheckPriceBookingFail'],
        orderPercent =0
        )
        db.session.add(Flightdata)
        db.session.commit()

        Hoteldata = HotelData(
        date_time = self.__responsedata['data']['dataInfo'][0]['date'],
        defaultRecommed = self.__responsedata['data']['dataInfo'][0]['hotelRecommend'],
        defaultFailed = self.__responsedata['data']['dataInfo'][0]['hotelRecommendLack'],
        defaultPercent =round( (self.__responsedata['data']['dataInfo'][0]['hotelRecommendLack']/self.__responsedata['data']['dataInfo'][0]['hotelRecommend'])*100,1),
        systemProduct = self.__responsedata['data']['dataInfo'][0]['hotelRecommendPrd'],
        systemFailed =self.__responsedata['data']['dataInfo'][0]['hotelRecommendPrdLack'],
        systemPercent =round((self.__responsedata['data']['dataInfo'][0]['hotelRecommendPrdLack']/self.__responsedata['data']['dataInfo'][0]['hotelRecommendPrd'])*100,1),
        checkPrice =self.__responsedata['data']['dataInfo'][0]['hotelCheckPriceCar']+self.__responsedata['data']['dataInfo'][0]['hotelCheckPriceBooking'],
        checkFailed = self.__responsedata['data']['dataInfo'][0]['hotelCheckPriceCarFail']+self.__responsedata['data']['dataInfo'][0]['hotelCheckPriceBookingFail'],
        checkPercent = round((self.__responsedata['data']['dataInfo'][0]['hotelCheckPriceCarFail']+self.__responsedata['data']['dataInfo'][0]['hotelCheckPriceBookingFail'])/(self.__responsedata['data']['dataInfo'][0]['hotelCheckPriceCar']+self.__responsedata['data']['dataInfo'][0]['hotelCheckPriceBooking'])*100, 1),
        shoppingCart = self.__responsedata['data']['dataInfo'][0]['hotelCheckPriceCar'],
        shoppingFailed =self.__responsedata['data']['dataInfo'][0]['hotelCheckPriceCarFail'],
        shoppingPercent =0,
        orderPage =self.__responsedata['data']['dataInfo'][0]['hotelCheckPriceBooking'],
        orderFailed = self.__responsedata['data']['dataInfo'][0]['hotelCheckPriceBookingFail'],
        orderPercent =0
        )

        db.session.add(Hoteldata)
        db.session.commit()

        Ticketdata = TicketData(date_time=self.__responsedata['data']['dataInfo'][0]['date'],
                              defaultRecommed=self.__responsedata['data']['dataInfo'][0]['scenicRecommend'],
                              defaultFailed=self.__responsedata['data']['dataInfo'][0]['scenicRecommendLack'],
                              defaultPercent=round((self.__responsedata['data']['dataInfo'][0]['scenicRecommendLack'] /
                                                    self.__responsedata['data']['dataInfo'][0]['scenicRecommend']) * 100,
                                                   1),
                              checkPrice=self.__responsedata['data']['dataInfo'][0]['ticketCheckPriceCar'] +
                                         self.__responsedata['data']['dataInfo'][0]['ticketCheckPriceBooking'],
                              checkFailed=self.__responsedata['data']['dataInfo'][0]['ticketCheckPriceCarFail'] +
                                          self.__responsedata['data']['dataInfo'][0]['ticketCheckPriceBookingFail'],
                              checkPercent=round((self.__responsedata['data']['dataInfo'][0]['ticketCheckPriceCarFail'] +
                                                  self.__responsedata['data']['dataInfo'][0][
                                                      'ticketCheckPriceBookingFail']) / (
                                                             self.__responsedata['data']['dataInfo'][0][
                                                                 'ticketCheckPriceCar'] +
                                                             self.__responsedata['data']['dataInfo'][0][
                                                                 'ticketCheckPriceBooking']) * 100, 1),
                              shoppingCart=self.__responsedata['data']['dataInfo'][0]['ticketCheckPriceCar'],
                              shoppingFailed=self.__responsedata['data']['dataInfo'][0]['ticketCheckPriceCarFail'],
                              shoppingPercent=0,
                              orderPage=self.__responsedata['data']['dataInfo'][0]['ticketCheckPriceBooking'],
                              orderFailed=self.__responsedata['data']['dataInfo'][0]['ticketCheckPriceBookingFail'],
                              orderPercent=0)
        db.session.add(Ticketdata)
        db.session.commit()

        Packagebookdata = PackageBookData(    date_time=self.__responsedata['data']['dataInfo'][0]['date'],
                                packageNum=self.__responsedata['data']['dataInfo'][0]['packProduct'],
                                packageFailed=self.__responsedata['data']['dataInfo'][0]['packProductFail'],
                                packagePercent=round(
                                    (self.__responsedata['data']['dataInfo'][0]['packProductFail'] /
                                     self.__responsedata['data']['dataInfo'][0]['packProduct']) * 100,
                                    1),
                                enterBookNum=self.__responsedata['data']['dataInfo'][0]['goBookingPage'],
                                orderNum = None, resign = None,orderNumforHS = None,resignforHS = None
                            )

        db.session.add(Packagebookdata)
        db.session.commit()

        ForeignFlightdata = ForeignFlightData(
            date_time=self.__responsedata['data']['dataInfoAbroad'][0]['date'],
            defaultRecommed=self.__responsedata['data']['dataInfoAbroad'][0]['flightRecommend'],
            defaultFailed=self.__responsedata['data']['dataInfoAbroad'][0]['flightRecommendLack'],
            defaultPercent=round((self.__responsedata['data']['dataInfoAbroad'][0]['flightRecommendLack'] /
                                  self.__responsedata['data']['dataInfoAbroad'][0]['flightRecommend']) * 100, 1),
            checkPrice=self.__responsedata['data']['dataInfoAbroad'][0]['flightCheckPriceCar'] +
                       self.__responsedata['data']['dataInfoAbroad'][0]['flightCheckPriceBooking'],
            checkFailed=self.__responsedata['data']['dataInfoAbroad'][0]['flightCheckPriceCarFail'] +
                        self.__responsedata['data']['dataInfoAbroad'][0]['flightCheckPriceBookingFail'],
            checkPercent=round((self.__responsedata['data']['dataInfoAbroad'][0]['flightCheckPriceCarFail'] +
                                self.__responsedata['data']['dataInfoAbroad'][0]['flightCheckPriceBookingFail']) / (
                                           self.__responsedata['data']['dataInfoAbroad'][0]['flightCheckPriceCar'] +
                                           self.__responsedata['data']['dataInfoAbroad'][0]['flightCheckPriceBooking']) * 100,
                               1),
            shoppingCart=self.__responsedata['data']['dataInfoAbroad'][0]['flightCheckPriceCar'],
            shoppingFailed=self.__responsedata['data']['dataInfoAbroad'][0]['flightCheckPriceCarFail'],
            shoppingPercent=0,
            orderPage=self.__responsedata['data']['dataInfoAbroad'][0]['flightCheckPriceBooking'],
            orderFailed=self.__responsedata['data']['dataInfoAbroad'][0]['flightCheckPriceBookingFail'],
            orderPercent=0
        )
        db.session.add(ForeignFlightdata)
        db.session.commit()

        ForeignHoteldata = ForeignHotelData(
            date_time=self.__responsedata['data']['dataInfoAbroad'][0]['date'],
            defaultRecommed=self.__responsedata['data']['dataInfoAbroad'][0]['hotelRecommend'],
            defaultFailed=self.__responsedata['data']['dataInfoAbroad'][0]['hotelRecommendLack'],
            defaultPercent=round((self.__responsedata['data']['dataInfoAbroad'][0]['hotelRecommendLack'] /
                                  self.__responsedata['data']['dataInfoAbroad'][0]['hotelRecommend']) * 100, 1),
            checkPrice=self.__responsedata['data']['dataInfoAbroad'][0]['hotelCheckPriceCar'] +
                       self.__responsedata['data']['dataInfoAbroad'][0]['hotelCheckPriceBooking'],
            checkFailed=self.__responsedata['data']['dataInfoAbroad'][0]['hotelCheckPriceCarFail'] +
                        self.__responsedata['data']['dataInfoAbroad'][0]['hotelCheckPriceBookingFail'],
            checkPercent=round((self.__responsedata['data']['dataInfoAbroad'][0]['hotelCheckPriceCarFail'] +
                                self.__responsedata['data']['dataInfoAbroad'][0]['hotelCheckPriceBookingFail']) / (
                                           self.__responsedata['data']['dataInfoAbroad'][0]['hotelCheckPriceCar'] +
                                           self.__responsedata['data']['dataInfoAbroad'][0]['hotelCheckPriceBooking']) * 100,
                               1),
            shoppingCart=self.__responsedata['data']['dataInfoAbroad'][0]['hotelCheckPriceCar'],
            shoppingFailed=self.__responsedata['data']['dataInfoAbroad'][0]['hotelCheckPriceCarFail'],
            shoppingPercent=0,
            orderPage=self.__responsedata['data']['dataInfoAbroad'][0]['hotelCheckPriceBooking'],
            orderFailed=self.__responsedata['data']['dataInfoAbroad'][0]['hotelCheckPriceBookingFail'],
            orderPercent=0
        )

        db.session.add(ForeignHoteldata)
        db.session.commit()

        ForeignTicketdata = ForeignTicketData(date_time=self.__responsedata['data']['dataInfoAbroad'][0]['date'],
                                defaultRecommed=self.__responsedata['data']['dataInfoAbroad'][0]['scenicRecommend'],
                                defaultFailed=self.__responsedata['data']['dataInfoAbroad'][0]['scenicRecommendLack'],
                                defaultPercent=round(
                                    (self.__responsedata['data']['dataInfoAbroad'][0]['scenicRecommendLack'] /
                                     self.__responsedata['data']['dataInfoAbroad'][0]['scenicRecommend']) * 100,
                                    1),
                                checkPrice=self.__responsedata['data']['dataInfoAbroad'][0]['ticketCheckPriceCar'] +
                                           self.__responsedata['data']['dataInfoAbroad'][0]['ticketCheckPriceBooking'],
                                checkFailed=self.__responsedata['data']['dataInfoAbroad'][0]['ticketCheckPriceCarFail'] +
                                            self.__responsedata['data']['dataInfoAbroad'][0]['ticketCheckPriceBookingFail'],
                                checkPercent=round(
                                    (self.__responsedata['data']['dataInfoAbroad'][0]['ticketCheckPriceCarFail'] +
                                     self.__responsedata['data']['dataInfoAbroad'][0][
                                         'ticketCheckPriceBookingFail']) / (
                                            self.__responsedata['data']['dataInfoAbroad'][0][
                                                'ticketCheckPriceCar'] +
                                            self.__responsedata['data']['dataInfoAbroad'][0][
                                                'ticketCheckPriceBooking']) * 100, 1),
                                shoppingCart=self.__responsedata['data']['dataInfoAbroad'][0]['ticketCheckPriceCar'],
                                shoppingFailed=self.__responsedata['data']['dataInfoAbroad'][0]['ticketCheckPriceCarFail'],
                                shoppingPercent=0,
                                orderPage=self.__responsedata['data']['dataInfoAbroad'][0]['ticketCheckPriceBooking'],
                                orderFailed=self.__responsedata['data']['dataInfoAbroad'][0]['ticketCheckPriceBookingFail'],
                                orderPercent=0)
        db.session.add(ForeignTicketdata)
        db.session.commit()

        ForeignPackagebookdata = ForeignPackageBookData(date_time=self.__responsedata['data']['dataInfoAbroad'][0]['date'],
                                          packageNum=self.__responsedata['data']['dataInfoAbroad'][0]['packProduct'],
                                          packageFailed=self.__responsedata['data']['dataInfoAbroad'][0]['packProductFail'],
                                          packagePercent=round(
                                              (self.__responsedata['data']['dataInfoAbroad'][0]['packProductFail'] /
                                               self.__responsedata['data']['dataInfoAbroad'][0]['packProduct']) * 100,
                                              1),
                                          enterBookNum=self.__responsedata['data']['dataInfoAbroad'][0]['goBookingPage'],
                                          orderNum=None, resign=None, orderNumforHS=None, resignforHS=None
                                          )

        db.session.add(ForeignPackagebookdata)
        db.session.commit()
        return self.__responsedata



if __name__ == "__main__":
    vp = StorePackageData()
    vp.GetData()



