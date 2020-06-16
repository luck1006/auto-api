# -*- coding: utf-8 -*-
# TIME:         7.27
# Author:       zhangwen3
# Explain：     保存前台填写的技术支持分析


import datetime
from jira import JIRA
import json
from app.models.models import *
from flask import Blueprint,request
import re
from flask import Flask

#蓝图，注册到app
analysis = Blueprint('analysis', __name__,)
#路由，具体业务接口
@analysis.route('/saveAnalysis',methods=['GET','POST'])
def saveTechnicalAnalysis():
    content = request.get_json().get('content')
    #content = '一、40W新增技术支持量分析测试测试测：'
    if content != "" and content is not None:
        #截取分析中的周
        s=(re.compile('[0-9]+')).findall(content[:10])
        if s not in ([],None):
            week = db.session.query(Technical_Analysis.week).group_by(Technical_Analysis.year,Technical_Analysis.week).all()
            s1 = []
            for i in week:
                s1.append(i[0])
            print('s1',s1)
            s2=int(s[0])
            print('s2',s2)
            if s2 not in s1:
                content_list = []
                data = {"week": s2, "content": content}
                content_list.append(data)
                print(content_list)
                try:
                    # 填写的周数据库里还没有，插入一条新数据
                    db.session.execute(Technical_Analysis.__table__.insert(), content_list)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    return json.dumps({"success": "false", "msg": str(e)})
                else:
                    return json.dumps({"success": "true", "msg": "ok"})
            elif s2 in s1:
                content_list = []
                data = {"week": s2, "content": content}
                content_list.append(data)
                try:
                    # 填写的周，数据库中已存在，先把旧数据置为无效
                    db.session.query(Technical_Analysis.id).filter(Technical_Analysis.year==int(datetime.datetime.now().year)).filter(Technical_Analysis.week == s2).filter(
                        Technical_Analysis.del_flag == 0).update({"del_flag": 1})
                    # 再插入一条新数据
                    db.session.execute(Technical_Analysis.__table__.insert(), content_list)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    return json.dumps({"success": "false", "msg": str(e)})
                else:
                    return json.dumps({"success": "true", "msg": "ok"})
            else:
                return json.dumps({"success": "false", "msg": "输入不规范！"}, ensure_ascii=False)
        else:
            return json.dumps({"success": "false", "msg": "输入不规范，标题加上时间周"}, ensure_ascii=False)
        

    else:
        return json.dumps({"success":"false","msg":"入参不能为空！"},ensure_ascii=False)





#路由，具体业务接口
@analysis.route('/getAnalysis')
def getTechnicalAnalysis():
    try:
        result=db.session.query(Technical_Analysis.content,Technical_Analysis.week).filter(Technical_Analysis.del_flag==0).order_by(Technical_Analysis.year.desc(),Technical_Analysis.week.desc()).all()
        context_list = []
        for i in result:
            context_data = {}
            context_data["content"] = i[0]
            context_data["week"] = str(i[1]) + 'W'
            context_list.append(context_data)
        response = {"success": "true", "msg": "ok", "data": context_list}
    except Exception as e:
        raise e
        response = {"success": "false", "msg": "查询失败~~"}
    response = json.dumps(response, ensure_ascii=False)
    return response

#获取周数
@analysis.route('/getdate')
def getDate():
    try:
        result=db.session.query(Technical_Analysis.week).filter(Technical_Analysis.del_flag==0).order_by(Technical_Analysis.week.desc()).all()
        context_list = []
        for i in result:
            context_data = {}
            context_data["content"] = i[0]
            context_data["week"] = str(i[1]) + 'W'
            context_list.append(context_data)
        response = {"success": "true", "msg": "ok", "data": context_list}
    except Exception as e:
        raise e
        response = {"success": "false", "msg": "查询失败~~"}
    response = json.dumps(response, ensure_ascii=False)
    return response




if __name__ == '__main__':
    getTechnicalAnalysis()





