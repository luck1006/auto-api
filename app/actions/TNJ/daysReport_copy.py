# -*- coding: UTF-8 -*-

import openpyxl
import requests
import time
from bs4 import BeautifulSoup
import pysnooper
import pandas as pd
import time, math
from app.models.models import *
from app import  db
from sqlalchemy import and_, or_, distinct, text
from jira import JIRA
# from xpinyin import Pinyin


class queryFromSql(object):

    def __init__(self, Dbname, sql, export=0):
        self.sql = sql
        self.Dbname = Dbname
        self.export = export

    # @pysnooper.snoop('log.log')
    def querySql(self):
        '''
        :param Dbname:
        :param sql:
        :return:list  以[[],[]...] 的形式返回数据
        '''
        url = "http://newsqladmin.tuniu.org/sqladmin"
        headers = {
            'Connection': "keep-alive",
            'Cache-Control': "max-age=0",
            'Upgrade-Insecure-Requests': "1",
            'Content-Type': "application/x-www-form-urlencoded",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'Referer': "http://newsqladmin.tuniu.org/sqladmin",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cookie': "username=xingenlu",
            'Host': "newsqladmin.tuniu.org",
            'Origin': 'http://newsqladmin.tuniu.org'
        }
        if self.Dbname in ['d_mall_booking', 'd_mall_ord', 'd_mall_prd']:
            headers['Cookie'] = 'username=liutaotao'
        times = 0
        endId = 30
        data = []
        key = []
        idx = 0
        print(self.sql)
        while endId == 30:
            print("计数", times)
            # newsqladmin 每次30条记录
            startId = times * 30
            if "limit" not in self.sql and startId != 0:
                # if "limit" not in self.sql:
                Sqlstr = self.sql + f" limit {startId} , 30 "
            else:
                Sqlstr = self.sql
            payload = {
                "Dbname": self.Dbname,
                "Sqlstr": Sqlstr,
                "Sqlstr_hide": None
            }
            retry = 0
            time1 = time.time()
            try:
                time4 = time.time()
                response = requests.post(url, payload, headers=headers)
                print('查询时间：', time.time() - time4)
                time.sleep(0.5)
                while response.status_code != 200 or 'newsqladmin自动kill' in str(response.content, 'utf8'):
                    time.sleep(2)
                    response = requests.post(url, payload, headers=headers)
                    retry += 1
                    print(f"retry{retry}次")
                    if retry > 10:
                        break
            except Exception as e:
                print('exception', response.text)
                raise e
            time2 = time.time()
            print('耗时 ' + str(time2 - time1) + 's')
            soup = BeautifulSoup(response.text, 'lxml')

            # 优化点 后边再看
            # resultset = soup.select('#qryresult tr')
            # print(resultset)

            for idx, tr in enumerate(soup.find_all('tr')):
                tds = tr.find_all('td')
                list = []
                if idx != 0:
                    for c in tds[1:]:
                        # 一堆数据库报错信息的再解释
                        if 'newsqladmin自动kill' in c.text:
                            list.append('查询超时，请优化')
                        elif '执行select语句失败' in c.text:
                            list.append('查询失败，请检查')
                        elif '无该数据库的访问权限' in c.text:
                            list.append('无权限')
                        elif 'sqladmin' in c.text:
                            list.append('查询失败，请检查')
                        else:
                            list.append(c.text)
                    data.append(list)
                elif startId == 0:
                    for c in tds[1:]:
                        key.append(c.text)
                    data.append(key)
            endId = idx
            times = times + 1
            if 'limit' in self.sql.lower():
                break
            # 非jira库 最多查询100条
            if self.Dbname == 'jira' or self.export == 1:
                pass
            else:
                break
        return data

    def tokv(self, data):
        '''
        :param data: [[data1],[],[],...]
        :return: [{key1:value1,...},{},...] key为data1
        '''
        list = []
        keyList = data[0]
        for i in data:
            if i != keyList:
                c = dict(zip(keyList, i))
                list.append(c)
        return list

    def sqlToList(self):
        data = queryFromSql(self.Dbname, self.sql)
        data = data.querySql()
        res = queryFromSql.tokv(self, data)
        return res

    def toexcel(self, sheet_name='Sheet1'):
        data = queryFromSql(self.Dbname, self.sql, 1).querySql()
        df = pd.DataFrame(data[1:], columns=data[0])
        writer = pd.ExcelWriter('result.xlsx')
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        writer.save()


