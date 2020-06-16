# /usr/bin/python
# -*- coding:utf-8 -*-
"""
# project:autoapi
# user:: liju
@author: liju
@time: 2019-10-28 11:21
"""
import datetime

from flask import Blueprint
# 注册蓝图
from sqlalchemy import text

from app import db
from app.actions.tools.conf import cors_response
from app.models.models import FlightData, HotelData, TicketData, PackageBookData, ForeignFlightData, ForeignHotelData, \
    ForeignTicketData, ForeignPackageBookData

GetPackageData = Blueprint('GetPackageData', __name__, url_prefix="")


class getPackageData:
    def __init__(self, urlData=None, env=None):
        self.__urlData = urlData
        self.__env = env
        self.__responsedata = None

    ### 按月份获取机票数据

@GetPackageData.route('/GetFlightDataByMonth', methods=['GET', 'POST'])
def getFlightData():

    ratelist = []
    numberlist= []
    result1 = []
    result2 = []
    result3 = []
    result4 = []
    result5 = []
    result6 = []
    result7 = []
    result8 = []
    result9 = []
    result10 = []
    result11 =[]
    result12 = []
    result13 = []
    result14 = []

    """机票推荐失败率"""
    result = db.session.query(FlightData.defaultPercent).limit(40).all()
    for i in range(0, len(result)):
        result3.append(result[i][0])

    """系统推荐失败率"""
    result = db.session.query(FlightData.systemPercent).limit(40).all()
    for i in range(0, len(result)):
        result6.append(result[i][0])

    """验价失败率"""
    result = db.session.query(FlightData.checkPercent).limit(40).all()
    for i in range(0, len(result)):
        result9.append(result[i][0])

    """返回最近30天的时间数据"""
    result = db.session.query(FlightData.date_time).limit(40).all()
    for i in range(0, len(result)):
        result10.append(result[i][0])

    """rate相关数据和时间数据放入ratedata，用于比率试图的数据来源"""
    ratelist.append(result3)
    ratelist.append(result6)
    ratelist.append(result9)
    ratelist.append(result10)

    """机票默认推荐次数"""
    result = db.session.query(FlightData.defaultRecommed).limit(40).all()
    for i in range(0, len(result)):
        result1.append(result[i][0])

    """机票默认推荐失败次数"""
    result = db.session.query(FlightData.defaultFailed).limit(40).all()
    for i in range(0, len(result)):
        result2.append(result[i][0])


    """机票系统打包产品推荐次数"""
    result = db.session.query(FlightData.systemProduct).limit(40).all()
    for i in range(0, len(result)):
        result4.append(result[i][0])

    """机票系统打包产品推荐失败次数"""
    result = db.session.query(FlightData.systemFailed).limit(40).all()
    for i in range(0, len(result)):
        result5.append(result[i][0])

    """机票总验价次数"""
    result = db.session.query(FlightData.checkPrice).limit(40).all()
    for i in range(0, len(result)):
        result7.append(result[i][0])

    """机票验价失败总次数"""
    result = db.session.query(FlightData.checkFailed).limit(40).all()
    for i in range(0, len(result)):
        result8.append(result[i][0])

    """机票购物车验价次数"""
    result = db.session.query(FlightData.shoppingCart).limit(40).all()
    for i in range(0, len(result)):
        result11.append(result[i][0])

    """机票购物车验价失败次数"""
    result = db.session.query(FlightData.shoppingFailed).limit(40).all()
    for i in range(0, len(result)):
        result12.append(result[i][0])

    """机票预定页验价次数"""
    result = db.session.query(FlightData.orderPage).limit(40).all()
    for i in range(0, len(result)):
        result13.append(result[i][0])

    """机票预定页验价失败次数"""
    result = db.session.query(FlightData.orderFailed).limit(40).all()
    for i in range(0, len(result)):
        result14.append(result[i][0])
    numberlist.append(result1)
    numberlist.append(result2)
    numberlist.append(result4)
    numberlist.append(result5)
    numberlist.append(result7)
    numberlist.append(result8)
    numberlist.append(result11)
    numberlist.append(result12)
    numberlist.append(result13)
    numberlist.append(result14)

    resp = cors_response({"success": True, "ratedata": ratelist, "numberdata" : numberlist})
    return  resp



