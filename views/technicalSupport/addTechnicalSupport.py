# -*- coding: utf-8 -*-
# TIME:         7.4
# Author:       zhangwen3
# Explain：     获取本周技术支持数据，插入数据库中

import datetime
from jira import JIRA
import json
from app.models.models import *
from flask import Blueprint


#设置蓝图
addTechnical = Blueprint('addTechnical', __name__)

@addTechnical.route('/addTechnical')
def addTechnicalSupport():
    a = nowtime()
    now_time = a[0]
    start = a[2]
    end = a[3]
    week = a[5]
    insert_data_list = get_insert_data(week,start,end)
    adddata = AddData()
    adddata.add_data(insert_data_list)
    return "数据新增成功！"



#计算时间，当前周，当前周的开始时间和结束时间
def nowtime():
    now_time = datetime.datetime.now()
    day=now_time.weekday()    #返回一个星期的第几天
    start_time = now_time + datetime.timedelta(days=-day - 3)
    start_time = start_time.date()
    start = start_time.strftime('%Y-%m-%d')
    end_time = now_time+datetime.timedelta(4-day)
    end_time = end_time.date()
    end = end_time.strftime('%Y-%m-%d')
    week = int(datetime.datetime.now().strftime('%U'))+1
    return now_time,end_time,start,end,day,week

class GetJira():
    def __init__(self,homesystem,start,end):
        #初始化jira链接
        self.jira =JIRA('http://jira.tuniu.org',basic_auth=('zhangwen3','005381@nzc8'))
        self.homesystem = homesystem
        self.start = start
        self.end = end
        '''
        if(self.homesystem!='(其他)'):
            self.sql1=f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in {self.homesystem} AND created > {start} AND created <= {end}'
            self.sql2=f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in {self.homesystem} AND status = resolved AND resolved > {start} AND resolved <= {end}'
            self.sql3=f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in {self.homesystem} AND status in (待系统负责人审批, "In Progress", Reopened, 确认中, 延期, 延期判断) AND created >= {start} AND created <= {end}'
            self.sql4=f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in {self.homesystem} AND status in (待系统负责人审批, "In Progress", Reopened, 确认中, 延期, 延期判断)'
        else:
            self.sql1 =f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in cascadeOption(线上BU-系统产品研发, 其他) AND created > {start} AND created <= {end}'
            self.sql2 =f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in cascadeOption(线上BU-系统产品研发, 其他) AND status = resolved AND resolved > {start} AND resolved <= {end}'
            self.sql3 =f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in cascadeOption(线上BU-系统产品研发, 其他) AND status in (待系统负责人审批, "In Progress", Reopened, 确认中, 延期, 延期判断) AND created >= {start} AND created <= {end}'
            self.sql4 =f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in cascadeOption(线上BU-系统产品研发, 其他) AND status in (待系统负责人审批, "In Progress", Reopened, 确认中, 延期, 延期判断)'
        '''

    def get_newnum(self):
        newnum = 0
        if(self.homesystem!='(其他)'):
            self.sql1=f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in {self.homesystem} AND created > {self.start} AND created <= {self.end}'
            technicalsupport=self.jira.search_issues(self.sql1,maxResults=False)
            newnum = len(technicalsupport)
        else:
            self.sql1 =f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in cascadeOption(线上BU-系统产品研发, 其他) AND created > {self.start} AND created <= {self.end}'
            technicalsupport = self.jira.search_issues(self.sql1, maxResults=False)
            newnum = len(technicalsupport)
        print('newnum',newnum)
        return newnum

    def get_closenum(self):
        closenum = 0
        if(self.homesystem!='(其他)'):
            self.sql2=f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in {self.homesystem} AND status = resolved AND resolved > {self.start} AND resolved <= {self.end}'
            technicalsupport = self.jira.search_issues(self.sql2, maxResults=False)
            closenum = len(technicalsupport)
        else:
            self.sql2 =f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in cascadeOption(线上BU-系统产品研发, 其他) AND status = resolved AND resolved > {self.start} AND resolved <= {self.end}'
            technicalsupport = self.jira.search_issues(self.sql2, maxResults=False)
            closenum = len(technicalsupport)
        print('closenum',closenum)
        return closenum

    def get_unsolvednum(self):
        unsolvednum = 0
        if (self.homesystem != '(其他)'):
            self.sql3=f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in {self.homesystem} AND status in (待系统负责人审批, "In Progress", Reopened, 确认中, 延期, 延期判断) AND created >= {self.start} AND created <= {self.end}'
            technicalsupport = self.jira.search_issues(self.sql3, maxResults=False)
            unsolvednum = len(technicalsupport)
        else:
            self.sql3 =f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in cascadeOption(线上BU-系统产品研发, 其他) AND status in (待系统负责人审批, "In Progress", Reopened, 确认中, 延期, 延期判断) AND created >= {self.start} AND created <= {self.end}'
            technicalsupport = self.jira.search_issues(self.sql3, maxResults=False)
            unsolvednum = len(technicalsupport)
        print('unsolvednum',unsolvednum)
        return unsolvednum

    def get_hisunsolvednum(self):
        hisunsolvednum = 0
        if (self.homesystem != '(其他)'):
            self.sql4=f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in {self.homesystem} AND status in (待系统负责人审批, "In Progress", Reopened, 确认中, 延期, 延期判断)'
            technicalsupport = self.jira.search_issues(self.sql4, maxResults=False)
            hisunsolvednum = len(technicalsupport)
        else:
            self.sql4 =f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in cascadeOption(线上BU-系统产品研发, 其他) AND status in (待系统负责人审批, "In Progress", Reopened, 确认中, 延期, 延期判断)'
            technicalsupport = self.jira.search_issues(self.sql4, maxResults=False)
            hisunsolvednum = len(technicalsupport)
        print('hisunsolvednum',hisunsolvednum)
        return hisunsolvednum


