# 统计迭代功能点数
author = "zhy"
date = "2019/3/19"
import time
import datetime

import sys,os
import unittest

# print(sys.path)
current_dir = os.path.dirname(os.path.abspath(__file__))
# print(current_dir)
config_dir = os.path.abspath(os.path.join(os.getcwd()))
# print(config_dir)
sys.path.append(current_dir)
sys.path.append(config_dir)
# print(sys.path)


from jira import JIRA
import requests
import json
import xlrd
import xlwt
import pandas as pd
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from sqlalchemy import create_engine
from app.models.models import *
from app import db
import re
import socket
import logging
import threading

now = datetime.datetime.now()
path = now.strftime("%Y%m%d%H%M%S")
pool = ThreadPool()

names = []
planPoints = []
planCnts = []
actPoints = []
actCnts = []
addPoints = []
puntedPoints = []
Rates = []
BugCnts = []
bugRates = []
sumCnts = []


class GetJira():


    def __init__(self):

        # 初始化链接Jira,定义Jira空间和Epic时间
        self.jira = JIRA('https://jira.tuniu.org', basic_auth=('zhuhaiyan', 'map.eat-99'))
        JSESSIONID = self.jira.session(auth=('zhuhaiyan', 'map.eat-99')).raw['session']['value']
        self.server = "https://jira.tuniu.org/browse/"
        self.header = {"Accept": "*/*",
                       "Accept-Encoding": "gzip,deflate",
                       "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
                       "Connection": "keep-alive",
                       "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
                       "Referer": "https://jira.tuniu.org/secure/RapidBoard.jspa?rapidView=941&view=reporting&chart=sprintRetrospective&sprint=3888",
                       "Cookie": "__utmz=20250019.1550624936.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _pzfxuvpc=1551152287968%7C8015486457172139600%7C2%7C1551156273046%7C2%7C2608662471935185260%7C1384817995408035069; __xsptplus352=352.1.1551156339.1551156339.1%234%7C%7C%7C%7C%7C%23%23tUrPj1WhfY3K_QBxUtRn560zOFAoVVgo%23; _tact=Nzk3YmIwYjYtN2Q4OS1hNjJmLWMxMjEtMDljOWZhNjA1OGVi; _taca=1552876801703.1552876801703.1552876801703.1; BSFIT_OkLJUJ=FFLCzFWmqskSQW4N_1lRQ4o3xC7piUID; fp_ver=4.5.2; BSFIT_EXPIRATION=1552933688784; BSFIT_DEVICEID=a8o9OTQ__Hp9i2AoP_OjWrkUdJxuSRdg5z3XpXimAGKoqi_kWrZCzSTCAaYyKkdMN-Mpj_FQgeL-Omw7reL41SBMFbQxEpThuXYKZhUs9Nmpghwcz49KVm9PjCgne-Hg0e8Ya1lZlzg3pqGiXCrYI2X7AMtQXaXK; __utma=20250019.122278891.1550624936.1552900899.1552904774.10; jira.mobile.desktop.switch=true; seraph.rememberme.cookie=128965%3Ac8209fdfc08916dd228e38ac8af1017aed12fb09; atlassian.xsrf.token=BUUK-J6AN-FDNV-PLO6|ad289024b91fac33095f6b47d8dba04aefbc8fbe|lin; JSESSIONID=" + JSESSIONID}
        # self.project = 'CONTENT, "INT", MALL,PJ_自由行——国内打包预订更便宜,PJ_打包更便宜III期-国内库存酒店,VACA'
        # self.project = 'FIN,MST,MID,TNTMC,TWEEKER,VACA'
        self.project = 'AMID'
        self.created = "2019-01-01 "
        self.status = "待解决", "待回归", "待分配", "延后处理", "待确认", "已关闭（正常）"
        self.issuetype = "开发测试Bug,线上Bug"

    # 根据id获取point
    def get_Point(self, key_Id):
        issue = self.jira.issue(key_Id)
        content = issue.raw
        # print (content)
        if content['fields']['status']['name'] != "已取消":
            if str(content).find('customfield_10308')>=0:
                point = content['fields']['customfield_10308']
            else:
                point = 0
                print (key_Id+"无story point字段，请检查需求类型填写是否符合规范")
        else:
            point = 0
        # print (point)
        return point

    # 获取开发测试BUG
    def get_DevBug(self, s_sprint):
        devBugkeys = []
        devBug = self.jira.search_issues(
            f'project in ({self.project}) and issuetype in ({self.issuetype})  and status in ({self.status}) and sprint in ({s_sprint}) ORDER BY assignee ASC',
            maxResults=False, fields='summary,description,comment')
        # print (devBug)
        for i in devBug:
            devBugkeys.append(i.key)
        # print (devBugkeys)
        return devBugkeys

    # 获取bug严重程度，对bug进行折算
    def get_BugDetail(self, devBugkeys):
        GetJ = GetJira()
        i = 0
        for bugDetail in devBugkeys:
            # i = i + 1
            bugid = bugDetail
            issue = self.jira.issue(bugid)
            bug = issue.raw
            # 严重程度
            severity = bug['fields']['customfield_10040']['value']
            # print(severity)
            j = GetJ.foo(severity)
            i += j
        return i

    def foo(self, var):
        return {
            "C-一般": 1,
            'A-致命': 4,
            'B-严重': 2,
            'D-轻微': 0.5,
            'E-建议': 0.5,
            '无': 1
        }.get(var, 'error')  # 'error'为默认返回值，可自设置

    def get_SprintId(self, url, scrumName, j):
        # print(url)
        self.sprintUrl = url
        ids = []
        names = []  # 从jira中获取经办人列表
        reportUrls = []
        response = requests.get(self.sprintUrl, headers=self.header)
        # getcontent = response.text
        # json到字典的转化
        # list_active = []
        dict_content = json.loads(response.text)
        # print(dict_content)
        sprints = dict_content['sprints']
        # historyName=version +"Volvo_慧勇"+version +"Stark_周燕"+version+"冰岛_杨洁"+version+"翡诺岛_赵阳"+version+"布吉岛_明星"+version+"Renault_桃林"+version+"Transformer_翠翠"+version+"拉布拉卡_刘飞"+version+"侠客岛_汤靖咚"+version+"Architect"
        # historyName=version+"阿尔法"+version+"NIO"+version+"GTR"
        # print(scrumName)
        for i in sprints:
            s = i["name"]
            s = s.replace("-", "_")
            # print('s1>>>>>>>>>>>>>>>>>>>'+s)
            if s in scrumName:  # 迭代开启中的sprint
                id = str(i["id"])
                name = i["name"]
                ids.append(id)
                # print("name55555555>>>>>>>>>>>>>>>>>>>>>>>>"+name)
                names.append(name)
        # print (ids)
        # print (j)
        if len(ids) > 0:
            for id in ids:
                if j == 0:
                    reportUrl = "https://jira.tuniu.org/rest/greenhopper/1.0/rapid/charts/sprintreport?rapidViewId=1079&sprintId=" + id + "&_=1578644638913"
                # reportUrl=reportUrl
                # elif j == 1:
                #     reportUrl = "https://jira.tuniu.org/rest/greenhopper/1.0/rapid/charts/sprintreport?rapidViewId=1043&sprintId=" + id + "&_=1578644638913"
                # elif j == 2:
                #     reportUrl = "https://jira.tuniu.org/rest/greenhopper/1.0/rapid/charts/sprintreport?rapidViewId=1042&sprintId=" + id + "&_=1578644638913"
                reportUrls.append(reportUrl)
            # print (reportUrls)
        else:
            reportUrls = []
        return reportUrls

    # 根据指定的版本获取scrumteam信息---计划是取启动后的点数，实际取现在的点数
    def get_SprintDate(self, reportUrls):
      try:
        # print (reportUrls)
        GetJ = GetJira()
        response = requests.get(reportUrls, headers=self.header)
        dict_Issues = json.loads(response.text)
        contentComplete = dict_Issues['contents']['completedIssues']
        planompletePoint = 0  # 计划点数已完成
        planinompletePoint = 0  # 计划未完成
        planpuntedpoint = 0  # 计划移出
        sumcompletePoint = 0  # 实际完成点数
        sumIncompletePoint = 0  # 实际未文成点数
        sumAddPoint = 0  # 实际新增点数
        sumPuntedPoint = 0  # 实际移出点
        cntComplete = 0
        cntIncomplete = 0
        cntAdd = 0
        cntPunted = 0

        name = dict_Issues['sprint']['name']
        # print('name>>>>>>>>>>>>>>>>>>'+ name)
        g = re.search("(\_|\-).*(\-|\_)", name)
        # g = str(re.search("(\_).*(\_)", name))
        # print('g>>>>>>>>>>>>'+g)
        if g:
            teamname = (g.group()[1:len(g.group()) - 1])
            # print("teamnamesucces>>>>>>>>>>"+teamname)
        else:
            g = re.search("(\_|\-).*", name)
            # print("未匹配_,_or-中间的团队名称")
            teamname = (g.group()[1:len(g.group())])
            # print("teamnamef>>>>>>>>>>" + teamname)
            # print(teamname)
        # print (teamname)
        names.append(teamname)
        # print (names)
        DevBug = GetJ.get_DevBug(name)
        # print(DevBug)
        CntBug = GetJ.get_BugDetail(DevBug)
        # print(name + ":" + str(CntBug))
        # print (CntBug)
        BugCnts.append(CntBug)
        # print ("BUGcnts:"+str(BugCnts))
        # 新增需求==========================================================
        contentAdd = dict_Issues['contents']['issueKeysAddedDuringSprint']
        addkeys = contentAdd.keys()
        # print (addkeys)
        # ================================================================
        # print("#### 已完成需求 ####")
        for complete in contentComplete:
            key_Id = str(complete["key"])
            typeName = str(complete["typeName"])
            # print("typeName:" + typeName)
            req=self.jira.issue(key_Id)
            reqcontent = req.raw
            # print (reqcontent)
            # subreqlist = reqcontent['fields']['subtasks']
            # print (subreqlist)
            if typeName != '开发测试Bug' and typeName != '线上Bug':
                # 计划point
                # print (complete)
                # if complete['estimateStatistic']['statFieldValue'] != {} :
                if reqcontent['fields']['aggregatetimeoriginalestimate'] != None:
                    # print("====="+ complete['estimateStatistic']['statFieldValue'])
                    storyplanpoint = reqcontent['fields']['aggregatetimeoriginalestimate']
                    # print (complete)
                    # print ('已完成需求'+key_Id+'  '+str(storyplanpoint))
                    if key_Id not in (addkeys):
                        planompletePoint += storyplanpoint
                # elif len(subreqlist)>0:
                #     storyplanpoint = 0
                #     for subreq in subreqlist:
                #         getoriginalestime=subreq['fields']['timetracking_originalestimate']['value']
                #         print (getoriginalestime)
                #         storyplanpoint = storyplanpoint+getoriginalestime
                #     if key_Id not in (addkeys):
                #         planompletePoint += storyplanpoint
                # 实际point
                point = GetJira.get_Point(self, key_Id)
                if point == None:
                    point = 0
                # print("key_Id:" + key_Id + " point:" + str(point) + "typeName:" + typeName)
                cntComplete += 1
                sumcompletePoint += point
                # print("key_Id1:" + key_Id + "typeName:" + typeName)

        # print("#### 未完成需求 ####")
        contentIncomplete = dict_Issues['contents']['incompletedIssues']
        for incomplete in contentIncomplete:
            key_Id = str(incomplete["key"])
            typeName = (incomplete["typeName"])
            req=self.jira.issue(key_Id)
            reqcontent = req.raw
            if typeName != '开发测试Bug' and typeName != '线上Bug':
                # print (incomplete)
                if reqcontent['fields']['aggregatetimeoriginalestimate'] != None:
                    instoryplanpoint = reqcontent['fields']['aggregatetimeoriginalestimate']
                    # print (incomplete)
                    # print ('未完成'+key_Id+'   '+str(instoryplanpoint))
                    if key_Id not in (addkeys):
                        planinompletePoint += instoryplanpoint
                point = GetJira.get_Point(self, key_Id)
                if point == None:
                    point = 0
                # print("key_Id:" + key_Id + " point:" + str(point))
                sumIncompletePoint += point
                cntIncomplete += 1
        sumCnt = cntComplete + cntIncomplete
        sumCnts.append(sumCnt)

        # print("#### 新增需求 ####")
        for key_Id in addkeys:
            point = GetJira.get_Point(self, key_Id)
            if point == None:
                point = 0
            # print("key_Id:" + key_Id + " point:" + str(point))
            sumAddPoint += point
            cntAdd += 1

        # print("#### 移出需求 ####")
        contentpunted = dict_Issues['contents']['puntedIssues']
        for punted in contentpunted:
            key_Id = str(punted["key"])
            typeName = str(punted["typeName"])
            req=self.jira.issue(key_Id)
            reqcontent = req.raw
            if typeName != '开发测试Bug' and typeName != '线上Bug':
                # print (punted)
                if reqcontent['fields']['aggregatetimeoriginalestimate'] != None:
                    puntedpoint = reqcontent['fields']['aggregatetimeoriginalestimate']
                    # print ('移出需求'+key_Id+'  '+str(puntedpoint))
                    if key_Id not in (addkeys):
                        planpuntedpoint += puntedpoint
                point = GetJira.get_Point(self, key_Id)
                if point == None:
                    point = 0
                # print("key_Id:" + key_Id + " point:" + str(point))
                sumPuntedPoint += point
                cntPunted += 1

        # print ("#### 计算 -8小时为1天,需求建立子事务后预估时间####")
        # planPoint = int(int(planompletePoint + planinompletePoint + planpuntedpoint)/28800)
        planPoint = int (sumcompletePoint + sumIncompletePoint - sumAddPoint + sumPuntedPoint )
        planCnt = cntComplete + cntIncomplete + cntPunted - cntAdd
        actPoint = int(sumcompletePoint + sumIncompletePoint)
        actCnt = cntComplete + cntIncomplete
        sumAddPoint = int(sumAddPoint)
        sumPuntedPoint = int(sumPuntedPoint)

        if planPoint != 0:
            actRate = round(actPoint / planPoint, 4)
        else:
            actRate = 0
        if actPoint != 0:
            bugRate = round(CntBug / actPoint, 4)
        else:
            bugRate = 0
        bugRates.append(bugRate)
        planPoints.append(planPoint)
        planCnts.append(planCnt)
        actPoints.append(actPoint)
        actCnts.append(actCnt)
        addPoints.append(sumAddPoint)
        puntedPoints.append(sumPuntedPoint)
        Rates.append(actRate)
        # print (planPoints)
        # writer = pd.ExcelWriter(excelPath,engine='openpyxl')
        # PointsData.to_excel(excel_writer=writer, sheet_name='迭代汇总', startcol=0, index=False)
      except Exception as e:
        print (e)


    # def insertdata(self,PointsData):
    #     hostname = socket.gethostname()
    #     # logging.info("hostname>>>>>>>>>>>>>>>>>>>>"+hostname)
    #     if (hostname == 'vm-prd-tnauto-occamrazor-185-170.tuniu.org'):
    #          # app = create_app('production')
    #         engine = create_engine('mysql+mysqlconnector://root:@MonLey880124@10.28.32.130/pandora')
    #         PointsData.to_sql(Scrumteam.__tablename__, con=engine, schema="pandora", index=False,
    #                             index_label=False,
    #                             if_exists='append', chunksize=1000)
    #     else:
    #         engine = create_engine('mysql+pymysql://root:@MonLey880124@10.28.32.130/auto_platform')
    #         PointsData.to_sql(Scrumteam.__tablename__, con=engine, schema="auto_platform", index=False,
    #         # PointsData.to_sql(Scrumteam.__tablename__, con=engine, schema="pandora",index=False,
    #                             index_label=False,
    #                             if_exists='append', chunksize=1000)

    def save_Excel(self, vers):
        try:
            # vers = "10.8.0"
            GetJ = GetJira()
            # 一共2个看板，线上团队一个看板，度假三个团队一个看板

            sprintUrl = [
                # "https://jira.tuniu.org/rest/greenhopper/1.0/sprintquery/941?includeHistoricSprints=false&includeFutureSprints=false&_=1552980219648",
                # "https://jira.tuniu.org/rest/greenhopper/1.0/sprintquery/988?includeHistoricSprints=false&includeFutureSprints=false&_=1555580594015"]
                # #赤焰军-2B赋能
                # "https://jira.tuniu.org/rest/greenhopper/1.0/sprintquery/1041?includeHistoricSprints=false&includeFutureSprints=false&_=1578641384145",
                # #财神团-内核
                # "https://jira.tuniu.org/rest/greenhopper/1.0/sprintquery/1043?includeHistoricSprints=false&includeFutureSprints=false&_=1578641337821",
                # #神兽团-应用中台
                # "https://jira.tuniu.org/rest/greenhopper/1.0/sprintquery/1042?includeHistoricSprints=false&includeFutureSprints=false&_=1578641078216",
                #系统产品研发-应用
                "https://jira.tuniu.org/rest/greenhopper/1.0/sprintquery/1079?includeHistoricSprints=false&includeFutureSprints=false&_=1584067681047"]
            # scrumName = [
            #     vers + "_ENH_合作店主线版本" + vers + "_RT_2B中台能力建设" + vers + "_YCY_商旅主线" + vers + "_GCD_合作店服务能力",
            #     vers + "_金蟾_财务标准化" + vers + "_貔貅_支付对账" + vers + "_金鳌_人事财务",
            #     vers + "_奚鼠_酒店资源标准化" + vers + "_鲲鹏_酒店资源标准化" + vers + "_玄武_对客体验" + vers + "_朱雀_工具与营销" + vers + "_麒麟_产品详情页" + vers + "_白虎_金融与保险" + vers + "_白泽_技术支持标准化" + vers + "_山猫_基础服务和框架" + vers + "_凤凰_数据相关" + vers + "_朱雀_工具与营销"]


            scrumName = [
                vers + "_白虎_金融与保险" + vers + "_貔貅_职能应用" + vers + "_鲲鹏_供给应用" + vers + "_火箭军_销售应用" +
                vers + "_朱雀_供给应用" + vers + "_长林军_销售应用" + vers + "_GCD_商旅应用" + vers + "_YCY_商旅应用" + vers + "_玄武_供应链应用" + vers + "_金蟾_职能应用"]

            # 指定团队看板
            # print (scrumName)
            print("=======================根据sprint获取信息===============")
            i = 0
            for url in sprintUrl:
                reportUrls = GetJ.get_SprintId(url, scrumName[i], i)
                # print (reportUrls)
                if len(reportUrls) > 0:

                    pool = ThreadPool(1)
                    # pool.map(GetJ.get_SprintInfo, reportUrls)
                    pool.map(GetJ.get_SprintDate, reportUrls)
                    pool.close()
                    pool.join()
                    i += 1
                    isInsert = True
                else:
                    print("迭代池还未建立开启，请检查后再同步~~")
                    isInsert = False
            # print (isInsert)
            if isInsert == True:
                try:
                    # print(names)
                    namelabeldic = dict(db.session.query(Teamname.name,Teamname.team).filter(Teamname.flag==1).all())
                    # print (namelabeldic)
                    for i in range (0,len(names)):
                        # print (names[i])
                        if names[i] not in namelabeldic.values():
                            if names[i] not in namelabeldic.keys():
                                print ("未搜索到当前迭代组："+names[i])
                            else:
                                names[i] = namelabeldic[names[i]]
                    # print (names)

                    PointsData = pd.DataFrame(
                        {'vers': vers, 'reqnum': sumCnts, 'planpoint': planPoints, 'actualpoint': actPoints,
                         'insertpoint': addPoints,
                         'removpoint': puntedPoints, 'finishrate': Rates, 'bugnum': BugCnts, 'bugrate': bugRates,
                         'team': names})
                    # excelPath = "/AUTOMATION/" + path + ".xlsx"
                    # print(excelPath)
                    print(PointsData)
                except Exception as e:
                    print(e)
                    raise e
                print("====生成DataFrame数据")
                # engine = create_engine('mysql+mysqlconnector://root:tuniu520@localhost/maxdata')

                # thread1 = threading.thread(target=GetJira().insertdata(),args=PointsData)
                # thread1.start()
                # thread1.join()
                hostname = socket.gethostname()
                # logging.info("hostname>>>>>>>>>>>>>>>>>>>>"+hostname)
                if (hostname == 'vm-prd-tnauto-occamrazor-185-170.tuniu.org'):
                    # app = create_app('production')
                    engine = create_engine('mysql+mysqlconnector://root:@MonLey880124@10.28.32.130/pandora')
                    PointsData.to_sql(Scrumteam.__tablename__, con=engine, schema="pandora", index=False,
                                      index_label=False,
                                      if_exists='append', chunksize=1000)
                else:
                    engine = create_engine('mysql+pymysql://root:@MonLey880124@10.28.32.130/auto_platform')
                    PointsData.to_sql(Scrumteam.__tablename__, con=engine, schema="auto_platform", index=False,
                    # PointsData.to_sql(Scrumteam.__tablename__, con=engine, schema="pandora",index=False,
                                      index_label=False,
                                      if_exists='append', chunksize=1000)

                # PointsData.to_sql(Scrumteam.__tablename__, con=engine, schema="maxdata", index=False, index_label=False, if_exists='append', chunksize=1000)
                # print ("ok")
                return "ok"
            else:
                return "迭代池还未建立开启，请检查后再同步~~"
        except Exception as e:
            raise e
            return "同步失败，请检查～～"

if __name__ == '__main__':
    try:

        # jira = JIRA('https://jira.tuniu.org', basic_auth=('zhuhaiyan', 'map.eat-97'))
        # d = jira.fields()
        # print(json.dumps(d))
        #获取当前已启动项目迭代版本
        response = requests.get("https://jira.tuniu.org/rest/greenhopper/1.0/sprintquery/1079?includeHistoricSprints=false&includeFutureSprints=false&_=1578641384145")
        # getcontent = response.text
        # json到字典的转化
        # list_active = []
        dict_content = json.loads(response.text)
        # print(dict_content)
        vers = str(dict_content['sprints'][-1]['name'].split('_')[0])
        # print (vers)
        Scrumteam.query.filter(Scrumteam.vers == vers).delete()
        db.session.commit()
        # thread1 = threading.Thread(target=GetJira().save_Excel,args=vers)
        # thread1.join()
        GetJira().save_Excel(vers)
    except Exception as e:
        print (e)