@GetPackageData.route('/GetHotelDataByMonth', methods=['GET', 'POST'])
def getHotelData():

    ratelist = []
    numberlist= []
    result1 = []
    result2 = []
    result3 = []
    result4 = []
    result5 = []
    result6 = []
    result7 = []
    result8 = []
    result9 = []
    result10 = []
    result11 =[]
    result12 = []
    result13 = []
    result14 = []

    """酒店推荐失败率"""
    result = db.session.query(HotelData.defaultPercent).limit(40).all()
    for i in range(0, len(result)):
        result3.append(result[i][0])

    """系统推荐失败率"""
    result = db.session.query(HotelData.systemPercent).limit(40).all()
    for i in range(0, len(result)):
        result6.append(result[i][0])

    """验价失败率"""
    result = db.session.query(HotelData.checkPercent).limit(40).all()
    for i in range(0, len(result)):
        result9.append(result[i][0])

    """返回最近30天的时间数据"""
    result = db.session.query(HotelData.date_time).limit(40).all()
    for i in range(0, len(result)):
        result10.append(result[i][0])

    """rate相关数据和时间数据放入ratedata，用于比率试图的数据来源"""
    ratelist.append(result3)
    ratelist.append(result6)
    ratelist.append(result9)
    ratelist.append(result10)

    """酒店默认推荐次数"""
    result = db.session.query(HotelData.defaultRecommed).limit(40).all()
    for i in range(0, len(result)):
        result1.append(result[i][0])

    """酒店默认推荐失败次数"""
    result = db.session.query(HotelData.defaultFailed).limit(40).all()
    for i in range(0, len(result)):
        result2.append(result[i][0])


    """酒店系统打包产品推荐次数"""
    result = db.session.query(HotelData.systemProduct).limit(40).all()
    for i in range(0, len(result)):
        result4.append(result[i][0])

    """酒店系统打包产品推荐失败次数"""
    result = db.session.query(HotelData.systemFailed).limit(40).all()
    for i in range(0, len(result)):
        result5.append(result[i][0])

    """酒店总验价次数"""
    result = db.session.query(HotelData.checkPrice).limit(40).all()
    for i in range(0, len(result)):
        result7.append(result[i][0])

    """酒店验价失败总次数"""
    result = db.session.query(HotelData.checkFailed).limit(40).all()
    for i in range(0, len(result)):
        result8.append(result[i][0])

    """酒店购物车验价次数"""
    result = db.session.query(HotelData.shoppingCart).limit(40).all()
    for i in range(0, len(result)):
        result11.append(result[i][0])

    """酒店购物车验价失败次数"""
    result = db.session.query(HotelData.shoppingFailed).limit(40).all()
    for i in range(0, len(result)):
        result12.append(result[i][0])

    """酒店预定页验价次数"""
    result = db.session.query(HotelData.orderPage).limit(40).all()
    for i in range(0, len(result)):
        result13.append(result[i][0])

    """酒店预定页验价失败次数"""
    result = db.session.query(HotelData.orderFailed).limit(40).all()
    for i in range(0, len(result)):
        result14.append(result[i][0])
    numberlist.append(result1)
    numberlist.append(result2)
    numberlist.append(result4)
    numberlist.append(result5)
    numberlist.append(result7)
    numberlist.append(result8)
    numberlist.append(result11)
    numberlist.append(result12)
    numberlist.append(result13)
    numberlist.append(result14)

    resp = cors_response({"success": True, "ratedata": ratelist, "numberdata": numberlist})
    return  resp

