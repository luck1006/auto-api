#  -*-  coding: utf-8  -*-
import json
from app.actions.tools.queryFromSql import queryFromSql
import pandas as pd
import numpy as np
import openpyxl


# 官方数据库文档
# "https://confluence.atlassian.com/display/JIRA040/Database+Schema"
class Tn_JIRA():

    def __init__(self, db='jira', **args):
        self.db = db
        self.args = args

    @staticmethod
    def get_sprint():
        '''
        # 当前激活状态的sprint
        '''
        sql = F'''
        select id,name from AO_60DB71_SPRINT where CLOSED = 0 and RAPID_VIEW_ID in (1079) and STARTED =1 order by RAPID_VIEW_ID,NAME desc
        '''
        d = queryFromSql('jira', sql).sqlToList()
        print(d)
        return d

    def get_epic_name(self):
        sql = ''' select c.STRINGVALUE  from  customfieldvalue where CUSTOMFIELD = 10304 '''
        d = queryFromSql('jira', sql).sqlToList()
        return d

    @staticmethod
    def get_work_time_info(sprint):
        if sprint == 'all':
            all_sprint = Tn_JIRA.get_sprint()
            sprint = tuple([i['name'] for i in all_sprint])
            where = f'''
                         AND sprint.NAME in {sprint} 
                        '''
        elif sprint != None:
            where = f'''
             AND sprint.NAME = '{sprint}'
            '''
        sql = F'''   
SELECT 
    (select STRINGVALUE from  customfieldvalue where CUSTOMFIELD = 10304 and ISSUE = epic.id ) as "Epic"
    , IFNUll(epic.summary,'其他') AS "epic 概要"
    , sprint.NAME AS 'Sprint'
	, CONCAT(pro.pkey, '-', story.issuenum) AS "Story"
    , status.pname as "Story状态" 
	, story.SUMMARY AS "概要", itd.pname AS "任务类型"
    , user.name_cn AS "经办人"
	, CONCAT(pro.pkey, '-', task.issuenum) AS "task"
    , task.summary as "子任务"
    , IFNULL(task.timeoriginalestimate, 0) / 28800 AS "预估工作量"
	, IFNULL(task.timespent, 0) / 28800 AS "已完成工作量"
    , IFNULL(task.timeestimate, 0) / 28800 AS "剩余工作量",
    case when (IFNULL(task.timespent, 0) / 28800 ) -  (IFNULL(task.timeoriginalestimate, 0) / 28800)<=0
         then 0
         else (IFNULL(task.timespent, 0) / 28800 )-  (IFNULL(task.timeoriginalestimate, 0) / 28800) end
    as '超预估工作量'
FROM customfieldvalue c
	LEFT JOIN jiraissue story ON story.ID = c.ISSUE
    left join issuestatus  status on story.issuestatus = status.id
	LEFT JOIN AO_60DB71_SPRINT sprint ON sprint.ID = c.STRINGVALUE
	LEFT JOIN issuetype it ON it.id = story.issuetype
	LEFT JOIN issuelink stlink ON stlink.source = story.id
	LEFT JOIN jiraissue task ON task.id = stlink.destination
	LEFT JOIN issuetype itd ON itd.id = task.issuetype
	LEFT JOIN issuelink eslink ON eslink.destination = story.id
	LEFT JOIN jiraissue epic ON epic.id = eslink.source
	LEFT JOIN project pro ON task.PROJECT = pro.ID
	LEFT JOIN t_oa_user user ON user.name_en = task.ASSIGNEE
WHERE (stlink.linktype = 10100
	AND eslink.linktype = 10200
	{where}
	)
ORDER BY epic.id, CONCAT(pro.pkey, '-', task.issuenum)
        '''
        d = queryFromSql('jira', sql).querySql()
        return d

    @staticmethod
    def get_work_time_by_sprint(sprint):
        tnjira = Tn_JIRA()
        data = tnjira.get_work_time_info(sprint)
        detail = pd.DataFrame(data[1:], columns=data[0])
        # 数字类型转换
        num = ['剩余工作量', '预估工作量', '已完成工作量', '超预估工作量']
        for i in num:
            detail[i] = detail[i].astype(float)
        return detail


if __name__ == '__main__':
    excelWriter = pd.ExcelWriter('aaa.xlsx', engine='openpyxl')
    # l = pd.DataFrame(['', ''])
    # l.to_excel(excelWriter, sheet_name='epic')
    # tnjira = Tn_JIRA(ver='10.24.0')
    # data = tnjira.get_work_time_by_epic()
    # detail = pd.DataFrame(data[1:], columns=data[0])
    # detail.to_excel(excelWriter, sheet_name='明细', index=False)
    # excelWriter.save()
    # 数字类型转换
    # num = ['剩余工作量', '预估工作量', '已完成工作量', '超预估工作量']
    # for i in num:
    #     detail[i] = detail[i].astype(float)
    detail = pd.read_excel(excelWriter, sheet_name='epic')
    detail_json = detail.to_json(orient='table')
    print(detail.to_json())

    # print('Epic josn', detail['Epic'].to_json())
    df = detail.groupby(['Sprint', 'Epic', '概要', 'Story状态'])['预估工作量', '已完成工作量', '剩余工作量', '超预估工作量'].sum().reset_index()
    # detail.to_excel(excelWriter, sheet_name='明细', index=False)
    # df.to_excel(excelWriter, sheet_name='epic', index=False)
    df1 = pd.DataFrame(data=[detail['Epic'], detail['预估工作量']], columns=['Epic', '预估工作量'])
    # print(df1.to_json())

    # d  = np.random.randint(low=0, high=10, size=(5, 5))
    # print(d)
    # print(type(d))
    # df1.to_excel(excelWriter, sheet_name='s', index=False)

    # detail.to_excel(excelWriter, sheet_name='明细', index=False)
    # df.to_excel(excelWriter, sheet_name='epic', index=False)
    # excelWriter.save()