def jira_tuniu(start_time, end_time, dept_sec):
    excelWriter = pd.ExcelWriter('temp.xlsx', engine='openpyxl')

    # 只是为了部门在第一个sheet
    l = pd.DataFrame(['', ''])
    l.to_excel(excelWriter, sheet_name='日报')

    db = 'jira'
    # 查询worklog表中数据
    sql = f'''
    SELECT  b.name_cn AS 姓名, b.dept_sec AS 组织架构, STR_TO_DATE(STARTDATE, '%Y-%m-%d') AS 日期
	,a.timeworked / 3600  AS "工时(h)"
	,a.worklogbody as 工作日志
	, CONCAT(d.pkey, '-', c.issuenum) AS 单号
	,c.SUMMARY as 任务
	, e.pname AS 类型, c.id, g.LINKNAME
	, IF(e.pname IN ('技术需求', '业务需求', '新技术支持'), c.id, f.SOURCE) AS SOURCE
FROM worklog a
	LEFT JOIN t_oa_user b ON a.AUTHOR = b.name_en
	LEFT JOIN jiraissue c ON c.id = a.issueid
	LEFT JOIN project d ON c.PROJECT = d.ID
	LEFT JOIN issuetype e ON c.issuetype = e.id
	LEFT JOIN issuelink f ON f.DESTINATION = c.id
	LEFT JOIN issuelinktype g ON f.LINKTYPE = g.id
WHERE b.dept_fir = '系统产品研发BU'
-- 	AND b.dept_sec in {dept_sec}
	AND e.pname IN ('子事务', 'Sub-task')
	AND g.id = 10100
 -- 取jira为('子事务', 'Sub-task') 链接类型是jira_subtask_link
	AND date(STARTDATE) BETWEEN '{start_time}' AND '{end_time}'
UNION ALL 
SELECT b.name_cn AS 姓名, b.dept_sec AS 组织架构, STR_TO_DATE(STARTDATE, '%Y-%m-%d') AS 日期
	, a.timeworked / 3600 AS "工时(h)"
	, a.worklogbody as 工作日志
	, CONCAT(d.pkey, '-', c.issuenum) AS 单号
	, c.SUMMARY as 任务
	, e.pname AS 类型, c.id, g.LINKNAME
	, IF(e.pname IN ('技术需求', '业务需求', '新技术支持'), c.id, f.SOURCE) AS SOURCE  
	-- 限制父级jira在('技术需求', '业务需求', '新技术支持')
FROM worklog a
	LEFT JOIN t_oa_user b ON a.AUTHOR = b.name_en
	LEFT JOIN jiraissue c ON c.id = a.issueid
	LEFT JOIN project d ON c.PROJECT = d.ID
	LEFT JOIN issuetype e ON c.issuetype = e.id
	LEFT JOIN issuelink f ON f.DESTINATION = c.id
	LEFT JOIN issuelinktype g ON f.LINKTYPE = g.id
WHERE b.dept_fir = '系统产品研发BU'
-- 	AND b.dept_sec in {dept_sec}
	AND e.pname NOT IN ('子事务', 'Sub-task')
    AND date(STARTDATE) BETWEEN '{start_time}' AND '{end_time}'
	-- 取其他jira 此时不限制
    '''
    tmp_data = queryFromSql(db, sql).sqlToList()
    print('111111111111--tmp_data >>>>is: \n', tmp_data)
    data = queryFromSql(db, sql).querySql()
    res = pd.DataFrame(data[1:], columns=data[0])
    ids = res['SOURCE']
    ids = ids.tolist()
    l = list(set(ids))
    ids = ''
    for i in l:
        if i != "":
            ids += i + ','
    ids = ids.strip().strip(',')

    # 查询jra父级相关属性或本身 ('业务需求','技术需求','新技术支持')属性
    sql_2 = f'''
    SELECT distinct c.id AS SOURCE,  CONCAT(d.pkey, '-', c.issuenum) AS 父级jira
        , e.pname AS 类型
    --     , f.SOURCE 父级id
        , c.SUMMARY 主题
        , c.DESCRIPTION  描述,
        (SELECT b.name_cn  FROM customfieldvalue af left join t_oa_user b on b.name_en = af.STRINGVALUE WHERE af.ISSUE=c.ID AND CUSTOMFIELD=10023) AS 需求提出人,
        (SELECT cfd.customvalue FROM customfieldvalue af LEFT JOIN customfieldoption cfd ON cfd.id=af.STRINGVALUE WHERE af.ISSUE=c.ID AND af.CUSTOMFIELD=17905) AS 需求提出部门,
        IFNULL((SELECT cfop.customvalue FROM customfieldvalue cfvp,customfieldoption cfop WHERE c.ID= cfvp.ISSUE AND cfvp.CUSTOMFIELD = 12100 AND cfop.ID = cfvp.STRINGVALUE),'未立项()') AS 立项项目名称,
        (SELECT STRINGVALUE FROM customfieldvalue af WHERE af.ISSUE = c.ID AND CUSTOMFIELD = 10301) Epic
    FROM jiraissue c
        LEFT JOIN  worklog a ON c.id = a.issueid
        LEFT JOIN t_oa_user b ON a.AUTHOR = b.name_en
        LEFT JOIN project d ON c.PROJECT = d.ID
        LEFT JOIN issuetype e ON c.issuetype = e.id
        LEFT JOIN issuelink f ON f.DESTINATION = c.id
    WHERE c.id in ({ids}) AND e.pname in ('业务需求','技术需求','新技术支持')
    '''

    # 序号	ID	LINKNAME	INWARD	OUTWARD	pstyle
    # 1	10000	Blocks	is blocked by	blocks
    # 2	10001	Cloners	is cloned by	clones
    # 3	10002	Duplicate	is duplicated by	duplicates
    # 4	10003	Relates	relates to	relates to
    # 5	10100	jira_subtask_link	jira_subtask_inward	jira_subtask_outward	jira_subtask
    # 6	10200	Epic-Story Link	has Epic	is Epic of	jira_gh_epic_story

    data_2 = queryFromSql(db, sql_2).querySql()
    res_2 = pd.DataFrame(data_2[1:], columns=data_2[0])
    df = pd.DataFrame.merge(res, res_2, how='left', on='SOURCE')

    print("df is >>>>>: \n", df)

    # 取所有的填写工时的人
    members = tuple(set(df['姓名']))

    # 工时列 字符串转数字
    df[['工时(h)']] = df[['工时(h)']].apply(pd.to_numeric)
    d = pd.read_excel('名单.xlsx', sheet_name='Sheet1')
    df = pd.merge(df, d, how='left', on='姓名', left_on=None, right_on=None,
                  left_index=False, right_index=False, sort=True,
                  suffixes=('_x', '_y'), copy=True, indicator=False)
    d2 = pd.read_excel('名单.xlsx', sheet_name='Sheet2')
    fujian_id = tuple(d2['JIRA'])

    pic = f'''
     select concat(p.`pkey`,'-',ji.`issuenum`) JIRA,ji.`SUMMARY`,
    ji.DESCRIPTION as 团队描述,
    concat('https://jira.tuniu.org/browse/',p.`pkey`,'-',ji.`issuenum`) as 团队地址,
    group_concat(concat('https://jira.tuniu.org/secure/attachment/',fm.id,'/', fm.FILENAME)) as 截图,
    date(fm.`CREATED`) as 日期 from `fileattachment` fm
    left join jiraissue ji on fm.`issueid` = ji.`ID`
    left join project p on ji.`PROJECT` = p.`ID`
    where concat(p.`pkey`,'-',ji.`issuenum`) in {fujian_id}
    and date(fm.CREATED)  BETWEEN '{start_time}' AND '{end_time}'
    group by ji.id ,date(fm.`CREATED`)
    order by ji.`SUMMARY`; 
    '''
    data_3 = queryFromSql(db, pic).querySql()
    res_3 = pd.DataFrame(data_3[1:], columns=data_3[0])
    df1 = pd.merge(d2, res_3, how='left', on='JIRA', left_on=None, right_on=None,
                   left_index=False, right_index=False, sort=True,
                   suffixes=('_x', '_y'), copy=True, indicator=False)
    df = pd.merge(df, df1, how='left', on=['ScrumTeam', '日期'], left_on=None, right_on=None,
                  left_index=False, right_index=False, sort=True,
                  suffixes=('_x', '_y'), copy=True, indicator=False)

    print('the last df is >>>>>>: \n', df)

    temp = {}

    # ws.write(i, 1, "=HYPERLINK(\"#sheet2!a{}\")\r".format(i))

    for i in ['姓名', '组织架构', 'ScrumTeam', '日期', '工时(h)', '类型_x', '工作日志', '单号', '任务', '父级jira', '主题', '截图'
              ]:
        temp[i] = df[i]
    d = pd.DataFrame(data=temp)
    d = d.sort_values(by=['组织架构', '姓名'])
    d.to_excel(excelWriter, sheet_name='日报', index=None)

    team = f'''
  select ji.`SUMMARY`as 团队,
    ji.DESCRIPTION as 团队描述,
    concat('https://jira.tuniu.org/browse/',p.`pkey`,'-',ji.`issuenum`) as 团队地址
    from jiraissue ji 
    left join project p on ji.`PROJECT` = p.`ID`
    where concat(p.`pkey`,'-',ji.`issuenum`) in {fujian_id}

    '''

    data_4 = queryFromSql(db, team).querySql()
    res_4 = pd.DataFrame(data_4[1:], columns=data_4[0])
    res_4.to_excel(excelWriter, sheet_name='团队', index=None)

    excelWriter.save()
    excelWriter.close()

