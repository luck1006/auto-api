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
orderLoginReport = Blueprint('orderLoginReport', __name__)

@orderLoginReport.route('/orderLoginReport')
def getorderLoginReport():
    try:
        # 获取表里最近10周下单和会员登录的数据
        orderInfos = []
        week = db.session.query(Order_week_statistics.week).filter(Order_week_statistics.productType == '度假').filter(
            Order_week_statistics.isSuccess == 1).order_by((Order_week_statistics.year).desc(),(Order_week_statistics.week).desc()).limit(10).all()
        week1 = list(reversed(week))
        #print(week1)

        for i in range(len(week1)):
            # 获取最近10周下单成功的数量
            successCount_holiday1 = db.session.query(Order_week_statistics.count).filter(
                Order_week_statistics.productType == '度假').filter(Order_week_statistics.isSuccess == '1').filter(
                Order_week_statistics.week == week1[i][0]).all()
            successCount_holiday = successCount_holiday1[0][0]
            #print(successCount_holiday)
            successCount_mall1 = db.session.query(Order_week_statistics.count).filter(
                Order_week_statistics.productType == '零售').filter(Order_week_statistics.isSuccess == '1').filter(
                Order_week_statistics.week == week1[i][0]).all()
            successCount_mall = successCount_mall1[0][0]
            #print(successCount_mall)
            ## 获取最近10周下单失败的数量
            failCount_holiday1 = db.session.query(Order_week_statistics.count).filter(
                Order_week_statistics.productType == '度假').filter(Order_week_statistics.isSuccess == '0').filter(
                Order_week_statistics.week == week1[i][0]).all()
            #print(failCount_holiday1)
            failCount_holiday = failCount_holiday1[0][0]
            failCount_mall1 = db.session.query(Order_week_statistics.count).filter(
                Order_week_statistics.productType == '零售').filter(Order_week_statistics.isSuccess == '0').filter(
                Order_week_statistics.week == week1[i][0]).all()
            failCount_mall = failCount_mall1[0][0]
            #print(failCount_mall)
            ## 获取最近10周会员登录成功的数量
            loginsuccess1 = db.session.query(Order_week_statistics.count).filter(
                Order_week_statistics.productType == '登录').filter(Order_week_statistics.isSuccess == '1').filter(
                Order_week_statistics.week == week1[i][0]).all()
            #print(loginsuccess1)
            loginsuccess = loginsuccess1[0][0]
            loginfail1 = db.session.query(Order_week_statistics.count).filter(
                Order_week_statistics.productType == '登录').filter(Order_week_statistics.isSuccess == '0').filter(
                Order_week_statistics.week == week1[i][0]).all()
            loginfail = loginfail1[0][0]
            #print(loginfail)

            if (failCount_holiday+successCount_holiday) == 0:
                holidayfailurerate = 0
            else:
                holidayfailurerate = (failCount_holiday/(failCount_holiday+successCount_holiday))*100

            if (failCount_mall+successCount_mall) == 0:
                mallfailureRate = 0
            else:
                mallfailureRate = (failCount_mall/(failCount_mall+successCount_mall))*100

            data = {
                "week": week1[i][0],
                "holidayordersuccess": successCount_holiday,
                "mallordersuccess": successCount_mall,
                "holidayorderfailure": failCount_holiday,
                "mallorderfailure": failCount_mall,
                # "holidayfailurerate": '%.2f' % ((failCount_holiday/(failCount_holiday+successCount_holiday))*100),
                "holidayfailurerate": '%.2f' % holidayfailurerate,
                "mallfailurerate": '%.2f' % mallfailureRate,
                "loginsuccess": loginsuccess,
                "loginfailure": loginfail,

            }
            orderInfos.append(data)
        # 获取最新一周下单渠道分布数据
        ternimalInfos = []
        terminal = db.session.query(Order_success_terminal.terminal).filter(
            Order_success_terminal.productType == '度假').all()
        print(terminal)
        for j in range(len(terminal)):
            # 获取度假pc渠道下单数据
            holiday1 = db.session.query(Order_success_terminal.orderCount).filter(
                Order_success_terminal.productType == '度假').filter(
                Order_success_terminal.terminal == terminal[j][0]).all()
            holiday = holiday1[0][0]
            mall1 = db.session.query(Order_success_terminal.orderCount).filter(
                Order_success_terminal.productType == '零售').filter(
                Order_success_terminal.terminal == terminal[j][0]).all()
            mall = mall1[0][0]
            #print (mall)
            data = {
                "terminaltype": terminal[j][0],
                "holiday": holiday,
                "mall": mall
            }
            ternimalInfos.append(data)
        #获取最近一周登录失败原因
        loginre = []
        count = db.session.query(Order_failuer_statistics).filter(
            Order_failuer_statistics.failMsg == 'hiveTJlogin').filter(
            Order_failuer_statistics.productType != 0).count()
        for l in range(count):
            failcode = db.session.query(Order_failuer_statistics.productType).filter(
                Order_failuer_statistics.failMsg == 'hiveTJlogin').filter(
                Order_failuer_statistics.productType != 0).order_by(Order_failuer_statistics.orderCount.desc()).all()
            failcode1 = failcode[l][0]
            #print(failcode1)
            if (failcode1 == '1'):
                failreason = '用户名不存在'
            elif (failcode1 == '2'):
                failreason = '当日登录超过限制'
            elif (failcode1 == '3'):
                failreason = '密码错误'
            else:
                failreason = '验证码错误'
            failnum = db.session.query(Order_failuer_statistics.orderCount).filter(
                Order_failuer_statistics.failMsg == 'hiveTJlogin').filter(
                Order_failuer_statistics.productType != 0).order_by(
                Order_failuer_statistics.orderCount.desc()).all()

            data = {
                "failcode": failcode[l][0],
                "failreason": failreason,
                "failnum": failnum[l][0]
            }
            loginre.append(data)
        #获取最近一周零售下单失败原因
        mallre=[]
        count=db.session.query(Order_failuer_statistics).filter(
            Order_failuer_statistics.productType == '零售').filter(
            Order_failuer_statistics.isSuccess == 0).count()
        for k in range(count):
            failreason = db.session.query(Order_failuer_statistics.failMsg).filter(
                Order_failuer_statistics.productType == '零售').filter(
                Order_failuer_statistics.isSuccess == 0).order_by(Order_failuer_statistics.orderCount.desc()).all()
            # print (failreason[k][0])
            failnum = db.session.query(Order_failuer_statistics.orderCount).filter(
                Order_failuer_statistics.productType == '零售').filter(
                Order_failuer_statistics.isSuccess == 0).order_by(Order_failuer_statistics.orderCount.desc()).all()
            data = {
                "producttype": '零售',
                "failreason": failreason[k][0],
                "failnum": failnum[k][0]
            }
            mallre.append(data)
        #获取最近一周度假下单失败原因
        holidayre = []
        count = db.session.query(Order_failuer_statistics).filter(
            Order_failuer_statistics.productType.in_(('boss3门票', '自由行', 'ngboss门票'))).filter(
            Order_failuer_statistics.isSuccess == 0).count()
        for m in range(count):
            producttype=db.session.query(Order_failuer_statistics.productType).filter(
            Order_failuer_statistics.productType.in_(('boss3门票', '自由行', 'ngboss门票'))).filter(
                Order_failuer_statistics.isSuccess == 0).order_by(Order_failuer_statistics.orderCount.desc()).all()
            failreason = db.session.query(Order_failuer_statistics.failMsg).filter(
            Order_failuer_statistics.productType.in_(('boss3门票', '自由行', 'ngboss门票'))).filter(
                Order_failuer_statistics.isSuccess == 0).order_by(Order_failuer_statistics.orderCount.desc()).all()
            # print (failreason[k][0])
            failnum = db.session.query(Order_failuer_statistics.orderCount).filter(
            Order_failuer_statistics.productType.in_(('boss3门票', '自由行', 'ngboss门票'))).filter(
                Order_failuer_statistics.isSuccess == 0).order_by(Order_failuer_statistics.orderCount.desc()).all()
            data = {
                "producttype": producttype[m][0],
                "failreason": failreason[m][0],
                "failnum": failnum[m][0]
            }
            holidayre.append(data)
        #获取最近一周度假子品类下单成功数量
        holidaysub = []
        count = db.session.query(Order_failuer_statistics).filter(
            Order_failuer_statistics.failMsg=='hiveTJ').count()
        for n in range(count):
            producttype = db.session.query(Order_failuer_statistics.productType).filter(
                Order_failuer_statistics.failMsg=='hiveTJ').order_by(Order_failuer_statistics.orderCount.desc()).all()
            successnum = db.session.query(Order_failuer_statistics.orderCount).filter(
                Order_failuer_statistics.failMsg=='hiveTJ').order_by(Order_failuer_statistics.orderCount.desc()).all()
            data = {
                "producttype": producttype[n][0],
                "successnum": successnum[n][0]
            }
            holidaysub.append(data)
        response = ({"success": "true", "msg": "OK",
                     "data": [{"name": '下单和登录数据', "data": orderInfos}, {"name": '下单终端统计', "data": ternimalInfos},
                              {"name": '登录失败原因', "data": loginre}, {"name": '零售下单失败原因', "data": mallre},
                              {"name": '度假下单失败原因', "data": holidayre}, {"name": '度假子品类下单成功', "data": holidaysub}]})

    except Exception as e:
        raise e
        response = ({"success": "false", "msg": "操作失败～～"})
    response = json.dumps(response)
    return response




#if __name__ == '__main__':

