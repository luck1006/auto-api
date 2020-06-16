#  -*-  coding: utf-8  -*-
import json
from app.actions.TNJ.jira_conf import execute
import time

# 查项目下所有的jira, 按照有没有父及jira区分
# 1 技术需求,业务需求,事务
# 2 子需求，子事务，Sub-task
query_by_project = '''
SELECT ji.issuenum, it.pname AS issuetype, ji.summary, concat(pepic.pkey,'-',jifa.issuenum,' ', cfv.STRINGVALUE) AS epic, user.dept_fir
	, dept_sec, dept_thi, user.name_cn, wl.worklogbody, ifnull(wl.timeworked,0)/28800 as timeworked
FROM jiraissue ji
	LEFT JOIN issuelink sub ON sub.DESTINATION = ji.id
	LEFT JOIN jiraissue jifa ON jifa.id = sub.SOURCE
	LEFT JOIN project p ON p.ID = ji.PROJECT
	left join project pepic on pepic.id  =jifa.PROJECT
	LEFT JOIN issuetype it ON it.id = ji.issuetype
	LEFT JOIN customfieldvalue cfv
	ON cfv.issue = jifa.id
		AND cfv.CUSTOMFIELD = 10304
	LEFT JOIN worklog wl ON ji.id = wl.issueid
	LEFT JOIN t_oa_user user ON user.name_en = wl.AUTHOR
WHERE p.pkey IN ('AMID')
	AND ji.issuetype IN (12100, 25, 10300) 
UNION ALL
SELECT ji.issuenum, it.pname AS issuetype, ji.summary, concat(pepic.pkey,'-',epic.issuenum,' ', cfv.STRINGVALUE) AS epic, user.dept_fir
	, dept_sec, dept_thi, user.name_cn, wl.worklogbody,  ifnull(wl.timeworked,0)/28800 as timeworked
FROM jiraissue ji
	LEFT JOIN issuelink sub ON sub.DESTINATION = ji.id
	LEFT JOIN jiraissue jifa ON jifa.id = sub.SOURCE
	LEFT JOIN project p ON p.id = jifa.project
	LEFT JOIN issuetype it ON it.id = ji.issuetype
	LEFT JOIN issuelink epicl ON epicl.DESTINATION = jifa.id
	LEFT JOIN jiraissue epic ON epicl.source = epic.id
	left join project pepic on pepic.id  =epic.PROJECT
	LEFT JOIN customfieldvalue cfv
	ON cfv.issue = epic.id
		AND cfv.CUSTOMFIELD = 10304
	LEFT JOIN worklog wl ON ji.id = wl.issueid
	LEFT JOIN t_oa_user user ON user.name_en = wl.AUTHOR
WHERE ji.issuetype IN (10302, 10301, 5)  
	AND p.pkey IN ('AMID')
'''


# 按月查询epic投入

query_epicby_month = '''
select concat(month,'M') as month,epic,sum(timeworked) as timeworded from (SELECT month(wl.created) as month, concat(pepic.pkey,'-',jifa.issuenum,' ', cfv.STRINGVALUE) AS epic, 
dept_sec, ifnull(wl.timeworked,0)/28800 as timeworked
FROM jiraissue ji
LEFT JOIN issuelink sub ON sub.DESTINATION = ji.id
LEFT JOIN jiraissue jifa ON jifa.id = sub.SOURCE
LEFT JOIN project p ON p.ID = ji.PROJECT
left join project pepic on pepic.id  =jifa.PROJECT
LEFT JOIN issuetype it ON it.id = ji.issuetype
LEFT JOIN customfieldvalue cfv
ON cfv.issue = jifa.id
AND cfv.CUSTOMFIELD = 10304
LEFT JOIN worklog wl ON ji.id = wl.issueid
LEFT JOIN t_oa_user user ON user.name_en = wl.AUTHOR
WHERE p.pkey IN ('AMID') 
AND ji.issuetype IN (12100, 25, 10300) 
UNION all
SELECT month(wl.created) as month, concat(pepic.pkey,'-',epic.issuenum,' ', cfv.STRINGVALUE) AS epic
, dept_sec, ifnull(wl.timeworked,0)/28800 as timeworked
FROM jiraissue ji
LEFT JOIN issuelink sub ON sub.DESTINATION = ji.id
LEFT JOIN jiraissue jifa ON jifa.id = sub.SOURCE
LEFT JOIN project p ON p.id = jifa.project
LEFT JOIN issuetype it ON it.id = ji.issuetype
LEFT JOIN issuelink epicl ON epicl.DESTINATION = jifa.id
LEFT JOIN jiraissue epic ON epicl.source = epic.id
left join project pepic on pepic.id  =epic.PROJECT
LEFT JOIN customfieldvalue cfv
ON cfv.issue = epic.id
AND cfv.CUSTOMFIELD = 10304
LEFT JOIN worklog wl ON ji.id = wl.issueid
LEFT JOIN t_oa_user user ON user.name_en = wl.AUTHOR
WHERE ji.issuetype IN (10302, 10301, 5)  
AND p.pkey IN ('AMID') ) a  where month is not null group by month,epic order by month
'''

if __name__ == '__main__':
    sql = query_by_project
    time1 = time.time()
    d = execute(sql)
    print(json.dumps(d))
    time2 = time.time()
    print(time2 - time1)
