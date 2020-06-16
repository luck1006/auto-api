# -*- coding: utf-8 -*-
# TIME:         6.24
# Author:       huangfang
# Explain：     获取每周下单和会员登录统计数据

from app.models.models import *
from flask import Blueprint
from sqlalchemy import func, and_, desc
import json
import sys
from flask import current_app

# 设置蓝图
orderLogin = Blueprint('orderLogin', __name__)

@orderLogin.route('/orderLogin')
def getorderLogin():
    try:
        # 获取表里最近一周的统计数据的周数
         week1 = db.session.query(Order_week_statistics.week).order_by((Order_week_statistics.week).desc()).limit(1).all()
         week = str(week1[0][0])

        # 获取最近一周度假产品下单成功的数量
         successCount_holiday1= db.session.query(Order_week_statistics.count).filter(Order_week_statistics.productType=='度假').filter(Order_week_statistics.isSuccess=='1').filter(Order_week_statistics.week== week ).all()
         successCount_holiday=successCount_holiday1[0][0]

        # 获取最近一周度假产品下单失败的数量
         failCount_holiday1= db.session.query(Order_week_statistics.count).filter(Order_week_statistics.productType=='度假').filter(Order_week_statistics.isSuccess=='0').filter(Order_week_statistics.week== week ).all()
         failCount_holiday = failCount_holiday1[0][0]

    # 获取最近一周零售产品下单成功的数量
         successCount_mall1 = db.session.query(Order_week_statistics.count).filter(
         Order_week_statistics.productType == '零售').filter(Order_week_statistics.isSuccess == '1').filter(
         Order_week_statistics.week == week).all()
         successCount_mall=successCount_mall1[0][0]

       # 获取最近一周度假产品下单失败的数量
         failCount_mall1 = db.session.query(Order_week_statistics.count).filter(
         Order_week_statistics.productType == '零售').filter(Order_week_statistics.isSuccess == '0').filter(
         Order_week_statistics.week == week).all()
         failCount_mall=failCount_mall1[0][0]

        # 获取最近一周会员登录成功的数量
         successCount_login1= db.session.query(Order_week_statistics.count).filter(
         Order_week_statistics.productType == '登录').filter(Order_week_statistics.isSuccess == '1').filter(
         Order_week_statistics.week == week).all()
         successCount_login=successCount_login1[0][0]


    # 获取最近一周度假会员登录失败的数量
         failCount_login1 = db.session.query(Order_week_statistics.count).filter(
         Order_week_statistics.productType == '登录').filter(Order_week_statistics.isSuccess == '0').filter(
         Order_week_statistics.week == week).all()
         failCount_login=failCount_login1[0][0]
         if (failCount_mall+successCount_mall) == 0:
             mallfailureRate = 0
         else:
             mallfailureRate = (failCount_mall/(failCount_mall+successCount_mall))*100
         if (failCount_holiday+successCount_holiday) == 0:
             tourfailureRate = 0
         else:
             tourfailureRate = (failCount_holiday/(failCount_holiday+successCount_holiday))*100
         if (failCount_login+successCount_login) == 0:
             loginfailureRate = 0
         else:
             loginfailureRate = (failCount_login/(failCount_login+successCount_login))*100


         response = (
             {"success": "true", "msg": "OK",
              "data":{
               "week":week,
             'orderCount': [
            {
             'productType': '零售下单',
             'successCount': successCount_mall,
             'failCount': failCount_mall,
             'failureRate': "%.2f%%" % mallfailureRate
             },
           {
             'productType': '度假下单',
             'successCount': successCount_holiday,
             'failCount': failCount_holiday,
             'failureRate': "%.2f%%" % tourfailureRate
           },
           {
            'productType': '会员登录',
            'successCount': successCount_login,
            'failCount': failCount_login,
            'failureRate': "%.2f%%" % loginfailureRate
           }
            ]}})
    except Exception as e:
        raise e
        response = ({"success": "false", "msg": "操作失败～～"})
    response = json.dumps(response)
    return response




#if __name__ == '__main__':

    #pass
    #week1 = db.session.query(Order_week_statistics.week).order_by((Order_week_statistics.week).desc()).limit(1).all()
    #week =week1[0][0]
    #successCount1 = db.session.query(Order_week_statistics.count).filter(
        #Order_week_statistics.productType == '零售').filter(Order_week_statistics.isSuccess == '1').filter(
        #Order_week_statistics.week == week).all()
    #successCount=successCount1[0][0]

    #print (response)

