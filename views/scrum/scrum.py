# -*- coding: utf-8 -*-
# TIME:         下午2:56
# Author:       zhuhaiyan
# Explain：         获取scrumteam信息返回前端生成echart图标

from app.models.models import *
from flask import Blueprint, request
from sqlalchemy import func, and_,cast, distinct
from app import db,cache
import json, requests
import sys
from flask import current_app
from app.actions.TNJ.daysReport_copy import *
from collections import OrderedDict

# 设置蓝图
scrum = Blueprint('scrum', __name__)


# @scrum.route('/')
# def home():
#     #return render_template('dist/index.html')
#     return "hello"


@scrum.route('/queryChart')
@cache.cached(query_string=True)
def getScrumInfo():
    # 查询所有的scrumteam
    try:
        listInfo = db.session.query(Teamname.team, Teamname.name, Teamname.topic).filter(Teamname.flag == 1).all()
        scrumInfos = []
        ammInfos = []
        pointInfos = []
        infos = []
        compval = ""
        for i in range(len(listInfo)):
            iCnt=0
            # 获取team的point的bug信息
            scrumInfo = Scrumteam.query.filter(Scrumteam.team == listInfo[i][0]).order_by(cast(func.replace(Scrumteam.vers,".","") ,db.Integer).desc()).all()
            for j in range(len(scrumInfo)):
                data = {
                    "vers": scrumInfo[j].vers,
                    "reqnum": scrumInfo[j].reqnum,
                    "planpoint": scrumInfo[j].planpoint,
                    "actualpoint": scrumInfo[j].actualpoint,
                    "bugnum": scrumInfo[j].bugnum,
                    "bugrate": "%.2f%%" % (scrumInfo[j].bugrate * 100),
                }
                # scrumInfos.append(data)
                #不超过8个迭代的数据
                iCnt+=1
                if iCnt<=50:
                    scrumInfos.append(data)
            scrumInfos.reverse()
            # 获取team敏捷成熟度信息
            quarterInfo = db.session.query(Ammteam.quarter).filter(Ammteam.team == listInfo[i][0]).group_by(
                Ammteam.quarter).all()
            for z in range(len(quarterInfo)):
                ammInfo = db.session.query(Ammfirst.id, Ammfirst.title, func.sum(Ammsecond.point)).filter(
                    and_(Ammsecond.firstid == Ammfirst.id, Ammteam.secondid == Ammsecond.id,
                         Ammteam.team == listInfo[i][0]), Ammteam.quarter == quarterInfo[z][0]).group_by(
                    Ammfirst.id).order_by(Ammfirst.id).all()
                # current_app.logger.info(ammInfo)
                for x in range(len(ammInfo)):
                    quarter = quarterInfo[z][0]
                    id = ammInfo[x][0]
                    title = ammInfo[x][1]
                    point = int(ammInfo[x][2])
                    pointInfos.append({"id": id, "title": title, "point": point})
                ammInfos.append({"legend": quarter, "data": pointInfos})
                pointInfos = []
            infos.append(
                {"teamCode": listInfo[i][0], "teamName": listInfo[i][1],"teamtopic": listInfo[i][2], "scrumInfo": scrumInfos, "ammInfo": ammInfos})
            scrumInfos = []
            ammInfos = []
        response = ({"success": "true", "msg": "OK", "data": infos})
    except Exception as e:
        raise e
        response = {"success": "false", "msg": "查询失败~~"}
    # print (response)
    response = json.dumps(response)
    return response

