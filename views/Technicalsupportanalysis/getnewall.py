#./user/bin/python
#coding=UTF_8
from app.models.models import *
from flask import Blueprint
from sqlalchemy import func, and_, desc
from sqlalchemy.sql import func
import json
import sys
from flask import current_app
import xlrd
from views.interfaceAuto.interface import cors_response
from flask import Blueprint,request
# 设置蓝图
getnewallnum = Blueprint('getnewallnum', __name__)
@getnewallnum.route('/getnewallnum')
def getnewall():
    data1 = []

    try:
        dict = request.args
        if len(dict) >= 1:
           systmmodule =request.args["modulesystem"]
        newweek=db.session.query(func.max(Support_sum.week)).scalar()
        dataall = db.session.query(func.sum(Support_sum.num)).filter(Support_sum.week==newweek).filter(Support_sum.systemname==systmmodule).filter(Support_sum.del_flag==0).limit(14).all()
        dataxin = db.session.query(Support_sum.systemname,Support_sum.module_id,Support_sum.week,Support_sum.num).filter(Support_sum.week==newweek).filter(Support_sum.systemname==systmmodule).filter(Support_sum.del_flag==0).all()
        #临时解决数
        datacpletea =db.session.query(func.sum(Support_completely_sum.num)).filter(and_(Support_completely_sum.systemname==systmmodule,Support_completely_sum.del_flag==0,Support_completely_sum.week==newweek,Support_completely_sum.completely==0)).scalar()
       #根本解决数
        datacpleteb =db.session.query(func.sum(Support_completely_sum.num)).filter(and_(Support_completely_sum.systemname==systmmodule,Support_completely_sum.del_flag==0,Support_completely_sum.week==newweek,Support_completely_sum.completely==1)).scalar()
        #0代表系统默认值
        datatypea =db.session.query(func.sum(Support_types_sum.num)).filter(and_(Support_types_sum.systemname==systmmodule,Support_types_sum.del_flag==0,Support_types_sum.week==newweek,Support_types_sum.types==0)).scalar()
        #1代表IT类
        datatypeb =db.session.query(func.sum(Support_types_sum.num)).filter(and_(Support_types_sum.systemname==systmmodule,Support_types_sum.del_flag==0,Support_types_sum.week==newweek,Support_types_sum.types==1)).scalar()
        #2代表无效问题
        datatypec =db.session.query(func.sum(Support_types_sum.num)).filter(and_(Support_types_sum.systemname==systmmodule,Support_types_sum.del_flag==0,Support_types_sum.week==newweek,Support_types_sum.types==2)).scalar()
        #3代表环境问题
        datatyped =db.session.query(func.sum(Support_types_sum.num)).filter(and_(Support_types_sum.systemname==systmmodule,Support_types_sum.del_flag==0,Support_types_sum.week==newweek,Support_types_sum.types==3)).scalar()
        #4代表用户类问题
        datatypee =db.session.query(func.sum(Support_types_sum.num)).filter(and_(Support_types_sum.systemname==systmmodule,Support_types_sum.del_flag==0,Support_types_sum.week==newweek,Support_types_sum.types==4)).scalar()
        #5代表系统不支持
        datatypef =db.session.query(func.sum(Support_types_sum.num)).filter(and_(Support_types_sum.systemname==systmmodule,Support_types_sum.del_flag==0,Support_types_sum.week==newweek,Support_types_sum.types==5)).scalar()
        #6代表系统故障
        datatypeg =db.session.query(func.sum(Support_types_sum.num)).filter(and_(Support_types_sum.systemname==systmmodule,Support_types_sum.del_flag==0,Support_types_sum.week==newweek,Support_types_sum.types==6)).scalar()
        #取出总数，且需要用to_eng_string()转化一下才可以放入接口
        allnum=dataall[0][0].to_eng_string()
        cplete0=datacpletea.to_eng_string()
        cplete1=datacpleteb.to_eng_string()
        datatype0=datatypea.to_eng_string()
        datatype1=datatypeb.to_eng_string()
        datatype2=datatypec.to_eng_string()
        datatype3=datatyped.to_eng_string()
        datatype4=datatypee.to_eng_string()
        datatype5=datatypef.to_eng_string()
        datatype6=datatypeg.to_eng_string()
        print(allnum,datacpletea,cplete0)
        for i in range(len(dataxin)):
            data ={}
            data["module_id"] =dataxin[i][1]
            data["num"] = dataxin[i][3]
            data["week"] = dataxin[i][2]
            data1.append(data)
        data2=[{"cplete0":cplete0},{"cplete1":cplete1}]
        data3=[{"datatype0":datatype0},{"datatype1":datatype1},{"datatype2":datatype2},{"datatype3":datatype3},{"datatype4":datatype4},{"datatype5":datatype5},{"datatype6":datatype6}]
        response = ({"success": "true", "msg": "OK", "data":{"allnum": allnum,"modeleall":data1,"cplete":data2,"types":data3}})
        print(response)
    except Exception as e:
        raise e
        response = {"success": "false", "msg": "查询失败~~"}
    response = json.dumps(response)
    return response

# if __name__ == '__main__':
#     getnewall()