def jira_tuniu_copy(start_time, end_time, dept_sec, workers_list):


    db = 'jira'
    # 查询worklog表中数据

    if dept_sec != '':
        sql = f'''
            SELECT  b.name_cn AS worker_name, b.dept_sec AS dept_sec, STR_TO_DATE(STARTDATE, '%Y-%m-%d') AS work_date
            ,a.timeworked / 3600  AS work_time
            ,a.worklogbody as work_log
            , CONCAT(d.pkey, '-', c.issuenum) AS work_id
            ,c.SUMMARY as task
            , e.pname AS work_type, c.id, g.LINKNAME
            , IF(e.pname IN ('技术需求', '业务需求', '新技术支持'), c.id, f.SOURCE) AS SOURCE
        FROM worklog a
            LEFT JOIN t_oa_user b ON a.AUTHOR = b.name_en
            LEFT JOIN jiraissue c ON c.id = a.issueid
            LEFT JOIN project d ON c.PROJECT = d.ID
            LEFT JOIN issuetype e ON c.issuetype = e.id
            LEFT JOIN issuelink f ON f.DESTINATION = c.id
            LEFT JOIN issuelinktype g ON f.LINKTYPE = g.id
        WHERE b.dept_fir = '系统产品研发BU'
            AND b.dept_sec in {dept_sec}
            AND e.pname IN ('子事务', 'Sub-task')
            AND g.id = 10100
         -- 取jira为('子事务', 'Sub-task') 链接类型是jira_subtask_link
            AND STARTDATE BETWEEN '{start_time}' AND '{end_time}'
        UNION ALL 
        SELECT b.name_cn AS worker_name, b.dept_sec AS dept_sec, STR_TO_DATE(STARTDATE, '%Y-%m-%d') AS work_date
            , a.timeworked / 3600 AS "工时(h)"
            , a.worklogbody as work_log
            , CONCAT(d.pkey, '-', c.issuenum) AS work_id
            , c.SUMMARY as task
            , e.pname AS work_type, c.id, g.LINKNAME
            , IF(e.pname IN ('技术需求', '业务需求', '新技术支持'), c.id, f.SOURCE) AS SOURCE  
            -- 限制父级jira在('技术需求', '业务需求', '新技术支持')
        FROM worklog a
            LEFT JOIN t_oa_user b ON a.AUTHOR = b.name_en
            LEFT JOIN jiraissue c ON c.id = a.issueid
            LEFT JOIN project d ON c.PROJECT = d.ID
            LEFT JOIN issuetype e ON c.issuetype = e.id
            LEFT JOIN issuelink f ON f.DESTINATION = c.id
            LEFT JOIN issuelinktype g ON f.LINKTYPE = g.id
        WHERE b.dept_fir = '系统产品研发BU'
            AND b.dept_sec in {dept_sec}
            AND e.pname NOT IN ('子事务', 'Sub-task')
            AND STARTDATE BETWEEN '{start_time}' AND '{end_time}'
            -- 取其他jira 此时不限制
            '''
    elif workers_list != '':   #按scrum_team下的人员名单进行查询
        sql = f'''
                    SELECT  b.name_cn AS worker_name, b.dept_sec AS dept_sec, STR_TO_DATE(STARTDATE, '%Y-%m-%d') AS work_date
                    ,a.timeworked / 3600  AS work_time
                    ,a.worklogbody as work_log
                    , CONCAT(d.pkey, '-', c.issuenum) AS work_id
                    ,c.SUMMARY as task
                    , e.pname AS work_type, c.id, g.LINKNAME
                    , IF(e.pname IN ('技术需求', '业务需求', '新技术支持'), c.id, f.SOURCE) AS SOURCE
                FROM worklog a
                    LEFT JOIN t_oa_user b ON a.AUTHOR = b.name_en
                    LEFT JOIN jiraissue c ON c.id = a.issueid
                    LEFT JOIN project d ON c.PROJECT = d.ID
                    LEFT JOIN issuetype e ON c.issuetype = e.id
                    LEFT JOIN issuelink f ON f.DESTINATION = c.id
                    LEFT JOIN issuelinktype g ON f.LINKTYPE = g.id
                WHERE b.dept_fir = '系统产品研发BU'
                    AND b.name_cn in {workers_list}
                    AND e.pname IN ('子事务', 'Sub-task')
                    AND g.id = 10100
                 -- 取jira为('子事务', 'Sub-task') 链接类型是jira_subtask_link
                    AND STARTDATE BETWEEN '{start_time}' AND '{end_time}'
                UNION ALL 
                SELECT b.name_cn AS worker_name, b.dept_sec AS dept_sec, STR_TO_DATE(STARTDATE, '%Y-%m-%d') AS work_date
                    , a.timeworked / 3600 AS "工时(h)"
                    , a.worklogbody as work_log
                    , CONCAT(d.pkey, '-', c.issuenum) AS work_id
                    , c.SUMMARY as task
                    , e.pname AS work_type, c.id, g.LINKNAME
                    , IF(e.pname IN ('技术需求', '业务需求', '新技术支持'), c.id, f.SOURCE) AS SOURCE  
                    -- 限制父级jira在('技术需求', '业务需求', '新技术支持')
                FROM worklog a
                    LEFT JOIN t_oa_user b ON a.AUTHOR = b.name_en
                    LEFT JOIN jiraissue c ON c.id = a.issueid
                    LEFT JOIN project d ON c.PROJECT = d.ID
                    LEFT JOIN issuetype e ON c.issuetype = e.id
                    LEFT JOIN issuelink f ON f.DESTINATION = c.id
                    LEFT JOIN issuelinktype g ON f.LINKTYPE = g.id
                WHERE b.dept_fir = '系统产品研发BU'
                    AND b.name_cn in {workers_list}
                    AND e.pname NOT IN ('子事务', 'Sub-task')
                    AND STARTDATE BETWEEN '{start_time}' AND '{end_time}'
                    -- 取其他jira 此时不限制
                    '''

    else:   #查询所有，不指定dept_sec 和 srcum_team
        sql = f'''
                    SELECT  b.name_cn AS worker_name, b.dept_sec AS dept_sec, STR_TO_DATE(STARTDATE, '%Y-%m-%d') AS work_date
                    ,a.timeworked / 3600  AS work_time
                    ,a.worklogbody as work_log
                    , CONCAT(d.pkey, '-', c.issuenum) AS work_id
                    ,c.SUMMARY as task
                    , e.pname AS work_type, c.id, g.LINKNAME
                    , IF(e.pname IN ('技术需求', '业务需求', '新技术支持'), c.id, f.SOURCE) AS SOURCE
                FROM worklog a
                    LEFT JOIN t_oa_user b ON a.AUTHOR = b.name_en
                    LEFT JOIN jiraissue c ON c.id = a.issueid
                    LEFT JOIN project d ON c.PROJECT = d.ID
                    LEFT JOIN issuetype e ON c.issuetype = e.id
                    LEFT JOIN issuelink f ON f.DESTINATION = c.id
                    LEFT JOIN issuelinktype g ON f.LINKTYPE = g.id
                WHERE b.dept_fir = '系统产品研发BU'
                    AND e.pname IN ('子事务', 'Sub-task')
                    AND g.id = 10100
                 -- 取jira为('子事务', 'Sub-task') 链接类型是jira_subtask_link
                    AND STARTDATE BETWEEN '{start_time}' AND '{end_time}'
                UNION ALL 
                SELECT b.name_cn AS worker_name, b.dept_sec AS dept_sec, STR_TO_DATE(STARTDATE, '%Y-%m-%d') AS work_date
                    , a.timeworked / 3600 AS "工时(h)"
                    , a.worklogbody as work_log
                    , CONCAT(d.pkey, '-', c.issuenum) AS work_id
                    , c.SUMMARY as task
                    , e.pname AS work_type, c.id, g.LINKNAME
                    , IF(e.pname IN ('技术需求', '业务需求', '新技术支持'), c.id, f.SOURCE) AS SOURCE  
                    -- 限制父级jira在('技术需求', '业务需求', '新技术支持')
                FROM worklog a
                    LEFT JOIN t_oa_user b ON a.AUTHOR = b.name_en
                    LEFT JOIN jiraissue c ON c.id = a.issueid
                    LEFT JOIN project d ON c.PROJECT = d.ID
                    LEFT JOIN issuetype e ON c.issuetype = e.id
                    LEFT JOIN issuelink f ON f.DESTINATION = c.id
                    LEFT JOIN issuelinktype g ON f.LINKTYPE = g.id
                WHERE b.dept_fir = '系统产品研发BU'
                    AND e.pname NOT IN ('子事务', 'Sub-task')
                    AND STARTDATE BETWEEN '{start_time}' AND '{end_time}'
                    -- 取其他jira 此时不限制
                    '''

    data = queryFromSql(db, sql).querySql()
    res = pd.DataFrame(data[1:], columns=data[0])

    print('rest is :\n',res)
    try:
        ids = res['SOURCE']
    except Exception as e:
        print('查询结果为：\n ',res)
        ids = ''
    else:
        ids = ids.tolist()
        l = list(set(ids))
        ids = ''
        for i in l:
            if i != "":
                ids += i + ','
        ids = ids.strip().strip(',')

    # 查询jra父级相关属性或本身 ('业务需求','技术需求','新技术支持')属性

    sql_2 = f'''
        SELECT distinct c.id AS SOURCE,  CONCAT(d.pkey, '-', c.issuenum) AS parent_jira
        --   , e.pname AS work_type
        --     , f.SOURCE parent_id
            , c.SUMMARY summary
            , c.DESCRIPTION  description,
            (SELECT b.name_cn  FROM customfieldvalue af left join t_oa_user b on b.name_en = af.STRINGVALUE WHERE af.ISSUE=c.ID AND CUSTOMFIELD=10023) AS demand_proposer,
            (SELECT cfd.customvalue FROM customfieldvalue af LEFT JOIN customfieldoption cfd ON cfd.id=af.STRINGVALUE WHERE af.ISSUE=c.ID AND af.CUSTOMFIELD=17905) AS demand_dept,
            IFNULL((SELECT cfop.customvalue FROM customfieldvalue cfvp,customfieldoption cfop WHERE c.ID= cfvp.ISSUE AND cfvp.CUSTOMFIELD = 12100 AND cfop.ID = cfvp.STRINGVALUE),'未立项()') AS project_name,
            (SELECT STRINGVALUE FROM customfieldvalue af WHERE af.ISSUE = c.ID AND CUSTOMFIELD = 10301) Epic
        FROM jiraissue c
            LEFT JOIN  worklog a ON c.id = a.issueid
            LEFT JOIN t_oa_user b ON a.AUTHOR = b.name_en
            LEFT JOIN project d ON c.PROJECT = d.ID
            LEFT JOIN issuetype e ON c.issuetype = e.id
            LEFT JOIN issuelink f ON f.DESTINATION = c.id
        WHERE c.id in ({ids}) AND e.pname in ('业务需求','技术需求','新技术支持')
        '''

    data2 = queryFromSql(db, sql).sqlToList()
    print('the data2 is : \n',data2)
    data3 = queryFromSql(db, sql_2).sqlToList()
    print('the data3 is : \n', data3)
    # print(len(data2), len(data3))
    data4=[]

    #若非查询到对应父级，则以下字段默认显示为空
    init_paraent_jira = {'parent_jira': '', 'summary': '', 'description': '', 'demand_proposer': '', 'demand_dept': '', 'project_name': '', 'Epic': ''}

    #将data3、data4字段数据合并
    temp_unmerged_list = []   #临时存放未合并的data3中的元素

    if data2 != [{'错误信息': '查询失败，请检查'}] and data3 != [{'错误信息': '查询失败，请检查'}]:
        for x in data2:
            x_times = 0
            for y in data3:
                if x['SOURCE'] == y['SOURCE']:
                    data4.append(dict(x,**y))
                    x_times+=1
            if x_times == 0:
                temp_unmerged_list.append(x)

        if len(temp_unmerged_list) > 0:   #为找到父级的记录，对应字段默认为空
            for i in temp_unmerged_list:
                data4.append(dict(i,**init_paraent_jira))
    elif data2 != [{'错误信息': '查询失败，请检查'}]:
        for x in data2:
            data4.append(dict(x, **init_paraent_jira))

    print('the end date4 is : \n',data4, '\n', len(data4))


    #结果数据实现按姓名排序
    # pin = Pinyin()
    # result = []
    # result_data = []
    # for item in data4:
    #     result.append((pin.get_pinyin(item['worker_name']), item))
    # result.sort()
    #
    # for i in range(len(result)):
    #     result_data.append(result[i][1])
    # print('pinyin sort >>>>>:\n', result_data)

    return data4

