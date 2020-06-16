#./user/bin/python
#coding=UTF_8
from app.models.models import *
from flask import Blueprint
from sqlalchemy import func, and_, desc
import json
import sys
from flask import current_app
import xlrd
from views.interfaceAuto.interface import cors_response
from flask import Blueprint,request
# 设置蓝图
getanalysiscpletes = Blueprint('getanalysiscplete', __name__)
@getanalysiscpletes.route('/getanalysiscplete')
def getanalysiscplete():
    data2 = []
    try:
        dict = request.args
        if len(dict) >= 1:
           moduleids = request.args["module"]
           sytem=request.args["modulesystem"]
        # print(moduleids)
        #moduleids='crm.任务管理'
        #直接表名查询，结果只是数据的指针，而非数据本身，所以下方难以赋值
       # data1 = Support_completely_sum.query.filter(and_(Support_completely_sum.systemname=='crm系统',Support_completely_sum.del_flag==0,Support_completely_sum.module_id==moduleids)).all()
        data1 = db.session.query(Support_completely_sum.systemname,Support_completely_sum.module_id,Support_completely_sum.week,Support_completely_sum.completely,Support_completely_sum.num).filter(and_(Support_completely_sum.del_flag==0,Support_completely_sum.module_id==moduleids,Support_completely_sum.systemname==sytem)).all()
       #用多个filter查询会导致数据不正确
       # data1 = db.session.query(Support_completely_sum.systemname,Support_completely_sum.module_id,Support_completely_sum.week,Support_completely_sum.completely,Support_completely_sum.num).filter(Support_sum.module_id=='crm.任务管理').filter(Support_sum.del_flag==0).all()
        #0代表临时解决，1代表根本解决
        #print(data1)
        completely=[0,1]
        for c in completely:
            h=[]
            s={}
            for i in range(len(data1)):
               if( c==data1[i][3]):
                 data={}
                 data['systemname'] = data1[i][0]
                 #data["module_id"] =data1[i][1]
                 data['week'] = data1[i][2]
                 data["num"] = data1[i][4]
                 h.append(data)
            s['completely']=c
            s['module']=moduleids
            s['data']=h
            data2.append(s)
        response = ({"success": "true", "msg": "OK", "data":data2})
       # print(response)
    except Exception as e:
        raise e
        response = {"success": "false", "msg": "查询失败~~"}
    response = json.dumps(response)
    return response
#
# if __name__ == '__main__':
#       getanalysiscplete()