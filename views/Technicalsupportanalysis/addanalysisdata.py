#./user/bin/python
#coding=UTF_8
import datetime
from jira import JIRA
import json
from app.models.models import *
from flask import Blueprint

#设置蓝图
addalysdatas = Blueprint('addalysdatas1', __name__)
@addalysdatas.route('/addalysdata2',methods=['GET'])
def addalysdata2():
    a = nowtime()
    now_time = a[0]
    start = a[3]
    end = a[4]
    week = a[6]
    h=getdata(week,start,end)
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

#获取模块的技术支持总数
    def get_mudulenum(self):
        d1=dict()
        newnum=0
        for i in self.mudules:
            if(i=='allmodules'):
            #JQL语句中有错误： '\+' 是无效的JQL转义字符。 正确的转义字符写法是 \', \", \t, \n, \r, \, '\ ' 和 \uXXXX.
                sql1=f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in ({self.systemname1}) AND updated > {self.start} AND updated <= {self.end}'
            else:
                sql1=f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in ({self.systemname1}) AND labels={i} AND updated > {self.start} AND updated <= {self.end}'
            technicalsupport=self.jira.search_issues(sql1,maxResults=False)
            newnum = len(technicalsupport)
            d1[i]=newnum
        return d1

#获取模块技术支持总数插表数据
def getdata(week,start,end):
    g = ['crm系统','会员系统','Boss3订单系统', '分单系统','门票系统','在线客服系统','营销','确认管理','产品系统', '资源系统', '库存系统','采购系统', '投诉质检','NB系统', '出团通知', '其他', 'BOH']
    insert_data=[]
    for k in g:
       # data={}
        d2=dict()
        mudules=getmodule(k)
        getnum1=getnum(k,start,end,mudules)
        d2=getnum1.get_mudulenum()
        i=0
        for v in d2.items():
           h=v
           data={}
           data['systemname'] = k
           data["module_id"] =h[0]
           data['week'] = str(week)+'W'
           data["num"] = h[1]
           insert_data.append(data)
    return insert_data

class AddData():
    #插入数据前检查数据库中是否已经存在本周数据，如果存在就逻辑删除
    def check_data(self,insdata):
        for i in insdata:
            #print(i.values())
            s = db.session.query(Support_sum.id).filter(Support_sum.systemname==list(i.values())[0]).filter(Support_sum.module_id==list(i.values())[1]).filter(Support_sum.week==list(i.values())[2])
            for j in s:
                supportsis=Support_sum(id=j[0],del_flag=1)
                db.session.merge(supportsis)

    #插入查询到的数据
    def insert_data_batch(self,insdata):
        db.session.execute(Support_sum.__table__.insert(),insdata)


    def add_data(self,insdata):
        try:
            self.check_data(insdata)
            print("提交成功")
            self.insert_data_batch(insdata)
            db.session.commit()
            #print("提交成功")
        except Exception as e:
            db.session.rollback()

# if __name__ == '__main__':
#     a = nowtime()
#     now_time = a[0]
#     start = a[3]
#     end = a[4]
#     week = a[6]
#     h=getdata(week,start,end)
#     add=AddData()
#     add.add_data(h)





