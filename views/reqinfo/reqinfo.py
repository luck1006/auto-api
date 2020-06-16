# -*- coding: utf-8 -*-
# Author:       liujingzu
# Explain：     scrum迭代过程数据统计

from app.models.models import *
from flask import Blueprint,current_app,request
from flask import make_response,send_from_directory,abort,request,jsonify,Flask,send_file
import os,json
import requests
from sys import stdout
import mimetypes
#解决跨域问题
from flask import Flask, session
from flask_cors import CORS
import pymysql
from jira import JIRA
from sqlalchemy import func
from sqlalchemy import and_, or_, distinct, text
# 设置蓝图
reqinfo = Blueprint('reqinfo', __name__)

# cors = CORS(reqinfo, resources={r"/.*": {"origins": "http://pandora.tuniu.org"}})   # 只允许特定域名跨域
# cors = CORS(reqinfo, resources={r"/.*": {"origins": "http://localhost:8081"}})   # 只允许特定域名跨域

@reqinfo.route('/reqinfo/searchreqinfo',methods=['GET'])
def searchreqinfo():
    # 获取入参
    Scrum_label = request.args['team']
    print (Scrum_label)
    Scrum_project = request.args['project']
    print (Scrum_project)
    scrum_version = request.args['version']
    print (scrum_version)
    SM_account=request.args['username']
    print (SM_account)
    SM_passwd= request.args['password']
    print (SM_passwd)

    #每次查询，实时查询JIRA数据，并更新数据库表字段信息
    try :
        jira = JIRA(server='http://jira.tuniu.org', basic_auth=(SM_account, SM_passwd))
        jql_all = 'project in ('+Scrum_project+') AND issuetype in (业务需求, 技术需求) AND sprint in ('+scrum_version+') AND Labels in ('+Scrum_label+') ORDER BY assignee ASC, reporter ASC, rank'
        requirement_list = jira.search_issues(jql_all,maxResults=-1)
        requirement_list_total = len(requirement_list)

        jql_bug_all = 'project in ('+Scrum_project+') AND issuetype in (Bug, 线上Bug, 开发测试Bug) AND Sprint = '+scrum_version
        bug_list = jira.search_issues(jql_bug_all,maxResults=-1)
        bug_list_total = len(bug_list)

        jql_subreq_all = 'project in ('+Scrum_project+') AND issuetype in (子事务) AND sprint in ('+scrum_version+') ORDER BY assignee ASC, reporter ASC, rank'
        sub_requirement_list = jira.search_issues(jql_subreq_all,maxResults=-1)
        sub_requirement_list_total = len(sub_requirement_list)
    except Exception as e:
        print (e)
        raise e
        response = {"success": "false", "msg": "JIRA链接查询失败~~"}

    #若存在需求，查询进行初始化操作插入/更新数据
    if requirement_list_total > 0 :
        for req in requirement_list:
            count_req_key = Scrum_Req_Info.query.filter(
                            and_(Scrum_Req_Info.key == req.key)).count()
            if count_req_key == 0:
                #需求子事务个数
                subreqnum = 0
                type = 0
                isdelay = 0
                isinsert = 0
                delay_version = 'None'
                for subreq in sub_requirement_list:
                    if str(subreq.fields.parent)==str(req.key):
                        subreqnum = subreqnum +1
                assigneestr=str(req.fields.assignee).split(' ')
                reporterstr=str(req.fields.reporter).split(' ')
                points = str(req.fields.customfield_10308)
                if points == 'None':
                    points = int(0)
                else:
                    points = int (float(points))
                processlist=str(req.fields.customfield_18435).replace('\r','').split('\n')
                if str(processlist[0]).find("插入") != -1:
                    isinsert = 1
                if str(processlist[-1]).find("延期") != -1:
                    isdelay = 1
                    delay_version = scrum_version
                process= str(str(req.fields.customfield_18435).replace('\r',';'))
                reqinfo = Scrum_Req_Info(
                    key= req.key,
                    permalink = req.permalink(),
                    summary = req.fields.summary,
                    owner_team = Scrum_label,
                    owner_project = Scrum_project,
                    owner_version = scrum_version,
                    type = type,
                    reporter = str(reporterstr[0]),
                    assigner = str(assigneestr[0]),
                    points = points,
                    subreqnum = subreqnum,
                    status = str(req.fields.status),
                    isdelay = isdelay,
                    isinsert = isinsert,
                    process = process,
                    delay_version = delay_version
                )
                try:
                    db.session.add(reqinfo)
                    db.session.commit()
                except Exception as e:
                    print (e)
                    raise e
                    response = {"success": "false", "msg": "数据初始化插入失败~~"}
            else:
                #需求子事务个数
                subreqnum_update = 0
                type_update = 0
                isdelay_update = 0
                isinsert_update = 0
                delay_version_update = 'None'
                for subreq in sub_requirement_list:
                    if str(subreq.fields.parent)==str(req.key):
                        subreqnum_update = subreqnum_update +1
                assigneestr_update=str(req.fields.assignee).split(' ')
                reporterstr_update=str(req.fields.reporter).split(' ')
                points_update = str(req.fields.customfield_10308)
                if points_update == 'None':
                    points_update = int(0)
                else:
                    points_update = int (float(points_update))
                processlist_update=str(req.fields.customfield_18435).replace('\r','').split('\n')
                if str(processlist_update[0]).find("插入") != -1:
                    isinsert_update = 1
                if str(processlist_update[-1]).find("延期") != -1:
                    isdelay_update = 1
                    delay_version_update = scrum_version
                process_update= str(str(req.fields.customfield_18435).replace('\r',';'))
                try:
                    Scrum_Req_Info.query.filter(
                        and_(Scrum_Req_Info.key == req.key)).update({
                            # 'key' : req.key,
                            # 'permalink' : req.permalink(),
                            'summary' : req.fields.summary,
                            'owner_team' : Scrum_label,
                            'owner_project' : Scrum_project,
                            'owner_version' : scrum_version,
                            'type' : type_update,
                            'reporter' : str(reporterstr_update[0]),
                            'assigner' : str(assigneestr_update[0]),
                            'points' : points_update,
                            'subreqnum' : subreqnum_update,
                            'status' : str(req.fields.status),
                            'isdelay' : isdelay_update,
                            'isinsert' : isinsert_update,
                            'process' : process_update,
                            'delay_version' : delay_version_update
                        })
                    db.session.commit()
                except Exception as e:
                    print (e)
                    raise e
                    response = {"success": "false", "msg": "数据更新失败~~"}

        #接口查询返回需求数据
        try:
            #获取指定version的需求
            version_reqcount = db.session.query(Scrum_Req_Info).filter(Scrum_Req_Info.type==0,Scrum_Req_Info.owner_team==Scrum_label,Scrum_Req_Info.owner_project==Scrum_project,Scrum_Req_Info.owner_version==scrum_version).count()

            #获取指定version的延期需求
            version_reqdelaycount = db.session.query(Scrum_Req_Info).filter(Scrum_Req_Info.type==0,Scrum_Req_Info.owner_team==Scrum_label,Scrum_Req_Info.owner_project==Scrum_project,Scrum_Req_Info.isdelay==1,Scrum_Req_Info.owner_version==scrum_version).count()

            #获取指定version的延期需求
            version_insertcount = db.session.query(Scrum_Req_Info).filter(Scrum_Req_Info.type==0,Scrum_Req_Info.owner_team==Scrum_label,Scrum_Req_Info.owner_project==Scrum_project,Scrum_Req_Info.isinsert==1,Scrum_Req_Info.owner_version==scrum_version).count()

            #获取指定version的需求详情
            owner_result = db.session.query(Scrum_Req_Info.key,Scrum_Req_Info.permalink,Scrum_Req_Info.summary,Scrum_Req_Info.owner_version,Scrum_Req_Info.reporter,Scrum_Req_Info.assigner,Scrum_Req_Info.points,Scrum_Req_Info.subreqnum,Scrum_Req_Info.status,Scrum_Req_Info.isdelay,Scrum_Req_Info.isinsert,Scrum_Req_Info.process).filter(Scrum_Req_Info.type==0,Scrum_Req_Info.owner_team==Scrum_label,Scrum_Req_Info.owner_project==Scrum_project,Scrum_Req_Info.owner_version==scrum_version).all()

            #统计所有版本
            owner_version_reqinfolist = []
            for owner_info in owner_result:
                b= {}
                b['key']=owner_info[0]
                b['permalink']= owner_info[1]
                b['summary']= owner_info[2]
                b['owner_version']= owner_info[3]
                b['reporter'] = owner_info [4]
                b['assigner'] = owner_info [5]
                b['points'] = owner_info[6]
                b['subreqnum']= owner_info[7]
                b['status']= owner_info[8]
                b['isdelay']= owner_info[9]
                b['isinsert']=owner_info[10]
                b['process']= owner_info[11]
                owner_version_reqinfolist.append(b)

            response = {"success": True, "msg": "查询成功","total":version_reqcount,"delaytotal":version_reqdelaycount,"insertotal":version_insertcount,"owner_data":owner_version_reqinfolist}
        except Exception as e:
            print (e)
            raise e
            response = {"success": "false", "msg": "查询失败~~"}
    else:
        response = {"success": True, "msg": "查询成功","total":0,"delaytotal":0,"insertotal":0,"owner_data":'null'}

    print (response)
    response = json.dumps(response,ensure_ascii=False)
    return response



@reqinfo.route('/reqinfo/getreqteaminfo',methods=['GET'])
def getreqteaminfo():
    try:
        result = db.session.query(Scrum_Req_TeamInfo.req_team,Scrum_Req_TeamInfo.req_project,Scrum_Req_TeamInfo.req_version).filter(Scrum_Req_TeamInfo.del_flag==0).all()
        resultlist = []
        for res in result:
            a = {}
            a["req_team"]= res[0]
            a["req_project"]= res[1]
            a["req_version"]= res[2]
            resultlist.append(a)
        # teamlist = db.session.query(Scrum_Req_TeamInfo.req_team).filter(Scrum_Req_TeamInfo.del_flag==0).distinct().one()
        # print (teamlist)
        response = {"success":True,"msg":"查询成功","data":resultlist}

    except Exception as e:
        print (e)
        raise e
        response = {"success": "false", "msg":"查询失败~~~"}

    print (response)
    response = json.dumps(response,ensure_ascii=False)
    return response







