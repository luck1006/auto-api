#./user/bin/python
#coding=UTF_8
import datetime
from jira import JIRA
import json
from app.models.models import *
from flask import Blueprint

#设置蓝图
addalystypes = Blueprint('addalystypes', __name__)
@addalystypes.route('/addalystypes')
def addalystypes2():
    a = nowtime()
    now_time = a[0]
    start = a[3]
    end = a[4]
    week = a[6]
    h1=getdata_types(week,start,end)
    h2=getdata_alltypes(week,start,end)
    add=AddData()
    add.add_data(h1)
    add.add_data(h2)
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

#查询jira
class getNum():
    def __init__(self,systemname,types,start,end):
        #初化jira链接
        self.jira =JIRA('http://jira.tuniu.org',basic_auth=('zhangwen3','005381@nzc8'))
        self.start=start
        self.end=end
        self.systemname=systemname
        self.types = types

    def get_type_num(self):

        if(self.types==0):
            num = 0
            # 获取【系统默认值】技术支持数
            self.sql = f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in ({self.systemname}) AND created > {self.start} AND created <= {self.end} AND cf[17808] IN cascadeOption(19803)'
            technicalsupport = self.jira.search_issues(self.sql, maxResults=False)
            num = len(technicalsupport)
            print('000000',num)
            return num
        elif(self.types==1):
            num = 0
            # 获取【IT类】技术支持数
            self.sql = f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in ({self.systemname}) AND created > {self.start} AND created <= {self.end} AND cf[17808] IN cascadeOption(19683)'
            technicalsupport = self.jira.search_issues(self.sql, maxResults=False)
            num = len(technicalsupport)
            print('111111', num)
            return num
        elif(self.types==2):
            num = 0
            # 获取【无效问题】技术支持数
            self.sql = f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in ({self.systemname}) AND created > {self.start} AND created <= {self.end} AND cf[17808] IN cascadeOption(19682)'
            technicalsupport = self.jira.search_issues(self.sql, maxResults=False)
            num = len(technicalsupport)
            print('222222', num)
            return num
        elif(self.types==3):
            num = 0
            # 获取【环境问题】技术支持数
            self.sql = f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in ({self.systemname}) AND created > {self.start} AND created <= {self.end} AND cf[17808] IN cascadeOption(19681)'
            technicalsupport = self.jira.search_issues(self.sql, maxResults=False)
            num = len(technicalsupport)
            print('333333', num)
            return num
        elif(self.types==4):
            num = 0
            # 获取【用户类问题】技术支持数
            self.sql = f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in ({self.systemname}) AND created > {self.start} AND created <= {self.end} AND cf[17808] IN cascadeOption(19680)'
            technicalsupport = self.jira.search_issues(self.sql, maxResults=False)
            num = len(technicalsupport)
            print('44444', num)
            return num
        elif(self.types==5):
            num = 0
            # 获取【系统不支持】技术支持数
            self.sql = f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in ({self.systemname}) AND created > {self.start} AND created <= {self.end} AND cf[17808] IN cascadeOption(19679)'
            technicalsupport = self.jira.search_issues(self.sql, maxResults=False)
            num = len(technicalsupport)
            print('555555', num)
            return num
        else:
            num = 0
            # 获取【系统故障】技术支持数
            self.sql = f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in ({self.systemname})  AND created > {self.start} AND created <= {self.end} AND cf[17808] IN cascadeOption(19678)'
            technicalsupport = self.jira.search_issues(self.sql, maxResults=False)
            num = len(technicalsupport)
            print('66666', num)
            return num

    def get_type7_num(self):
        num = 0
        # 获取系统【全部】技术支持数
        self.sql = f'(issuetype = 技术支持 OR issuetype = 新技术支持) AND 归属系统 in ({self.systemname}) AND created > {self.start} AND created <= {self.end}'
        technicalsupport = self.jira.search_issues(self.sql, maxResults=False)
        num = len(technicalsupport)
        print('7777777',num)
        return num