#获取团队与sprint对应关系
@scrum.route('/getTeamSprintRelationship', methods=['GET'])
def getTeamSprintRelationship():
    team_sprint = {}
    sprintList = []
    teamInfo = db.session.query(Teamname.name, Teamname.topic, Teamname.team).filter(and_(Teamname.flag==1,Teamname.topic != None)).all()
    print("teamInfo List: ", teamInfo)

    # temp_sprint = requests.get('http://magic-box.api.tuniu.org/tnj/sprint')
    # temp_sprint = json.loads(temp_sprint.content, encoding='utf-8')

    # 查询已经激活且未关闭的sprint
    response = BurnDown().jira_sprintQuery()
    # print(response)
    temp_sprint = []
    if response is not None:
        for item in response['sprints']:
            if item['state'] == 'ACTIVE':
                temp_sprint.append({"id": item['id'], "name": item['name']})
    print('111111--->:\n', temp_sprint)

    if teamInfo != None:
        for team_item in teamInfo:
            for sprint_item in temp_sprint:
                if (sprint_item['name'].find(team_item[0]) != -1) or (sprint_item['name'].find(team_item[2]) != -1):
                    tmp = list(team_item)
                    tmp.append(sprint_item['name'])
                    tmp.append(sprint_item['id'])
                    sprintList.append(tmp)
                    break
        print("sssssss: ",sprintList)

    if sprintList not in (None,[]):
        for i in sprintList:
            if i[1] in team_sprint.keys():
                tmp_item = team_sprint[i[1]]
                o= {}
                o['value'] = i[4]
                o['label'] = i[3]
                tmp_item.append(o)
                team_sprint[i[1]] = tmp_item
            else:
                tmp_item = []
                o= {}
                o['value'] = i[4]
                o['label'] = i[3]
                tmp_item.append(o)
                team_sprint[i[1]] = tmp_item
        print('team_sprint: ', team_sprint)

        response = {'success': True, 'msg': '查询成功', 'data': team_sprint}
    else:
        response = {'success': False, 'msg': '查询为空', 'data': None}

    # response = {"success": True, "msg": "查询成功", "data": {"赤焰军-2B赋能": [{"value": "20.02.0_YCY_商旅主线", "label": "20.02.0_YCY_商旅主线"}], "神兽团-应用中台": [{"value": "20.02.0_玄武_对客体验", "label": "20.02.0_玄武_对客体验"}, {"value": "20.02.0_麒麟_产品详情页", "label": "20.02.0_麒麟_产品详情页"}, {"value": "20.02.0_朱雀_工具与顾问对象", "label": "20.02.0_朱雀_工具与顾问对象"}, {"value": "20.02.0_山猫_基础服务和框架", "label": "20.02.0_山猫_基础服务和框架"}, {"value": "20.02.0_白泽_技术支持标准化", "label": "20.02.0_白泽_技术支持标准化"}, {"value": "20.02.0_白虎_金融与保险", "label": "20.02.0_白虎_金融与保险"}], "财神团-内核": [{"value": "20.02.0_金鳌_人事财务", "label": "20.02.0_金鳌_人事财务"}, {"value": "20.02.0_金蟾_财务标准化", "label": "20.02.0_金蟾_财务标准化"}, {"value": "20.02.0_貔貅_支付对账", "label": "20.02.0_貔貅_支付对账"}]}}

    return json.dumps(response)

