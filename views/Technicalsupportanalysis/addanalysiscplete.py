#./user/bin/python
#coding=UTF_8
import datetime
from jira import JIRA
import json
from app.models.models import *
from flask import Blueprint

#设置蓝图
adycpletes = Blueprint('addcpletes1', __name__)
@adycpletes.route('/addcpletes2',methods=['GET'])
def addcpletes2():
    a = nowtime()
    now_time = a[0]
    start = a[3]
    end = a[4]
    week = a[6]
    h=getdata_cplete(week,start,end)
    add=AddData()
    add.add_data(h)
    response = {"success": "true", "msg": "OK", "data":"数据新增成功"}
    response = json.dumps(response)
    return response

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
    return now_time,start_time,end_time,start,end,day,week

#查询表中系统的各个模块
def getmodule(systemname1):
    mymodule=[]
    mymodule1=[]
    mymodule=db.session.query(Support_module.module_id).filter(Support_module.systemname==systemname1).all()
    #从数据库取出的每个记录都默认格式为数组('crm.会员标签',)，所以需要处理一下
    for i in mymodule:
        m=i[0]
        mymodule1.append(m)
    return mymodule1

#查询jira
class getnum():
    def __init__(self,systemname1,start,end,mudules=[]):
        #初化jira链接
        self.jira =JIRA('http://jira.tuniu.org',basic_auth=('zhangshanshan3','zss@1234.com'))
        self.start=start
        self.end=end
        self.systemname1=systemname1
        self.mudules=mudules

#获取模块临时解决的模块技术支持总数
    def get_mudulenum_cplete_0(self):
        d2=dict()
        newnum2=0
        for i in self.mudules:
            #JQL语句中有错误： '\+' 是无效的JQL转义字符。 正确的转义字符写法是 \', \", \t, \n, \r, \, '\ ' 和 \uXXXX.
             if(i=='allmodules'):
               sql1=f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in ({self.systemname1})AND updated > {self.start} AND updated <= {self.end} AND 根本解决？ = 临时解决'
             else:
               sql1=f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in ({self.systemname1}) AND labels={i} AND updated > {self.start} AND updated <= {self.end} AND 根本解决？ = 临时解决'
             technicalsupport=self.jira.search_issues(sql1,maxResults=False)
             newnum2 = len(technicalsupport)
             d2[i]=newnum2
        return d2

#获取模块临时解决的模块技术支持总数
    def get_mudulenum_cplete_1(self):
        d2=dict()
        newnum2=0
        for i in self.mudules:
            #JQL语句中有错误： '\+' 是无效的JQL转义字符。 正确的转义字符写法是 \', \", \t, \n, \r, \, '\ ' 和 \uXXXX.
             if(i=='allmodules'):
                sql1=f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in ({self.systemname1}) AND updated > {self.start} AND updated <= {self.end} AND 根本解决？ = 根本解决'
             else:
                sql1=f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in ({self.systemname1}) AND labels={i} AND updated > {self.start} AND updated <= {self.end} AND 根本解决？ = 根本解决'
             #print(sql1)
             technicalsupport=self.jira.search_issues(sql1,maxResults=False)
             newnum2 = len(technicalsupport)
             d2[i]=newnum2
        return d2

#获取模块技术支持根本解决与否总数插表数据
def getdata_cplete(week,start,end):
    g =  ['crm系统','会员系统','Boss3订单系统', '分单系统','门票系统','在线客服系统','营销','确认管理','产品系统', '资源系统', '库存系统','采购系统', '投诉质检','NB系统', '出团通知', '其他', 'BOH']
    insert_data=[]
    for k in g:
       # data={}
        d2={}
        d3={}
        mudules=getmodule(k)
        getnum1=getnum(k,start,end,mudules)
        d2=getnum1.get_mudulenum_cplete_0()
        d3=getnum1.get_mudulenum_cplete_1()
        i=0
        for v in d2.items():
           h=v
           data={}
           data['systemname'] = k
           data["module_id"] =h[0]
           data['week'] = str(week)+'W'
           data['completely'] = 0
           data["num"] = h[1]
           insert_data.append(data)
        for v in d3.items():
           h=v
           data={}
           data['systemname'] = k
           data["module_id"] =h[0]
           data['week'] = str(week)+'W'
           data['completely'] = 1
           data["num"] = h[1]
           insert_data.append(data)
   # print(insert_data)
    return insert_data


class AddData():
    #插入数据前检查数据库中是否已经存在本周数据，如果存在就逻辑删除
    def check_data(self,insdata):
        for i in insdata:
            s = db.session.query(Support_completely_sum.id).filter(Support_completely_sum.systemname==list(i.values())[0]).filter(Support_completely_sum.module_id==list(i.values())[1]).filter(Support_completely_sum.week==list(i.values())[2]).filter(Support_completely_sum.completely==list(i.values())[3])
            for j in s:
                supportcplete=Support_completely_sum(id=j[0],del_flag=1)
                db.session.merge(supportcplete)

    #插入查询到的数据
    def insert_data_batch(self,insdata):
        db.session.execute(Support_completely_sum.__table__.insert(),insdata)


    def add_data(self,insdata):
        try:
            self.check_data(insdata)
            self.insert_data_batch(insdata)
            db.session.commit()
            print("提交成功")
        except Exception as e:
            db.session.rollback()

# if __name__ == '__main__':
#     a = nowtime()
#     now_time = a[0]
#     start = a[3]
#     end = a[4]
#     week = a[6]
#     h=getdata_cplete(week,start,end)
#     print(h)
#     add=AddData()
#     add.add_data(h)





