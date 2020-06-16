# -*- coding: utf-8 -*-
# TIME:         6.25
# Author:       huangfang
# Explain：     获取资本化信息

from app.models.models import *
from flask import Blueprint
from sqlalchemy import func, and_, desc
import json
import sys
from flask import current_app
import xlrd



# 设置蓝图
timeStatistic = Blueprint('timeStatistic', __name__)
@timeStatistic.route('/timeStatistic')
def gettimeStatistic():
    #读取资本化数据信息
    infos = []
    try:
        # 获取资本化数据最近10周数据
        workingtimeInfos = []
        week = db.session.query(Time_working.week).order_by(Time_working.year.desc(),Time_working.week.desc()).limit(10).all()
        week1 = week.reverse()
        for i in range(len(week)):
         #资本化工时
         capitalizationTime=db.session.query(Time_working.capitalizationTime).filter(Time_working.week == week[i][0]).all()
         #项目工时
         projectTime=db.session.query(Time_working.projectTime).filter(Time_working.week == week[i][0]).all()
         #技术支持工时
         supportTime = db.session.query(Time_working.supportTime).filter(Time_working.week == week[i][0]).all()
         #理论工时
         theoreticalTime = db.session.query(Time_working.theoreticalTime).filter(Time_working.week == week[i][0]).all()
         data = {
                    "week": week[i][0],
                    "capitalizationTime":capitalizationTime[0][0],
                    "projectTime":projectTime[0][0],
                    "supportTime":supportTime[0][0],
                    "theoreticalTime":theoreticalTime[0][0]
                   }
         workingtimeInfos.append(data)
        response = ({"success": "true", "msg": "OK", "data":{"workingTime": workingtimeInfos}})
    except Exception as e:
        raise e
        response = {"success": "false", "msg": "查询失败~~"}
    response = json.dumps(response)
    return response

'''if __name__ == '__main__':
    week = db.session.query(Time_working.week).order_by(Time_working.week.desc()).limit(10).all()
    #week1 = list(reversed(week))


    print("week======",week)
    #print("week1======", week1)'''


