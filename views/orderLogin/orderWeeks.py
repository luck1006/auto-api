# -*- coding: utf-8 -*-
# TIME:         7.4
# Author:       huangfang
# Explain：     获取最近10周度假&零售下单成功数据

from app.models.models import *
from flask import Blueprint
from sqlalchemy import func, and_, desc
import json
import sys
from flask import current_app

# 设置蓝图
orderWeeks = Blueprint('orderWeeks', __name__)

@orderWeeks.route('/orderWeeks')
def getorderWeeks():
    try:
        orderInfos=[]
        # 获取表里最近10周的周数
        orderInfos = []
        week1 = db.session.query(Order_week_statistics.week).filter(Order_week_statistics.productType == '度假').filter(
            Order_week_statistics.isSuccess == 1).order_by((Order_week_statistics.week).desc()).limit(10).all()
        for i in range(len(week1)):
            # 获取最近10周度假产品下单成功的数量
            successCount_holiday1 = db.session.query(Order_week_statistics.count).filter(
                Order_week_statistics.productType == '度假').filter(Order_week_statistics.isSuccess == '1').filter(
                Order_week_statistics.week == week1[i][0]).all()
            #print(successCount_holiday1)
            successCount_holiday = successCount_holiday1[0][0]
            successCount_mall1 = db.session.query(Order_week_statistics.count).filter(
                Order_week_statistics.productType == '零售').filter(Order_week_statistics.isSuccess == '1').filter(
                Order_week_statistics.week == week1[i][0]).all()
            successCount_mall = successCount_mall1[0][0]
            #print(successCount_mall)

            data = {
                "week": week1[i][0],
                "productType": "度假",
                "successCount": successCount_holiday,
                "productType1": "零售",
                "successCount1": successCount_mall,

            }
            orderInfos.append(data)
            response = ({"success": "true", "msg": "OK", "data": {"orderInfos": orderInfos}})

    except Exception as e:
        raise e
        response = ({"success": "false", "msg": "操作失败～～"})
    response = json.dumps(response)
    return response




if __name__ == '__main__':

    # 获取表里最近10周的周数
    orderInfos=[]
    week1 = db.session.query(Order_week_statistics.week).filter(Order_week_statistics.productType == '度假').filter(Order_week_statistics.isSuccess == 1).order_by((Order_week_statistics.week).desc()).limit(10).all()
    for i in range(len(week1)):
        # 获取最近10周度假产品下单成功的数量
        successCount_holiday1 = db.session.query(Order_week_statistics.count).filter(
            Order_week_statistics.productType == '度假').filter(Order_week_statistics.isSuccess == '1').filter(
        Order_week_statistics.week == week1[i][0]).all()
        print (successCount_holiday1)
        successCount_holiday = successCount_holiday1[0][0]
        successCount_mall1 = db.session.query(Order_week_statistics.count).filter(
               Order_week_statistics.productType == '零售').filter(Order_week_statistics.isSuccess == '1').filter(
               Order_week_statistics.week == week1[i][0]).all()
        successCount_mall = successCount_mall1[0][0]
        print(successCount_mall)

        data = {
            "week": week1[i][0],
            "productType": "度假",
            "successCount": successCount_holiday,
            "productType1": "零售",
            "successCount1": successCount_mall,

        }
        orderInfos.append(data)
        response = ({"success": "true", "msg": "OK", "data":{"orderInfos":orderInfos}})

        print (response)



