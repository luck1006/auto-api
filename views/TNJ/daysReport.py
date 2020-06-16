# -*- coding: UTF-8 -*-

import openpyxl
import requests
import time
from bs4 import BeautifulSoup
import pysnooper
import pandas as pd
import time


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


if __name__ == '__main__':
    start_time = '2020-02-10'
    end_time = '2020-02-14'
    jira_tuniu(start_time, end_time, dept_sec='')
