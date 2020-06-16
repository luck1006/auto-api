# -*- coding: utf-8 -*-
# TIME:         7.27
# Author:       huanfang
# Explain：     保存前台填写的下单和登录报表


import datetime
from jira import JIRA
import json
from app.models.models import *
from flask import Blueprint,request
from flask import Flask

#蓝图，注册到app
reportanalysis = Blueprint('reportanalysis', __name__,)
#路由，具体业务接口
@reportanalysis.route('/saveReportAnalysis',methods=['GET','POST'])
def saveReportAnalysis():
    content = request.get_json().get('content')


    #content = '下单数据分析'
    if content != "" and content is not None:
        content_list=[]

        data={"content":content}
        content_list.append(data)
        try:
            db.session.query(Report_Analysis.id).filter(Report_Analysis.del_flag==0).update({"del_flag":1})
            db.session.execute(Report_Analysis.__table__.insert(), content_list)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return json.dumps({"success":"false","msg":str(e)})
        else:
            return json.dumps({"success":"true","msg":"ok"})
    else:
        return json.dumps({"success":"false","msg":"入参不能为空！"},ensure_ascii=False)





#路由，具体业务接口
@reportanalysis.route('/getReportAnalysis')
def getReportAnalysis():
    try:
        result=db.session.query(Report_Analysis.content).filter(Report_Analysis.del_flag==0).first()
        context_list=[]
        context_data={}
        context_data["content"]=result[0]
        context_list.append(context_data)
        response = {"success": "true", "msg": "ok", "data": context_list}
    except Exception as e:
        raise e
        response = {"success": "false", "msg": "查询失败~~"}
    response = json.dumps(response, ensure_ascii=False)
    return response





