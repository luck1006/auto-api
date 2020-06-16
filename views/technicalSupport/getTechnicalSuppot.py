# -*- coding: utf-8 -*-
# TIME:         6.27
# Author:       zhangwen3
# Explain：     获取每周技术支持数量

from app.models.models import *
from flask import Blueprint,request
from sqlalchemy import func, and_, desc
import json
from app.actions.tools.queryFromSql import  queryFromSql
import datetime
import time

import sys
from flask import current_app


# 设置蓝图
technicalSupport = Blueprint('technicalSupport', __name__)
@technicalSupport.route('/technicalSupport')
def getTechnicalSupport():
    try:
        result = db.session.query(Technical_Support.name,Technical_Support.week,Technical_Support.newnum,Technical_Support.closenum,Technical_Support.unsolvednum,Technical_Support.hisunsolvednum).filter(Technical_Support.name.in_(['order','supplychain','ticket','member','market','confirm'])).filter(Technical_Support.del_flag==0).all()
        t={'ticket':'门票','member':'会员','market':'营销','order':'订单','supplychain':'供应链','confirm':'确认管理'}
        data_list=[]
        for k,v in t.items():
            b=[]
            s={}
            for j in result:
                if(j[0]==k):
                    a={}
                    a['week']=str(j[1])+'W'
                    a['newnum']=j[2]
                    a['closenum']=j[3]
                    a['unsolvednum']=j[4]
                    a['hisunsolvednum']=j[5]
                    b.append(a)
                    s['code']=k
                    s['name']=v
                    s['data']=b
            data_list.append(s)
        data_list.append(getHisunsolvednum())
        response = {"success":"true","msg":"ok","data":data_list}
    except Exception as e:
        raise e
        response = {"success": "false", "msg": "查询失败~~"}
    response = json.dumps(response,ensure_ascii=False)
    return response


def getHisunsolvednum():
    weeks = db.session.query(Technical_Support.week).filter(Technical_Support.name.in_(['order','supplychain','ticket','member','market','confirm'])).filter(Technical_Support.del_flag==0).group_by(Technical_Support.year,Technical_Support.week).order_by(Technical_Support.year,Technical_Support.week).all()
    data_list = []
    for i in weeks:
        num = db.session.query(Technical_Support.hisunsolvednum).filter(Technical_Support.week == i[0]).filter(Technical_Support.name.in_(['order','supplychain','ticket','member','market','confirm'])).filter(Technical_Support.del_flag==0).all()
        a={}
        result = 0
        for j in num:
            result = result + int(j[0])
        a['week'] = str(i[0])+'W'
        a['hisunsolved'] = result
        data_list.append(a)
    hisnum = {"code":"hisnum","name":"历史未解决总数","data":data_list}
    return hisnum


# 获取解决率
resolutionRate = Blueprint('resolutionRate', __name__)
@resolutionRate.route('/resolutionRate')
def getResolutionRate():
    dict = request.args
    #dict = {'cs': 'month'}
    if len(dict) == 1:
        #list(dict.values())[0]
        #list(dict.to_dict().values())[0] == 'week':
        if list(dict.to_dict().values())[0] == 'week':
            try:
                result = db.session.query(Technical_Support.name,Technical_Support.week,Technical_Support.resolutionrate).filter(Technical_Support.name=='all').filter(Technical_Support.del_flag==0).order_by(Technical_Support.year,Technical_Support.week).all()
                b=[]
                for j in result:
                    a={}
                    a['time']=str(j[1])+'W'
                    if j[2] is not None:
                        a['resolutionrate']=j[2]
                    else:
                        a['resolutionrate']=0
                    b.append(a)
                response = {"success": "true", "msg": "ok", "data": b}
            except Exception as e:
                raise e
                response = {"success": "false", "msg": "查询失败~~"}
            return json.dumps(response, ensure_ascii=False)
        elif list(dict.to_dict().values())[0] == 'month':
            try:
                result = db.session.query(Technical_MonthSupport.name, Technical_MonthSupport.month,Technical_MonthSupport.resolutionrate).filter(Technical_MonthSupport.name=='all').filter(Technical_MonthSupport.del_flag == 0).order_by(Technical_MonthSupport.year,Technical_MonthSupport.month).all()
                b = []
                for j in result:
                    a = {}
                    a['time'] = str(j[1])+'M'
                    if j[2] is not None:
                        a['resolutionrate'] =j[2]
                    else:
                        a['resolutionrate'] = 0
                    b.append(a)
                response = {"success": "true", "msg": "ok", "data": b}
            except Exception as e:
                raise e
                response = {"success": "false", "msg": "查询失败~~"}
            return json.dumps(response, ensure_ascii=False)
        elif list(dict.to_dict().values())[0] == 'quarter':
            try:
                result = db.session.query(Technical_QuarterSupport.name, Technical_QuarterSupport.quarter,Technical_QuarterSupport.resolutionrate).filter(Technical_QuarterSupport.name=='all').filter(Technical_QuarterSupport.del_flag == 0).order_by(Technical_QuarterSupport.year,Technical_QuarterSupport.quarter).all()
                b = []
                for j in result:
                    a = {}
                    a['time'] = 'Q'+str(j[1])
                    if j[2] is not None:
                        a['resolutionrate'] =j[2]
                    else:
                        a['resolutionrate'] = 0
                    b.append(a)
                response = {"success": "true", "msg": "ok", "data": b}
            except Exception as e:
                raise e
                response = {"success": "false", "msg": "查询失败~~"}
            return json.dumps(response, ensure_ascii=False)
        else:
            response = {"success": "false", "msg": "查询失败~~"}
            return json.dumps(response, ensure_ascii=False)