def get_insert_data(week,start,end):
    g = {"order":'(Boss3订单系统, 分单系统)',"supplychain":'(产品系统, 资源系统, 库存系统, 采购系统, 投诉质检, NB系统, 出团通知, BOH)',"ticket":'(门票系统)',"member":'(crm系统, 会员系统)',"market":'(营销)',"confirm":'(确认管理)',"other":'(其他)',"all":"(Boss3订单系统, 分单系统,产品系统, 资源系统, 库存系统, 采购系统, 投诉质检, NB系统, 出团通知, BOH,确认管理,门票系统,crm系统, 会员系统,营销)"}
    insert_data_list=[]
    for k,v in g.items():
        lasthisunsolvednum = db.session.query(Technical_Support.hisunsolvednum).filter(Technical_Support.week==(week-1)).filter(Technical_Support.name == k).filter(Technical_Support.del_flag==0).all()[0][0]
        data={}
        GetjiraJ = GetJira(v,start,end)
        data['name'] = k
        data['week'] = week
        data["newnum"] = GetjiraJ.get_newnum()
        data["closenum"] = GetjiraJ.get_closenum()
        data["unsolvednum"] = GetjiraJ.get_unsolvednum()
        data["hisunsolvednum"] = GetjiraJ.get_hisunsolvednum()
        if((lasthisunsolvednum+GetjiraJ.get_newnum())!=0):
            data["resolutionrate"] =(lasthisunsolvednum+GetjiraJ.get_newnum()-GetjiraJ.get_hisunsolvednum())/(lasthisunsolvednum+GetjiraJ.get_newnum())
        insert_data_list.append(data)
    return insert_data_list

class AddData():
    #插入数据前检查数据库中是否已经存在本周数据，如果存在就逻辑删除
    def check_data(self,insert_data):
        for i in insert_data:
            s = db.session.query(Technical_Support.id).filter(Technical_Support.year==int(datetime.datetime.now().year)).filter(Technical_Support.name==list(i.values())[0]).filter(Technical_Support.week==list(i.values())[1]).all()
            for j in s:
                support=Technical_Support(id=j[0],del_flag=1)
                db.session.merge(support)

    #插入查询到的数据
    def insert_data_batch(self,insert_data):
        db.session.execute(Technical_Support.__table__.insert(),insert_data)


    def add_data(self,insert_data):
        try:
            self.check_data(insert_data)
            self.insert_data_batch(insert_data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()


'''
if __name__ == '__main__':
    a = nowtime()
    now_time = a[0]
    start = a[2]
    end = a[3]
    week = a[5]

    insert_data_list = get_insert_data(week)
    adddata = AddData()
    adddata.add_data(insert_data_list)
'''