#获取系统技术支持问题类型数据
def getdata_alltypes(week,start,end):
    t = [0,1,2,3,4,5,6,7]
    g1 = [('门票系统'),('crm系统','会员系统'),('Boss3订单系统', '分单系统'),('营销'),('确认管理'),('产品系统', '资源系统', '库存系统','采购系统', '投诉质检','NB系统', '出团通知', 'BOH')]
    #g11 = [('确认管理')]
    insert_data=[]
    for i in t:
        for k in g1:
            data = {}
            getnum = getNum(k, i, start, end)
            if(k[0]=='crm系统'):
                data["systemname"] = "会员"
                data['detailsystem'] = "全部"
                data['week'] = week
                data["types"] = i
                if(i!=7):
                    data["num"] = getnum.get_type_num()
                else:
                    data["num"] = getnum.get_type7_num()
                insert_data.append(data)
            elif(k[0]=='Boss3订单系统'):
                data["systemname"] = "订单"
                data['detailsystem'] = "全部"
                data['week'] = week
                data["types"] = i
                if (i != 7):
                    data["num"] = getnum.get_type_num()
                else:
                    data["num"] = getnum.get_type7_num()
                insert_data.append(data)
            elif(k=='门票系统'):
                data["systemname"] = "门票"
                data['detailsystem'] = "全部"
                data['week'] = week
                data["types"] = i
                if (i != 7):
                    data["num"] = getnum.get_type_num()
                else:
                    data["num"] = getnum.get_type7_num()
                insert_data.append(data)
            elif(k=='营销'):
                data["systemname"] = "营销"
                data['detailsystem'] = "全部"
                data['week'] = week
                data["types"] = i
                if (i != 7):
                    data["num"] = getnum.get_type_num()
                else:
                    data["num"] = getnum.get_type7_num()
                insert_data.append(data)
            elif(k=='确认管理'):
                data["systemname"] = "确认管理"
                data['detailsystem'] = "全部"
                data['week'] = week
                data["types"] = i
                if (i != 7):
                    data["num"] = getnum.get_type_num()
                else:
                    data["num"] = getnum.get_type7_num()
                insert_data.append(data)
            else:
                data["systemname"] = "供应链"
                data['detailsystem'] = "全部"
                data['week'] = week
                data["types"] = i
                if (i != 7):
                    data["num"] = getnum.get_type_num()
                else:
                    data["num"] = getnum.get_type7_num()
                insert_data.append(data)
    return insert_data

def getdata_types(week, start, end):
    g = ['crm系统','会员系统','Boss3订单系统','分单系统','门票系统','营销','确认管理','产品系统','资源系统','库存系统','采购系统','投诉质检','NB系统','出团通知','BOH']
    #g = ['确认管理']
    t = [0, 1, 2, 3, 4, 5, 6, 7]
    insert_data = []
    for i in t:
        for k in g:
            data = {}
            getnum = getNum(k, i, start, end)
            if(k=='crm系统' or k=='会员系统'):
                data["systemname"] = "会员"
                data['detailsystem'] = k
                data['week'] = week
                data["types"] = i
                if(i!=7):
                    data["num"] = getnum.get_type_num()
                else:
                    data["num"] = getnum.get_type7_num()
                insert_data.append(data)
            elif(k=='Boss3订单系统' or k=='分单系统'):
                data["systemname"] = "订单"
                data['detailsystem'] = k
                data['week'] = week
                data["types"] = i
                if (i != 7):
                    data["num"] = getnum.get_type_num()
                else:
                    data["num"] = getnum.get_type7_num()
                insert_data.append(data)
            elif(k=='门票系统'):
                data["systemname"] = "门票"
                data['detailsystem'] = k
                data['week'] = week
                data["types"] = i
                if (i != 7):
                    data["num"] = getnum.get_type_num()
                else:
                    data["num"] = getnum.get_type7_num()
                insert_data.append(data)
            elif(k=='营销'):
                data["systemname"] = "营销"
                data['detailsystem'] = k
                data['week'] = week
                data["types"] = i
                if (i != 7):
                    data["num"] = getnum.get_type_num()
                else:
                    data["num"] = getnum.get_type7_num()
                insert_data.append(data)
            elif(k=='确认管理'):
                data["systemname"] = "确认管理"
                data['detailsystem'] = k
                data['week'] = week
                data["types"] = i
                if (i != 7):
                    data["num"] = getnum.get_type_num()
                else:
                    data["num"] = getnum.get_type7_num()
                insert_data.append(data)
            else:
                data["systemname"] = "供应链"
                data['detailsystem'] = k
                data['week'] = week
                data["types"] = i
                if (i != 7):
                    data["num"] = getnum.get_type_num()
                else:
                    data["num"] = getnum.get_type7_num()
                insert_data.append(data)
    return insert_data




class AddData():
    #插入数据前检查数据库中是否已经存在本周数据，如果存在就逻辑删除
    def check_data(self,insdata):
        for i in insdata:
            #print(i.values())
            s = db.session.query(Support_types_sum.id).filter(Support_types_sum.year==int(datetime.datetime.now().year)).filter(Support_types_sum.systemname==list(i.values())[0]).filter(Support_types_sum.detailsystem==list(i.values())[1]).filter(Support_types_sum.week==list(i.values())[2]).filter(Support_types_sum.types==list(i.values())[3]).all()
            for j in s:
                supporttypes=Support_types_sum(id=j[0],del_flag=1)
                db.session.merge(supporttypes)

    #插入查询到的数据
    def insert_data_batch(self,insdata):
        db.session.execute(Support_types_sum.__table__.insert(),insdata)

    def add_data(self,insdata):
        try:
            self.check_data(insdata)
            self.insert_data_batch(insdata)
            db.session.commit()
            print("提交成功")
        except Exception as e:
            db.session.rollback()

# if __name__ == '__main__':
    # a = nowtime()
    # now_time = a[0]
    # start = a[3]
    # end = a[4]
    # week = a[6]
    # h=getdata_types(week,start,end)
    # print(h)
    # add=AddData()
    # add.add_data(h)