#根据日期、组织架构查询jira日报数据
@scrum.route('/queryDaysReport', methods = ['GET'])
def queryDaysReport():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    dept_desc = request.args.get('dept_desc')
    scrum_team = request.args.get('scrum_team')
    workers_list = request.args.get('worker')

    print('params workers_list is .....: ', workers_list)

    if workers_list not in('', None, []):
        workers_list = workers_list
    else:
        if scrum_team not in ('', [], None):
            workers_list = []
            for item in scrum_team.split(','):
                workers_list += getWorkersFromScrum(item)
            workers_str = "("
            for worker in workers_list:
                workers_str += "'" + worker + "',"
            workers_list = workers_str[0:-1] + ")"
        else:
            workers_list = ''

    print('the params is : ', start_time, '   ', end_time, '  ', dept_desc, '   ', workers_list )

    # start_time = '2020-02-10'
    # end_time = '2020-02-14'
    # # dept_desc = "('研发TeamI','质量TeamR')"
    # dept_desc = ''
    # workers_list = ''

    #通过入参条件调方法查询数据库获取jira日报数据
    data = jira_tuniu_copy(start_time,end_time,dept_desc, workers_list)
    # print('the daysReport data is :\n', data, '\n', len(data))

    #获取人员与scrum_team的对应关系
    worker_scrum = get_Worker_Scrum_rel()
    # print('worker scrum is :', '\n', worker_scrum)
    data_list = []

    if len(data) > 0:
        #在查询到的jira日报数据字典中增加对应 人员的scrum_team
        for data_item in data:
            times = 0
            for scrum in worker_scrum:
                if data_item['worker_name'] == scrum[0]:
                    data_item['scrum_team'] = scrum[1]
                    data_list.append(data_item)
                    times +=1
                    break
            if times == 0:
                data_item['scrum_team'] = ''
                data_list.append(data_item)
        # response = {'success': True, 'msg': '查询成功', 'data': data}
        response = {'success': True, 'msg': '查询成功', 'data': data_list}
    else:
        response = {'success': False, 'msg': '查询数据为空', 'data':[]}

    return json.dumps(response,ensure_ascii=False)


@scrum.route('/getScrumTeam', methods = ['GET'])
def getScrumTeam():
    scrumTeam = db.session.query(distinct(Worker_ScrumTeam.scrum_team)).filter(Worker_ScrumTeam.status == True).all()
    print('the scrumTeam list is :\n', scrumTeam)
    scrumTeam_list = []
    if scrumTeam is not None:
        for team in scrumTeam:
            scrumTeam_list.append({'label':team[0], 'value': team[0]})
        response = {'success': True, 'msg': '查询成功', 'data': scrumTeam_list}
    else:
        response = {'success': False, 'msg': '查询数据为空', 'data': []}

    return json.dumps(response, ensure_ascii=False)

@scrum.route('/getWorkersList', methods = ['GET'])
def getWorkersList():
    # scrum_team = request.args.get('scrum_team')
    # print('the scrum_team: \n', scrum_team)
    #
    # if scrum_team not in ('', [], None):
    #     workers_list = []
    #     for item in scrum_team.split(','):
    #         workers_list += getWorkersFromScrum(item)
    #     # workers_str = "("
    #     # for worker in workers_list:
    #     #     workers_str += "'" + worker + "',"
    #     # workers_list = workers_str[0:-1] + ")"
    #     print('the workerlist is :\n', workers_list)
    #     data = []
    #     if len(workers_list) > 0:
    #         for worker in workers_list:
    #             data.append({'label': worker, 'value': worker})
    #
    #         response = {'success': True, 'msg': '查询成功', 'data': data}
    #     else:
    #         response = {'success': False, 'msg': '查询数据为空', 'data': []}
    # else:
    #     response = {'success': False, 'msg': '未选择要查询的scrumTeam,无需查询', 'data': []}
    workers = get_Worker_Scrum_rel()
    workers_list = []
    if len(workers) > 0:
        for worker in workers:
            workers_list.append({'label': worker[0], 'value': worker[0]})
        response = {'success': True, 'msg': '查询成功', 'data': workers_list}
    else:
        response = {'success': False, 'msg': '查询数据为空', 'data': []}

    return json.dumps(response, ensure_ascii=False)