def getWorkersFromScrum(scrumTeam):
    # workers = Worker_ScrumTeam.query.filter(and_(Worker_ScrumTeam.scrum_team==scrumTeam,Worker_ScrumTeam.status==True)).all()
    workers = db.session.query(Worker_ScrumTeam.worker_name).filter(and_(Worker_ScrumTeam.scrum_team==scrumTeam,Worker_ScrumTeam.status==True)).all()
    # print(workers)

    # workers_str = '('
    # if workers is not None:
    #     for worker in workers:
    #         workers_str += "'" + worker[0] + "',"
    #     workers_str = workers_str[:-1] + ')'
    # else:
    #     workers_str = ''
    # print(workers_str)
    # return  workers_str
    workers_list = []
    if workers is not None:
        for worker in workers:
            workers_list.append(worker[0])
    # print(workers_list)
    return workers_list

def get_Worker_Scrum_rel():
    workers = db.session.query(Worker_ScrumTeam.worker_name,Worker_ScrumTeam.scrum_team).filter(Worker_ScrumTeam.status==True).all()
    print(workers)

    if workers is not None:
        return workers
    else:
        return None

# 定义燃尽图相关类
class BurnDown():
    def __init__(self):
        self.name = 'dongfangfang'
        self.password = 'eat.art.dff-0312'
        self.rapidViewId = 1079   #定义看板id,jira如有变动，此处要修改
        jira = JIRA('https://jira.tuniu.org', basic_auth=(self.name,self.password))
        JSESSIONID = jira.session(auth=(self.name,self.password)).raw['session']['value']
        self.header = {"Accept": "*/*",
                   "Accept-Encoding": "gzip,deflate",
                   "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
                   "Connection": "keep-alive",
                   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
                   # "Referer": "https://jira.tuniu.org/secure/RapidBoard.jspa?rapidView=294&view=reporting&chart=burndownChart&sprint=" + str(sprintId),
                  "X - AUSERNAME": "dongfangfang",
                   "Cookie": "seraph.rememberme.cookie=138865%3A35e3e1d4b4085add6adf45c84c0b1b4413fc1216; atlassian.xsrf.token=BUUK-J6AN-FDNV-PLO6|8c2ebabda16b6d3ce5f882b9e60973b6276103df|lin; JSESSIONID=" + JSESSIONID}

    def jira_scopechangeburndownchart(self,sprintId=4525):
        url = "https://jira.tuniu.org/rest/greenhopper/1.0/rapid/charts/scopechangeburndownchart.json?rapidViewId=1079&sprintId=" + str(sprintId)
        response = requests.get(url,headers=self.header).content
        return(json.loads(response,encoding='utf-8'))

    def jira_sprintQuery(self):
        url = "https://jira.tuniu.org/rest/greenhopper/1.0/sprintquery/" + str(self.rapidViewId)+ "?includeHistoricSprints=false&includeFutureSprints=false"
        response = requests.get(url,headers=self.header).content
        return json.loads(response,encoding='utf-8')