@GetPackageData.route('/GetTicketDataByMonth', methods=['GET', 'POST'])
def getHTicketData():
    ratelist = []
    numberlist= []
    result1 = []
    result2 = []
    result3 = []
    result4 = []
    result5 = []
    result6 = []
    result7 = []
    result8 = []
    result9 = []
    result10 = []
    result11 =[]

    """门票推荐失败率"""
    result = db.session.query(TicketData.defaultPercent).limit(40).all()
    for i in range(0, len(result)):
        result3.append(result[i][0])

    """验价失败率"""
    result = db.session.query(TicketData.checkPercent).limit(40).all()
    for i in range(0, len(result)):
        result6.append(result[i][0])

    """返回最近30天的时间数据"""
    result = db.session.query(TicketData.date_time).limit(40).all()
    for i in range(0, len(result)):
        result11.append(result[i][0])

    """rate相关数据和时间数据放入ratedata，用于比率试图的数据来源"""
    ratelist.append(result3)
    ratelist.append(result6)
    ratelist.append(result11)

    """门票默认推荐次数"""
    result = db.session.query(TicketData.defaultRecommed).limit(40).all()
    for i in range(0, len(result)):
        result1.append(result[i][0])

    """门票默认推荐失败次数"""
    result = db.session.query(TicketData.defaultFailed).limit(40).all()
    for i in range(0, len(result)):
        result2.append(result[i][0])

    """门票总验价次数"""
    result = db.session.query(TicketData.checkPrice).limit(40).all()
    for i in range(0, len(result)):
        result4.append(result[i][0])

    """酒店验价失败总次数"""
    result = db.session.query(TicketData.checkFailed).limit(40).all()
    for i in range(0, len(result)):
        result5.append(result[i][0])

    """门票购物车验价次数"""
    result = db.session.query(TicketData.shoppingCart).limit(40).all()
    for i in range(0, len(result)):
        result7.append(result[i][0])

    """门票购物车验价失败次数"""
    result = db.session.query(TicketData.shoppingFailed).limit(40).all()
    for i in range(0, len(result)):
        result8.append(result[i][0])

    """门票预定页验价次数"""
    result = db.session.query(TicketData.orderPage).limit(40).all()
    for i in range(0, len(result)):
        result9.append(result[i][0])

    """门票预定页验价失败次数"""
    result = db.session.query(TicketData.orderFailed).limit(40).all()
    for i in range(0, len(result)):
        result10.append(result[i][0])

    numberlist.append(result1)
    numberlist.append(result2)
    numberlist.append(result4)
    numberlist.append(result5)
    numberlist.append(result7)
    numberlist.append(result8)
    numberlist.append(result9)
    numberlist.append(result10)

    resp = cors_response({"success": True, "ratedata": ratelist, "numberdata": numberlist})
    return  resp

@GetPackageData.route('/GetBookDataByMonth', methods=['GET', 'POST'])
def getBookData():
    ratelist = []
    numberlist= []
    result1 = []
    result2 = []
    result3 = []
    result4 = []
    result5 = []
    result6 = []
    result7 = []
    result8 = []

    """打包推荐失败率"""
    result = db.session.query(PackageBookData.packagePercent).limit(40).all()
    for i in range(0, len(result)):
        result3.append(result[i][0])

    """返回最近30天的时间数据"""
    result = db.session.query(PackageBookData.date_time).limit(40).all()
    for i in range(0, len(result)):
        result1.append(result[i][0])

    """rate相关数据和时间数据放入ratedata，用于比率试图的数据来源"""
    ratelist.append(result3)
    ratelist.append(result1)

    """打包接口调用次数"""
    result = db.session.query(PackageBookData.packageNum).limit(40).all()
    for i in range(0, len(result)):
        result2.append(result[i][0])

    """进入预定页次数"""
    result = db.session.query(PackageBookData.enterBookNum).limit(40).all()
    for i in range(0, len(result)):
        result4.append(result[i][0])

    """机酒下单数"""
    result = db.session.query(PackageBookData.orderNum).limit(40).all()
    for i in range(0, len(result)):
        result5.append(result[i][0])

    """机酒签约数"""
    result = db.session.query(PackageBookData.resign).limit(40).all()
    for i in range(0, len(result)):
        result6.append(result[i][0])

    """酒景下单数"""
    result = db.session.query(PackageBookData.orderNumforHS).limit(40).all()
    for i in range(0, len(result)):
        result7.append(result[i][0])

    """酒景签约数"""
    result = db.session.query(PackageBookData.resignforHS).limit(40).all()
    for i in range(0, len(result)):
        result8.append(result[i][0])


    numberlist.append(result2)
    numberlist.append(result4)
    numberlist.append(result5)
    numberlist.append(result6)
    numberlist.append(result7)
    numberlist.append(result8)

    resp = cors_response({"success": True, "ratedata": ratelist, "numberdata": numberlist})
    return  resp