# 导出获取新增技术支持
exporttechnicalSupport = Blueprint('exporttechnicalSupport', __name__)
@exporttechnicalSupport.route('/exporttechnicalSupport')
def getexporttechnicalSupport():
    try:
        startdate = request.args["startdate"]
        enddate=(datetime.datetime.strptime(request.args["enddate"], "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        print(startdate,type(startdate))
        print(enddate,type(enddate))
        #startdate = '2020-2-25'
        #enddate = '2020-2-26'
        day1 = time.strptime(startdate, '%Y-%m-%d')
        day2 = time.strptime(enddate, '%Y-%m-%d')
        daynum = (int(time.mktime(day2)) - int(time.mktime(day1))) / (24 * 60 * 60)
        print(abs(int(daynum)),type(abs(int(daynum))))
        if(abs(int(daynum))>30):
            response = {"success": "false", "msg": "日期间隔请小于30天~"}
        else:
            db = "jira"
            #sql = "select t2.SUMMARY,t2.CREATOR,t2.ASSIGNEE,t4.pname,t3.customvalue,t2.CREATED from (select ISSUE,STRINGVALUE from customfieldvalue where CUSTOMFIELD = 17807 and STRINGVALUE  in ('20565','20566','19626','19630','20584','20568','19627','19628','19631','19633','19632','19634','19635','19636','19884')) t1 left join jiraissue t2 on t1.ISSUE=t2.ID left join customfieldoption t3 on t1.STRINGVALUE=t3.ID left join issuestatus t4 on t4.ID=t2.issuestatus where t2.PROJECT =13117 and t2.issuetype =14806 and t2.CREATED between '%s' and '%s' order by t2.CREATED"%(startdate,enddate)
            sql = "select tmp1.SUMMARY, case when tuser1.name_cn is null then tmp1.CREATOR else tuser1.name_cn end as  CREATOR, case when tuser2.name_cn is null then tmp1.ASSIGNEE else tuser2.name_cn end as  ASSIGNEE, tmp1.pname, tmp1.CREATED, tmp1.customvalue from (select t2.SUMMARY, t2.CREATOR, t2.ASSIGNEE, t4.pname, t2.CREATED, t3.customvalue from (select ISSUE, STRINGVALUE from customfieldvalue where CUSTOMFIELD = 17807 and STRINGVALUE in ('20565', '20566', '19626', '19630', '20584', '20568', '19627', '19628', '19631', '19633', '19632', '19634', '19635', '19636', '19884')) t1 left join jiraissue t2 on t1.ISSUE = t2.ID left join customfieldoption t3 on t1.STRINGVALUE = t3.ID left join issuestatus t4 on t2.issuestatus = t4.ID where t2.PROJECT = 13117 and t2.issuetype = 14806 and t2.CREATED between '%s' and '%s' order by t2.CREATED) tmp1 left join t_oa_user tuser1 on tmp1.CREATOR = tuser1.name_en left join t_oa_user tuser2 on tmp1.ASSIGNEE = tuser2.name_en"%(startdate,enddate)
            fromSql = queryFromSql(db, sql)
            list = fromSql.sqlToList()
            #print(list)
            response = {"success": "true", "msg": "OK","data": list}
    except Exception as e:
        raise e
        response = {"success": "false", "msg": "查询失败~~"}
    response = json.dumps(response,ensure_ascii=False)
    return response




if __name__ == '__main__':
    print(getResolutionRate())