#将13位时间chuo转换成标准时间
def timeStamp(timeNum):
    timeStamp = float(int(timeNum)/1000 - 28800) # 减去28800,否则会晚8小时
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    # print(otherStyleTime)
    return otherStyleTime

def dateStamp(timeNum):
    timeStamp = float(int(timeNum)/1000 - 28800) # 减去28800,否则会晚8小时
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    # print(otherStyleTime)
    return otherStyleTime

#将日期转成13位时间chuo
def get_time_stamp13(datetime_obj):
    # print('the datetime_obj:',datetime_obj )

    dt = datetime.datetime.strptime(str(datetime_obj), '%Y-%m-%d %H:%M:%S')  # result从数据库中读出来的标准格式时间数据
    # # 10位，时间点相当于从1.1开始的当年时间编号
    date_stamp = str(int(time.mktime(dt.timetuple()))+28800)
    # # 3位，微秒
    data_microsecond = str("%06d" % dt.microsecond)[0:3]
    # date_stamp是个列表，将每个date_stamp逐个append到列表列表中再写入到数据库里，或者每个直接写入
    date_stamp = date_stamp + data_microsecond

    return int(date_stamp)


def secToHour(seconds):
    day = 24 * 60 * 60
    hour = 60 * 60
    min = 60
    if seconds < 60:
        return "%d sec" % math.ceil(seconds)
    elif seconds > day:
        days = divmod(seconds, day)
        return "%d days, %s" % (int(days[0]), secToHour(days[1]))
    elif seconds > hour:
        hours = divmod(seconds, hour)
        return '%d hours, %s' % (int(hours[0]), secToHour(hours[1]))
    else:
        mins = divmod(seconds, min)
        return "%d mins, %d sec" % (int(mins[0]), math.ceil(mins[1]))


if __name__ == '__main__':
    start_time = '2020-02-14'
    end_time = '2020-02-14'
    workers_list = "('李海红','王慧勇','赵君8','李冒妍2','赵茜5','李风明','赵阳3','董芳芳')"

    # jira_tuniu(start_time, end_time, dept_sec="('质量TeamS')")
    # jira_tuniu_copy(start_time, end_time, dept_sec='', workers_list=workers_list)
    # jira_tuniu(start_time, end_time, dept_sec='')

    # getWorkersFromScrum('玄武')
    # get_Worker_Scrum_rel()
    print(timeStamp(1583971200000))
    print(dateStamp(1584003600000))
    print(timeStamp(1583971200000))
    # print(secToHour(28800))
    # jira_scopechangeburndownchart()

    print(get_time_stamp13(dateStamp(1584003600000)+' 00:00:00'))