@GetPackageData.route('/GetForeignFlightDataByMonth', methods=['GET', 'POST'])
def getForeignFlightData():

    ratelist = []
    numberlist= []
    result1 = []
    result2 = []
    result3 = []
    result4 = []
    result5 = []
    result6 = []
    result7 = []
    result8 = []
    result9 = []
    result10 = []
    result11 =[]
    result12 = []
    result13 = []
    result14 = []

    """机票推荐失败率"""
    result = db.session.query(ForeignFlightData.defaultPercent).limit(40).all()
    for i in range(0, len(result)):
        result3.append(result[i][0])

    # """系统推荐失败率"""
    # result = db.session.query(ForeignFlightData.systemPercent).limit(40).all()
    # for i in range(0, len(result)):
    #     result6.append(result[i][0])

    """验价失败率"""
    result = db.session.query(ForeignFlightData.checkPercent).limit(40).all()
    for i in range(0, len(result)):
        result9.append(result[i][0])

    """返回最近30天的时间数据"""
    result = db.session.query(ForeignFlightData.date_time).limit(40).all()
    for i in range(0, len(result)):
        result10.append(result[i][0])

    """rate相关数据和时间数据放入ratedata，用于比率试图的数据来源"""
    ratelist.append(result3)
    # ratelist.append(result6)
    ratelist.append(result9)
    ratelist.append(result10)

    """机票默认推荐次数"""
    result = db.session.query(ForeignFlightData.defaultRecommed).limit(40).all()
    for i in range(0, len(result)):
        result1.append(result[i][0])

    """机票默认推荐失败次数"""
    result = db.session.query(ForeignFlightData.defaultFailed).limit(40).all()
    for i in range(0, len(result)):
        result2.append(result[i][0])


    # """机票系统打包产品推荐次数"""
    # result = db.session.query(ForeignFlightData.systemProduct).limit(40).all()
    # for i in range(0, len(result)):
    #     result4.append(result[i][0])

    # """机票系统打包产品推荐失败次数"""
    # result = db.session.query(ForeignFlightData.systemFailed).limit(40).all()
    # for i in range(0, len(result)):
    #     result5.append(result[i][0])

    """机票总验价次数"""
    result = db.session.query(ForeignFlightData.checkPrice).limit(40).all()
    for i in range(0, len(result)):
        result7.append(result[i][0])

    """机票验价失败总次数"""
    result = db.session.query(ForeignFlightData.checkFailed).limit(40).all()
    for i in range(0, len(result)):
        result8.append(result[i][0])

    """机票购物车验价次数"""
    result = db.session.query(ForeignFlightData.shoppingCart).limit(40).all()
    for i in range(0, len(result)):
        result11.append(result[i][0])

    """机票购物车验价失败次数"""
    result = db.session.query(ForeignFlightData.shoppingFailed).limit(40).all()
    for i in range(0, len(result)):
        result12.append(result[i][0])

    """机票预定页验价次数"""
    result = db.session.query(ForeignFlightData.orderPage).limit(40).all()
    for i in range(0, len(result)):
        result13.append(result[i][0])

    """机票预定页验价失败次数"""
    result = db.session.query(ForeignFlightData.orderFailed).limit(40).all()
    for i in range(0, len(result)):
        result14.append(result[i][0])
    numberlist.append(result1)
    numberlist.append(result2)
    # numberlist.append(result4)
    # numberlist.append(result5)
    numberlist.append(result7)
    numberlist.append(result8)
    numberlist.append(result11)
    numberlist.append(result12)
    numberlist.append(result13)
    numberlist.append(result14)

    resp = cors_response({"success": True, "ratedata": ratelist, "numberdata" : numberlist})
    return  resp



