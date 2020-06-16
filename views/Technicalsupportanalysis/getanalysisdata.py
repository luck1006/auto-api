#./user/bin/python
#coding=UTF_8
from app.models.models import *
from flask import Blueprint
from sqlalchemy import func, and_, desc
import json
import sys
from flask import current_app
import xlrd
from flask import Blueprint,request

# 设置蓝图
getanalysisdatas = Blueprint('getanalysisdatas', __name__)
@getanalysisdatas.route('/getanalysisdatas')
def getanalysisdata():
    data2 = []
    data3=[]
    try:
        dict = request.args
        if len(dict) >= 1:
           moduleids1 =request.args["module"]
           sytem=request.args["modulesystem"]
           #moduleids =request.form.get('module')
        #print(moduleids)
        print(moduleids1)
        #moduleidss=eval(moduleids)
        #moduleids='crm.任务管理'
        data1 = db.session.query(Support_sum.systemname,Support_sum.module_id,Support_sum.week,Support_sum.num).filter(and_(Support_sum.del_flag==0,Support_sum.module_id==moduleids1,Support_sum.systemname==sytem)).all()
        print(data1)
        dataxin1 = db.session.query(Support_sum.systemname,Support_sum.module_id,Support_sum.week,Support_sum.num).order_by(Support_sum.week.desc()).filter(Support_sum.systemname==sytem).filter(Support_sum.del_flag==0).all()
        for i in range(len(data1)):
           data={}
           data['systemname'] = data1[i][0]
           data["module_id"] =data1[i][1]
           data['week'] = data1[i][2]
           data["num"] = data1[i][3]
           data2.append(data)
        for i in range(len(dataxin1)):
           datan={}
           datan['systemname'] = dataxin1[i][0]
           datan["module_id"] =dataxin1[i][1]
           datan['week'] = dataxin1[i][2]
           datan["num"] = dataxin1[i][3]
           data3.append(datan)
        #print(data3)
        response = ({"success": "true", "msg": "OK", "data": {"dataall": data2,"datanew":data3}})
        #print(response)
    except Exception as e:
        raise e
        response = {"success": "false", "msg": "查询失败~~"}
    response = json.dumps(response)
    return response

# if __name__ == '__main__':
#    getanalysisdata()