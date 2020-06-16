#./user/bin/python
#coding=UTF_8

#使用这个文件，其他弃用 2019-11-19
from app.models.models import *
from sqlalchemy import func, and_, desc
import json
from flask import Blueprint,request

# 设置蓝图
modulegetty = Blueprint('modulegetty', __name__)
@modulegetty.route('/getty')
def getty():
    data2 = []
    try:
        dict = request.args
        if len(dict)>= 1:
           systemname=request.args["systemname"]
           detailsystem = request.args["detailsystem"]
        #0代表系统默认值，1代表IT类，2代表无效问题，3代表环境问题，4代表用户类问题，5代表系统不支持，6代表系统故障
        t={'0':"系统默认值","1":"IT类","2":"无效问题","3":"环境问题","4":"用户类问题","5":"系统不支持","6":"系统故障"}
        data1 = db.session.query(Support_types_sum.systemname,Support_types_sum.detailsystem,Support_types_sum.week,Support_types_sum.types,Support_types_sum.num).filter(and_(Support_types_sum.del_flag==0,Support_types_sum.systemname==systemname,Support_types_sum.detailsystem==detailsystem)).order_by(Support_types_sum.year,Support_types_sum.week).all()
        for k,v in t.items():
            h=[]
            s={}
            for i in range(len(data1)):
                 if( int(k)==data1[i][3]):
                   data={}
                   #data['detailsystem'] = data1[i][1]
                   data['week'] = str(data1[i][2])+'W'
                   data["num"] = data1[i][4]
                   h.append(data)
            s['types']=int(k)
            s['typesname']=v
            s['detailsystem'] = detailsystem
            s['data']=h
            data2.append(s)
        response = ({"success": "true", "msg": "OK","systemname":systemname, "data":data2})
    except Exception as e:
        raise e
        response = {"success": "false", "msg": "查询失败~~"}
    response = json.dumps(response)
    return response


#提供给前端，最近一周
gettynew = Blueprint('gettynew', __name__)
@gettynew.route('/gettynew')
def getty():
    data2 = []
    try:
        dict = request.args
        if len(dict)>= 1:
           systemname=request.args["systemname"]
           detailsystem = request.args["detailsystem"]
        #0代表系统默认值，1代表IT类，2代表无效问题，3代表环境问题，4代表用户类问题，5代表系统不支持，6代表系统故障
        t={'0':"系统默认值","1":"IT类","2":"无效问题","3":"环境问题","4":"用户类问题","5":"系统不支持","6":"系统故障"}
        week = db.session.query(Support_types_sum.week).filter(Support_types_sum.del_flag==0).group_by(Support_types_sum.year,Support_types_sum.week).order_by(Support_types_sum.year.desc(),Support_types_sum.week.desc()).first()
        print('week1',week)
        data1 = db.session.query(Support_types_sum.systemname,Support_types_sum.detailsystem,Support_types_sum.week,Support_types_sum.types,Support_types_sum.num).filter(and_(Support_types_sum.del_flag==0,Support_types_sum.systemname==systemname,Support_types_sum.detailsystem==detailsystem,Support_types_sum.week==int(week[0]))).all()
        print("data1+++++",data1)
        for k,v in t.items():
            h=[]
            s={}
            for i in range(len(data1)):
                 if( int(k)==data1[i][3]):
                   data={}
                   data['detailsystem'] = data1[i][1]
                   data['week'] = str(data1[i][2])+'W'
                   data["num"] = data1[i][4]
                   h.append(data)
            s['types']=k
            s['typesname']=v
            s['data']=h
            data2.append(s)
        response = ({"success": "true", "msg": "OK", "systemname":systemname,"data":data2})
    except Exception as e:
        raise e
        response = {"success": "false", "msg": "查询失败~~"}
    response = json.dumps(response)
    return response



#各系统全部数据接口，types=7
gettyall = Blueprint('gettyall', __name__)
@gettyall.route('/gettyall')
def getty():
    data2 = []
    try:
        dict = request.args
        if len(dict)>= 1:
           systemname=request.args["systemname"]
           detailsystem = request.args["detailsystem"]
           print("systemname+++++", systemname)
           print("detailsystem+++++", detailsystem)
        week = db.session.query(Support_types_sum.week).filter(Support_types_sum.del_flag==0).group_by(Support_types_sum.year,Support_types_sum.week).order_by(Support_types_sum.year.desc(),Support_types_sum.week.desc()).first()
        print('week2',week)
        if(detailsystem=="全部"):
            data1 = db.session.query(Support_types_sum.systemname,Support_types_sum.detailsystem,Support_types_sum.week,Support_types_sum.types,Support_types_sum.num).filter(and_(Support_types_sum.del_flag==0,Support_types_sum.systemname==systemname,Support_types_sum.detailsystem !="全部",Support_types_sum.types==7,Support_types_sum.week==int(week[0]))).all()
            print("gettyall",data1)
            h=[]
            s={}
            for i in range(len(data1)):
               data={}
               data['detailsystem'] = data1[i][1]
               data['week'] = str(data1[i][2])+'W'
               data["num"] = data1[i][4]
               h.append(data)
            s['types']=7
            s['data']=h
            data2.append(s)
            response = ({"success": "true", "msg": "OK", "data":data2})
        else:
            data1 = db.session.query(Support_types_sum.systemname, Support_types_sum.detailsystem,
                                     Support_types_sum.week, Support_types_sum.types, Support_types_sum.num).filter(
                and_(Support_types_sum.del_flag == 0, Support_types_sum.systemname == systemname,Support_types_sum.detailsystem==detailsystem,
                     Support_types_sum.types == 7,Support_types_sum.week == int(week[0]))).all()
            print("gettyallelse", data1)
            h = []
            s = {}
            for i in range(len(data1)):
                data = {}
                data['detailsystem'] = data1[i][1]
                data['week'] = str(data1[i][2]) + 'W'
                data["num"] = data1[i][4]
                h.append(data)
            s['types'] = 7
            s['data'] = h
            data2.append(s)
            response = ({"success": "true", "msg": "OK", "data": data2})
    except Exception as e:
        raise e
        response = {"success": "false", "msg": "查询失败~~"}
    response = json.dumps(response)
    return response