@GetPackageData.route('/GetForeignHotelDataByMonth', methods=['GET', 'POST'])
def getForeignHotelData():

    ratelist = []
    numberlist= []
    result1 = []
    result2 = []
    result3 = []
    result4 = []
    result5 = []
    result6 = []
    result7 = []
    result8 = []
    result9 = []
    result10 = []
    result11 =[]
    result12 = []
    result13 = []
    result14 = []

    """酒店推荐失败率"""
    result = db.session.query(ForeignHotelData.defaultPercent).limit(40).all()
    for i in range(0, len(result)):
        result3.append(result[i][0])

    # """系统推荐失败率"""
    # result = db.session.query(ForeignHotelData.systemPercent).limit(40).all()
    # for i in range(0, len(result)):
    #     result6.append(result[i][0])

    """验价失败率"""
    result = db.session.query(ForeignHotelData.checkPercent).limit(40).all()
    for i in range(0, len(result)):
        result9.append(result[i][0])

    """返回最近30天的时间数据"""
    result = db.session.query(ForeignHotelData.date_time).limit(40).all()
    for i in range(0, len(result)):
        result10.append(result[i][0])

    """rate相关数据和时间数据放入ratedata，用于比率试图的数据来源"""
    ratelist.append(result3)
    # ratelist.append(result6)
    ratelist.append(result9)
    ratelist.append(result10)

    """酒店默认推荐次数"""
    result = db.session.query(ForeignHotelData.defaultRecommed).limit(40).all()
    for i in range(0, len(result)):
        result1.append(result[i][0])

    """酒店默认推荐失败次数"""
    result = db.session.query(ForeignHotelData.defaultFailed).limit(40).all()
    for i in range(0, len(result)):
        result2.append(result[i][0])


    # """酒店系统打包产品推荐次数"""
    # result = db.session.query(ForeignHotelData.systemProduct).limit(40).all()
    # for i in range(0, len(result)):
    #     result4.append(result[i][0])
    #
    # """酒店系统打包产品推荐失败次数"""
    # result = db.session.query(ForeignHotelData.systemFailed).limit(40).all()
    # for i in range(0, len(result)):
    #     result5.append(result[i][0])

    """酒店总验价次数"""
    result = db.session.query(ForeignHotelData.checkPrice).limit(40).all()
    for i in range(0, len(result)):
        result7.append(result[i][0])

    """酒店验价失败总次数"""
    result = db.session.query(ForeignHotelData.checkFailed).limit(40).all()
    for i in range(0, len(result)):
        result8.append(result[i][0])

    """酒店购物车验价次数"""
    result = db.session.query(ForeignHotelData.shoppingCart).limit(40).all()
    for i in range(0, len(result)):
        result11.append(result[i][0])

    """酒店购物车验价失败次数"""
    result = db.session.query(ForeignHotelData.shoppingFailed).limit(40).all()
    for i in range(0, len(result)):
        result12.append(result[i][0])

    """酒店预定页验价次数"""
    result = db.session.query(ForeignHotelData.orderPage).limit(40).all()
    for i in range(0, len(result)):
        result13.append(result[i][0])

    """酒店预定页验价失败次数"""
    result = db.session.query(ForeignHotelData.orderFailed).limit(40).all()
    for i in range(0, len(result)):
        result14.append(result[i][0])
    numberlist.append(result1)
    numberlist.append(result2)
    # numberlist.append(result4)
    # numberlist.append(result5)
    numberlist.append(result7)
    numberlist.append(result8)
    numberlist.append(result11)
    numberlist.append(result12)
    numberlist.append(result13)
    numberlist.append(result14)

    resp = cors_response({"success": True, "ratedata": ratelist, "numberdata": numberlist})
    return  resp

