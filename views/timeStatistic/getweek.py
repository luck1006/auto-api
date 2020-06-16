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
getweek = Blueprint('getweek', __name__)
@getweek.route('/getweek')
def getgetweek():
    #读取资本化数据信息周数
    weekInfos = []
    try:
        # 获取资本化数据最近10周数据
        week = db.session.query(Time_working.week).order_by(Time_working.year.desc(),Time_working.week.desc()).limit(10).all()
        week1 = list(reversed(week))
        for i in range(len(week)):
            data = {
                "week": week[i][0],
            }
            weekInfos.append(data)
        response = ({"success": "true", "msg": "OK", "data": {"week": weekInfos}})
    except Exception as e:
        raise e
        response = {"success": "false", "msg": "查询失败~~"}
    response = json.dumps(response)
    return response

'''if __name__ == '__main__':
    weekInfos = []
    week = db.session.query(Time_working.week).order_by(Time_working.week.desc()).limit(10).all()
    week1 = list(reversed(week))
    for i in range(len(week)):
        data = {
            "week": week[i][0],
        }
        weekInfos.append(data)
    response = ({"success": "true", "msg": "OK", "data": {"week": weekInfos}})

    print("week======",response)
    #print("week1======", week1)'''


