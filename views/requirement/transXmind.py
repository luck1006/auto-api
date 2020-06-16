# -*- coding: utf-8 -*-
# TIME:         9.18
# Author:       zhuhaiyan
# Explain：     从jira数据库中获取epic对应的story信息


import datetime
from jira import JIRA
import json
from app.models.models import *
from flask import Blueprint,request
from app.actions.tools.queryFromSql import  queryFromSql
import re
from flask import Flask  ,jsonify

#蓝图，注册到app
getXmind = Blueprint('getXmind', __name__,)

#路由，具体业务接口
@getXmind.route('/getXmind',methods=['GET','POST'])
def getEpicxmind():
    epic = request.args['epic']
    print(epic)
    id=  int(request.args['id'] )
    print(id)
    issuenum= request.args['issuenum']
    print(issuenum)
    project_key=request.args['project_key']
    print(project_key)
    infos = []
    try:
        uni=0
        preVer=""
        preteamName=""
        preId=""
        db="jira"
        sql="select a.id,b.stringvalue ,c.name, issuenum,project,d.project_key,reporter,issuetype,summary,issuestatus,e.pname from jiraissue a left join customfieldvalue b  on  a.id =b.issue and b.customfield=10300 left join AO_60DB71_SPRINT c on b.stringvalue=c.id   join project_key d on a.project=d.project_id  join issuestatus e on issuestatus=e.id where a.id in(select destination from issuelink  where linktype=10200 and  SOURCE=%d) order by stringvalue desc"%(id)
        fromSql=queryFromSql(db,sql)
        list=fromSql.sqlToList()
        url = "https://jira.tuniu.org/browse/" + project_key + "-" + issuenum
        print(url)
        infos.append({'id': 'root', 'isroot': 'True', 'topic': epic,'url':url})

        for i in list:
            url = "https://jira.tuniu.org/browse/" + i["project_key"] + "-" + i["issuenum"]
            # print(url)
            if i["name"]!="":
                name=i["name"].replace("-","_")
                name = name.replace(" ", "_")
                nameArr=name.split("_",2)
                ver=nameArr[0]  #版本
                teamName=nameArr[1] #团队名称
                issuenum=str(i["issuenum"])
                verId = i["stringvalue"]
                teamId = verId + teamName
                if ver!=preVer:
                    infos.append({'id': verId, 'parentid': 'root', 'topic': ver,'url':""})
                    infos.append({'id': teamId, 'parentid':  verId, 'topic': teamName,'url':""})
                    infos.append({'id': issuenum, 'parentid': teamId, 'topic': i["pname"]+"-"+i["summary"],'url':url})
                else:
                    if teamName !=preteamName:
                        infos.append({'id': teamId, 'parentid': preId, 'topic': teamName,'url':""})
                        infos.append({'id': issuenum, 'parentid': teamId, 'topic': i["pname"]+"-"+i["summary"],'url':url})
                    else:
                        infos.append({'id': issuenum, 'parentid': teamId, 'topic': i["pname"]+"-"+i["summary"],'url':url})
                preVer=ver
                preteamName=teamName
                preId=verId
            else :
                if uni ==0:
                    infos.append({'id': 'sub1', 'parentid': 'root', 'topic': '未排期','url':"", 'direction': 'right', 'expanded': 'False',
                     'background-color': '#0000ff'})
                    infos.append({'id': i["issuenum"], 'parentid': 'sub1', 'topic': i["pname"]+"-"+i["summary"], 'url': url})
                    uni=1
                else:
                    infos.append({'id': i["issuenum"], 'parentid': 'sub1', 'topic': i["pname"]+"-"+i["summary"],'url':url})

        response = {"success": "true", "msg": "OK", "data": infos}
        print(response)
    except Exception as e:
        raise e
        response = {"success": "false", "msg": "查询失败~~"}
    response =jsonify (response)
    return response


@getXmind.route('/getEpic',methods=['GET','POST'])
def getEpicinfo():
    try:
        infos=[]
        db="jira"
        #select * from project_key where project_key in ('FIN','MST','MID','TNTMC','TWEEKER')
        sql="select distinct b.id,b.reporter,b.issuenum,b.summary,c.pname,d.project_key,count(b.id) as cnt from issuelink a, jiraissue b, issuestatus c,project_key d where linktype=10200 and issuetype=10000 and a.source=b.id and  project in (20505) and project=PROJECT_ID and b.issuestatus=c.id  group by(b.id) order by b.id desc limit 30"
        fromSql=queryFromSql(db,sql)
        list=fromSql.sqlToList()
        # topiclist = ['系统产品研发-应用']
        for i in list:
            status=foo(i["pname"] )
            # sql1="select sum(a. numbervalue) as sumpoint from customfieldvalue a where CUSTOMFIELD = 10408  and issue in (select id from jiraissue  where id in(select destination from issuelink  where linktype=10200 and SOURCE =%d))"%(int(i["id"]))
            # fromSql = queryFromSql(db, sql1)
            # list1 = fromSql.sqlToList()
            # for j in list1:
            # print("aa========================================")
            # point=list1[0]["sumpoint"]
            # if point=="":
            #     sumpoint=0
            # else:
            #     sumpoint=point
            # teamtopic = topiclist[0]
            # if i["project_key"]== 'FIN':
            #     teamtopic =topiclist[0]
            # elif i["project_key"]== 'MID':
            #     teamtopic =topiclist[1]
            # else :
            #     teamtopic =topiclist[2]
            infos.append({'value': i["id"],'label':i["summary"] ,'status':status,'issuenum':i['issuenum'],'project_key':i["project_key"],'reporter':i["reporter"],'cnt':i["cnt"]})
        # print (infos+'\n'+infos1+'\n'+infos2)
        response = {"success": "true", "msg": "OK", "data": infos}
        print(response)
    except Exception as e:
       raise e                                              
       response = {"success": "false", "msg": "查询失败~~"}
    response =jsonify (response)
    return response




def foo(var):
        return {
            "In Progress": "进行中",
            'To Do': "待处理",
            'Done': "已完成",
        }.get(var, 'error')  # 'error'为默认返回值，可自设置




if __name__ == '__main__':
    try:
        getEpicinfo()
    except Exception as e:
        print (e)