@GetPackageData.route('/GetForeignTicketDataByMonth', methods=['GET', 'POST'])
def getForeignTicketData():
    ratelist = []
    numberlist= []
    result1 = []
    result2 = []
    result3 = []
    result4 = []
    result5 = []
    result6 = []
    result7 = []
    result8 = []
    result9 = []
    result10 = []
    result11 =[]

    """门票推荐失败率"""
    result = db.session.query(ForeignTicketData.defaultPercent).limit(40).all()
    for i in range(0, len(result)):
        result3.append(result[i][0])

    """验价失败率"""
    result = db.session.query(ForeignTicketData.checkPercent).limit(40).all()
    for i in range(0, len(result)):
        result6.append(result[i][0])

    """返回最近30天的时间数据"""
    result = db.session.query(ForeignTicketData.date_time).limit(40).all()
    for i in range(0, len(result)):
        result11.append(result[i][0])

    """rate相关数据和时间数据放入ratedata，用于比率试图的数据来源"""
    ratelist.append(result3)
    ratelist.append(result6)
    ratelist.append(result11)

    """门票默认推荐次数"""
    result = db.session.query(ForeignTicketData.defaultRecommed).limit(40).all()
    for i in range(0, len(result)):
        result1.append(result[i][0])

    """门票默认推荐失败次数"""
    result = db.session.query(ForeignTicketData.defaultFailed).limit(40).all()
    for i in range(0, len(result)):
        result2.append(result[i][0])

    """门票总验价次数"""
    result = db.session.query(ForeignTicketData.checkPrice).limit(40).all()
    for i in range(0, len(result)):
        result4.append(result[i][0])

    """酒店验价失败总次数"""
    result = db.session.query(ForeignTicketData.checkFailed).limit(40).all()
    for i in range(0, len(result)):
        result5.append(result[i][0])

    """门票购物车验价次数"""
    result = db.session.query(ForeignTicketData.shoppingCart).limit(40).all()
    for i in range(0, len(result)):
        result7.append(result[i][0])

    """门票购物车验价失败次数"""
    result = db.session.query(ForeignTicketData.shoppingFailed).limit(40).all()
    for i in range(0, len(result)):
        result8.append(result[i][0])

    """门票预定页验价次数"""
    result = db.session.query(ForeignTicketData.orderPage).limit(40).all()
    for i in range(0, len(result)):
        result9.append(result[i][0])

    """门票预定页验价失败次数"""
    result = db.session.query(ForeignTicketData.orderFailed).limit(40).all()
    for i in range(0, len(result)):
        result10.append(result[i][0])

    numberlist.append(result1)
    numberlist.append(result2)
    numberlist.append(result4)
    numberlist.append(result5)
    numberlist.append(result7)
    numberlist.append(result8)
    numberlist.append(result9)
    numberlist.append(result10)

    resp = cors_response({"success": True, "ratedata": ratelist, "numberdata": numberlist})
    return  resp

@GetPackageData.route('/GetForeignBookDataByMonth', methods=['GET', 'POST'])
def getForeignBookData():
    ratelist = []
    numberlist= []
    result1 = []
    result2 = []
    result3 = []
    result4 = []
    result5 = []
    result6 = []
    result7 = []
    result8 = []

    """打包推荐失败率"""
    result = db.session.query(ForeignPackageBookData.packagePercent).limit(40).all()
    for i in range(0, len(result)):
        result3.append(result[i][0])

    """返回最近30天的时间数据"""
    result = db.session.query(ForeignPackageBookData.date_time).limit(40).all()
    for i in range(0, len(result)):
        result1.append(result[i][0])

    """rate相关数据和时间数据放入ratedata，用于比率试图的数据来源"""
    ratelist.append(result3)
    ratelist.append(result1)

    """打包接口调用次数"""
    result = db.session.query(ForeignPackageBookData.packageNum).limit(40).all()
    for i in range(0, len(result)):
        result2.append(result[i][0])

    """进入预定页次数"""
    result = db.session.query(ForeignPackageBookData.enterBookNum).limit(40).all()
    for i in range(0, len(result)):
        result4.append(result[i][0])

    """机酒下单数"""
    result = db.session.query(ForeignPackageBookData.orderNum).limit(40).all()
    for i in range(0, len(result)):
        result5.append(result[i][0])

    """机酒签约数"""
    result = db.session.query(ForeignPackageBookData.resign).limit(40).all()
    for i in range(0, len(result)):
        result6.append(result[i][0])

    """酒景下单数"""
    result = db.session.query(ForeignPackageBookData.orderNumforHS).limit(40).all()
    for i in range(0, len(result)):
        result7.append(result[i][0])

    """酒景签约数"""
    result = db.session.query(ForeignPackageBookData.resignforHS).limit(40).all()
    for i in range(0, len(result)):
        result8.append(result[i][0])


    numberlist.append(result2)
    numberlist.append(result4)
    numberlist.append(result5)
    numberlist.append(result6)
    numberlist.append(result7)
    numberlist.append(result8)

    resp = cors_response({"success": True, "ratedata": ratelist, "numberdata": numberlist})
    return  resp

