#根据sprintId获取该迭代组燃尽图数据
@scrum.route('/scopechangeburndownchart',methods=['GET'])
def scopechangeburndownchart():
    sprintId = request.args.get('sprintid')
    # print('the params is :',sprintId, type(sprintId))

    # sprintId = 4527
    #将sprintid 由str转成list
    sprintIds = eval(sprintId)


    burndownlist = []
    if len(sprintIds) > 0:

        for sprint in sprintIds:
            response = BurnDown().jira_scopechangeburndownchart(sprint['sprintid'])
            if response is not None:
                # temp_response = {}
                # for change in response['changes'].keys():
                #     otherStyleTime = timeStamp(change)
                #     temp_response[otherStyleTime]=response['changes'][change]
                # response['changes'] = temp_response
                # response['startTime'] = timeStamp(response['startTime'])
                # response['endTime'] = timeStamp(response['endTime'])
                response['changes'] = OrderedDict(sorted(response['changes'].items()))
                # 将response转成前台可以直接使用的图表data样式[时间，花费时间，[{issue1.。。}，{issues2....}]
                tmpEstimate = []
                tmpSpent = []
                currentSpent = 0
                currentEstimate = 0

                tmpvalues = []

                for k,v in response['changes'].items():
                    # print('1111111',k, type(k))
                    # print('2222222', response['startTime'], type(response['startTime']))

                    if int(k) <= response['startTime']:

                        for values in v:
                            if 'timeC' in values.keys():
                                if 'newEstimate' in values['timeC'].keys():
                                    currentEstimate += values['timeC']['newEstimate']
                                # 在迭代开启前，只统计新增的且有记录工时的issue的花费时间
                                if 'added' in values.keys() and 'timeSpent' in values['timeC'].keys():
                                    currentSpent += values['timeC']['timeSpent']

                                tmpvalues.append(values)
                    else:
                        break
                # 对estimate时间处理，若为负数，则显示为0
                if currentEstimate < 0:
                    currentEstimate = 0
                tmpSpent.append([int(get_time_stamp13(dateStamp(response['startTime'])+' 00:00:00')), round(currentSpent/3600,2), tmpvalues])
                tmpEstimate.append([int((get_time_stamp13(dateStamp(response['startTime'])+' 00:00:00'))), round((currentEstimate)/3600,2), tmpvalues])


                for k, v in response['changes'].items():
                    tmpvalues = []
                    if int(k) > response['startTime']:

                        for values in v:
                            if 'timeC' in values.keys():
                                # if 'newEstimate' in values['timeC'].keys():
                                #     currentEstimate += values['timeC']['newEstimate']
                                if values['timeC']['newEstimate'] < 0:
                                    currentEstimate += 0
                                else:
                                    currentEstimate += values['timeC']['newEstimate']

                                if 'timeSpent' in values['timeC'].keys():
                                    # 当已记录工时（如果新shengyu时间不为负数，才统计花时间），shengyu时间= 当前shengyu - 当前花费时间
                                    if values['timeC']['newEstimate'] >= 0:
                                        currentSpent += values['timeC']['timeSpent']
                                    currentEstimate -= values['timeC']['timeSpent']

                                tmpvalues.append(values)
                        # 对estimate时间处理，若为负数，则显示为0
                        if currentEstimate < 0:
                            currentEstimate = 0
                        if tmpvalues != []:
                            tmpSpent.append([int(k), round(currentSpent/3600,2), tmpvalues])
                            tmpEstimate.append([int(k), round((currentEstimate)/3600,2), tmpvalues])

                response['spent'] = tmpSpent
                response['estimate'] = tmpEstimate
                response['sprintName'] = sprint['sprintname']
                response.pop('changes')
                burndownlist.append(response)

        response = {'success': True, 'msg': '查询成功', 'data': burndownlist}
    else:
        response = {'success': True, 'msg': '未查询到该团下的sprint数据', 'data': []}
    return json.dumps(response, ensure_ascii=False)

#获取当前已激活的sprint
@scrum.route('/queryActiveSprint',methods=['GET'])
def queryActiveSprint():
    response = BurnDown().jira_sprintQuery()
    # print(response)
    sprint_data = []
    if response is not None:
        for item in response['sprints']:
            if item['state'] == 'ACTIVE':
                sprint_data.append({"id":item['id'],"name":item['name']})

        response = {'success': True, 'msg': '查询成功', 'data': sprint_data}
    else:
        response = {'success': True, 'msg': '查询成功', 'data': None}
    return json.dumps(response, ensure_ascii=False)