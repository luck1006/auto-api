# -*- coding: utf-8 -*-
# TIME:         7.12
# Author:       huangfang
# Explain：     工时脚本跑数据入detail表

from app.models.models import *
from flask import Blueprint,request
from sqlalchemy import func, and_, desc
import json
from decimal import Decimal
import sys
from flask import current_app
import xlrd
from views.interfaceAuto.interface import cors_response

# 设置蓝图
timeworking = Blueprint('timeworking', __name__)
#通过周数查看资本化数据
@timeworking.route('/timeworking')
def gettimeworking():
    try:
        dict = request.args
        if len(dict) == 1:
            week = request.args["week"]
             # 获取部门信息
            #DepartmentInfo = []
            # 获取部门总人数
        totalnum1 = db.session.query(Time_working.totalnum).filter(Time_working.week == week).all()
        totalnum=totalnum1[0][0]
        #项目统计人数（总人数-休假人数，需要手工统计，这边统计-1）
        statisticsnum = totalnum-1
        #本期参与项目人数（默认等于项目统计人数）
        participationnum = statisticsnum
        #部门理论人天（部门总人数*5）
        theorytime = totalnum*5
        DepartmentInfo = {
            "totalnum": totalnum,
            "statisticsnum": statisticsnum,
            "participationnum": participationnum,
            "theorytime": theorytime
        }
        #获取项目工作量
        #ProjectInfo = []
        #项目总工时
        inlinetime1 = db.session.query(Time_working.projectTime).filter(Time_working.week == week).all()
        inlinetime=inlinetime1[0][0]
        #项目理论工时（项目统计人数*5）
        projecttheorytime = statisticsnum*5
        #项目人员利用率（（项目筹备人天+项目实际人天）/项目理论工时，目前项目筹备人天默认为0）
        #项目占比（（项目筹备人天+项目实际人天）/部门理论工时，目前项目筹备人天默认为0）
        ProjectInfo = {
            "inlinetime":  '%.2f' %inlinetime,
            "projecttheorytime": projecttheorytime,
            "utilization": "%.2f%%" % ((inlinetime/projecttheorytime)*100),
            "proportion": "%.2f%%" % ((inlinetime/theorytime)*100),
        }
        #获取资本化和技术支持的信息
        # RtsupportInfo = []
        #获取技术支持工时
        supporttime1 = db.session.query(Time_working.supportTime).filter(Time_working.week == week).all()
        supporttime = supporttime1[0][0]
        # 获取小需求工时（资本化工时=总工时-技术支持工时-项目工时）
        requiretime1 = db.session.query(Time_working.capitalizationTime).filter(Time_working.week == week).all()
        requiretime = requiretime1[0][0]

        # 需求人天占比（资本化工时/部门理论人天）
        #技术支持占比（技术支持人天/项目理论人天）
        RtsupportInfo = {
            "requiretime": '%.2f' %requiretime,
            "rproportion": "%.2f%%" % ((requiretime/theorytime)*100),
            "support": '%.2f' %supporttime,
            "sproportion": "%.2f%%" % ((supporttime/projecttheorytime)*100)
        }
        # 获取资本化各个模块数据
        # ModuleInfo = []
        # 获取零售工时
        lingshouTime1 = db.session.query(Time_working.lingshouTime).filter(Time_working.week == week).all()
        lingshouTime = lingshouTime1[0][0]
        # 获取度假转化工时
        zhuanhuaTime1 = db.session.query(Time_working.zhuanhuaTime).filter(Time_working.week == week).all()
        zhuanhuaTime = zhuanhuaTime1[0][0]
        # 获取新客转化工时
        xinkeTime1 = db.session.query(Time_working.xinkeTime).filter(Time_working.week == week).all()
        xinkeTime = xinkeTime1[0][0]
        # 获取老客运营工时
        yunyingTime1 = db.session.query(Time_working. yunyingTime).filter(Time_working.week == week).all()
        yunyingTime =  yunyingTime1[0][0]
        # 获取架构工时
        jiagouTime1 = db.session.query(Time_working.jiagouTime).filter(Time_working.week == week).all()
        jiagouTime = jiagouTime1[0][0]
        # 获取打包预定工时
        dabaoTime1 = db.session.query(Time_working.dabaoTime).filter(Time_working.week == week).all()
        dabaoTime = dabaoTime1[0][0]
        # 获取聚合转化工时
        juheTime1 = db.session.query(Time_working.juheTime).filter(Time_working.week == week).all()
        juheTime = juheTime1[0][0]
        # 获取会员工时
        huiyuanTime1 = db.session.query(Time_working.huiyuanTime).filter(Time_working.week == week).all()
        huiyuanTime = huiyuanTime1[0][0]
        # 获取供应链工时
        gongyinglianTime1 = db.session.query(Time_working.gongyinglianTime).filter(Time_working.week == week).all()
        gongyinglianTime = gongyinglianTime1[0][0]
        # 获取订单工时
        dingdanTime1 = db.session.query(Time_working.dingdanTime).filter(Time_working.week == week).all()
        dingdanTime = dingdanTime1[0][0]

        ModuleInfo = {
            "lingshouTime": lingshouTime,
            "zhuanhuaTime": zhuanhuaTime,
            "xinkeTime": xinkeTime,
            "yunyingTime": yunyingTime,
            "jiagouTime": jiagouTime,
            "dabaoTime": dabaoTime,
            "juheTime": juheTime,
            "huiyuanTime": huiyuanTime,
            "gongyinglianTime": gongyinglianTime,
            "dingdanTime": dingdanTime,

        }


        response = ({"success": "true", "msg": "OK", "data": {"week":week,"DepartmentInfo":DepartmentInfo,"ProjectInfo":ProjectInfo,"RtsupportInfo":RtsupportInfo,"ModuleInfo":ModuleInfo}})

    except Exception as e:
        raise e
        response = ({"success": "false", "msg": "操作失败～～"})
    #response = json.dumps(response)
    return cors_response(response)


'''if __name__ == '__main__':
    totalnum1 = db.session.query(Time_working.totalnum).filter(Time_working.week == '28w').all()
    totalnum = totalnum1[0][0]
    theorytime = totalnum * 5
    statisticsnum = totalnum - 1
    projecttheorytime = statisticsnum * 5

    supporttime1 = db.session.query(Time_working.supportTime).filter(Time_working.week == '28w').all()
    supporttime = supporttime1[0][0]
    # 获取小需求工时（资本化工时=总工时-技术支持工时-项目工时）
    requiretime1 = db.session.query(Time_working.capitalizationTime).filter(Time_working.week == '28w').all()
    requiretime = requiretime1[0][0]

    # 需求人天占比（资本化工时/部门理论人天）
    # 技术支持占比（技术支持人天/项目理论人天）
    RtsupportInfo = {
        "requiretime": '%.2f' % requiretime,
        "rproportion": "%.2f%%" % ((requiretime / theorytime) * 100),
        "support": '%.2f' % supporttime,
        "sproportion": "%.2f%%" % ((supporttime/ projecttheorytime) * 100)
    }
    print(RtsupportInfo)'''