if __name__ == "__main__":
    ratelist = []
    numberlist = []
    result1 = []
    result2 = []
    result3 = []
    result4 = []
    result5 = []
    result6 = []
    result7 = []
    result8 = []
    result9 = []
    result10 = []
    result11 = []
    result12 = []
    result13 = []
    result14 = []

    """酒店推荐失败率"""
    result = db.session.query(HotelData.defaultPercent).limit(40).all()
    for i in range(0, len(result)):
        result3.append(result[i][0])

    """系统推荐失败率"""
    result = db.session.query(HotelData.systemPercent).limit(40).all()
    for i in range(0, len(result)):
        result6.append(result[i][0])

    """验价失败率"""
    result = db.session.query(HotelData.checkPercent).limit(40).all()
    for i in range(0, len(result)):
        result9.append(result[i][0])

    """返回最近30天的时间数据"""
    result = db.session.query(HotelData.date_time).limit(40).all()
    for i in range(0, len(result)):
        result10.append(result[i][0])

    """rate相关数据和时间数据放入ratedata，用于比率试图的数据来源"""
    ratelist.append(result3)
    ratelist.append(result6)
    ratelist.append(result9)
    ratelist.append(result10)

    """酒店默认推荐次数"""
    result = db.session.query(HotelData.defaultRecommed).limit(40).all()
    for i in range(0, len(result)):
        result1.append(result[i][0])

    """酒店默认推荐失败次数"""
    result = db.session.query(HotelData.defaultFailed).limit(40).all()
    for i in range(0, len(result)):
        result2.append(result[i][0])

    """酒店系统打包产品推荐次数"""
    result = db.session.query(HotelData.systemProduct).limit(40).all()
    for i in range(0, len(result)):
        result4.append(result[i][0])

    """酒店系统打包产品推荐失败次数"""
    result = db.session.query(HotelData.systemFailed).limit(40).all()
    for i in range(0, len(result)):
        result5.append(result[i][0])

    """酒店总验价次数"""
    result = db.session.query(HotelData.checkPrice).limit(40).all()
    for i in range(0, len(result)):
        result7.append(result[i][0])

    """酒店验价失败总次数"""
    result = db.session.query(HotelData.checkFailed).limit(40).all()
    for i in range(0, len(result)):
        result8.append(result[i][0])

    """酒店购物车验价次数"""
    result = db.session.query(HotelData.shoppingCart).limit(40).all()
    for i in range(0, len(result)):
        result11.append(result[i][0])

    """酒店购物车验价失败次数"""
    result = db.session.query(HotelData.shoppingFailed).limit(40).all()
    for i in range(0, len(result)):
        result12.append(result[i][0])

    """酒店预定页验价次数"""
    result = db.session.query(HotelData.orderPage).limit(40).all()
    for i in range(0, len(result)):
        result13.append(result[i][0])

    """酒店预定页验价失败次数"""
    result = db.session.query(HotelData.orderFailed).limit(40).all()
    for i in range(0, len(result)):
        result14.append(result[i][0])
    numberlist.append(result1)
    numberlist.append(result2)
    numberlist.append(result4)
    numberlist.append(result5)
    numberlist.append(result7)
    numberlist.append(result8)
    numberlist.append(result11)
    numberlist.append(result12)
    numberlist.append(result13)
    numberlist.append(result14)
    print(str(ratelist))
    print(str(numberlist))

    result = db.session.query(HotelData.date_time).limit(40).all()
    print(str(result))
    result = db.session.query(FlightData.date_time).limit(40).all()
    print(str(result))
    resp = {"success": True, "ratedata": ratelist, "numberdata": numberlist}
    print(str(resp))
