# -*- coding: utf-8 -*-
# TIME:         下午2:16
# Author:       xutaolin
from app import db
from app.actions.dataEncode import DateEncoder
import json
import datetime


class bbt_change(db.Model):
    '''
    CREATE TABLE `bbt_change` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `project` varchar(255) CHARACTER SET utf8mb4 NOT NULL DEFAULT '' COMMENT '代码库',
  `name` varchar(32) NOT NULL DEFAULT '' COMMENT '用户名',
  `branch` varchar(32) NOT NULL DEFAULT '' COMMENT '分支名称',
  `from_commit` varchar(32) NOT NULL DEFAULT ' ' COMMENT 'fromCommit',
  `to_commit` varchar(20) NOT NULL DEFAULT '' COMMENT 'toCommit',
  `message` varchar(255) NOT NULL DEFAULT '' COMMENT 'commit信息',
  `url` varchar(255) NOT NULL DEFAULT '' COMMENT 'diff代码地址',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='代码提交记录表';
    '''
    __tablename__ = 'bbt_change'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project = db.Column(db.String(64), nullable=False, default='')
    name = db.Column(db.String(32), nullable=False, default='')
    branch = db.Column(db.String(32), nullable=False, default='')
    from_commit = db.Column(db.String(16), nullable=False, default='')
    to_commit = db.Column(db.String(16), nullable=False, default='')
    message = db.Column(db.String(255), nullable=False, default='')
    url = db.Column(db.String(255), nullable=False, default='')
    create_time = db.Column(db.TIMESTAMP(True), nullable=False)

    def to_json(self):
        json_data = {
            'id': self.id,
            'project': self.project,
            'name': self.name,
            'branch': self.branch,
            'fromCommit': self.from_commit,
            'toCommit': self.to_commit,
            'message': self.message,
            'url': self.url,
            'createTime': self.create_time
        }
        return json.dumps(json_data, cls=DateEncoder)

    def __repr__(self):
        return '<bbt_change %r>' % self.name


class app_version(db.Model):
    __tablename__ = 'app_version'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,comment='主键id')
    version = db.Column(db.String(8), nullable=False, default='')
    start_time = db.Column(db.String(32), nullable=False, default='')
    end_time = db.Column(db.String(32), nullable=False, default='')
    tester = db.Column(db.String(8), nullable=False, default='')
    ios = db.Column(db.String(8), nullable=False, default='')
    android = db.Column(db.String(8), nullable=False, default='')
    remark = db.Column(db.String(255), nullable=False, default='',comment='备注')
    create_time = db.Column(db.TIMESTAMP(True), nullable=False)
    update_time = db.Column(db.TIMESTAMP(True), onupdate=datetime.datetime.now)


class Scrumteam(db.Model):
    __tablename__ = 'scrumteam'
    # id = db.Column(db.Integer)
    vers = db.Column(db.String(10), primary_key=True)
    reqnum = db.Column(db.Integer)
    planpoint = db.Column(db.Integer)
    actualpoint = db.Column(db.Integer)
    insertpoint = db.Column(db.Integer)
    removpoint = db.Column(db.Integer)
    finishrate = db.Column(db.Float)
    bugnum = db.Column(db.Integer)
    bugrate = db.Column(db.Float)
    team = db.Column(db.String(100), primary_key=True)


class Ammfirst(db.Model):
    __tablename__ = 'ammfirst'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10))


class Ammlevel(db.Model):
    __tablename__ = 'Ammlevel'
    levleid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10))


class Ammsecond(db.Model):
    __tablename__ = 'ammscecond'
    id = db.Column(db.Integer, primary_key=True)
    firstid = db.Column(db.Integer, db.ForeignKey('ammfirst.id'))
    level = db.Column(db.Integer)
    title = db.Column(db.String(255))
    point = db.Column(db.Integer)
    comment = db.Column(db.String(2048))


class Ammteam(db.Model):
    __tablename__ = 'ammteam'
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(20))
    secondid = db.Column(db.Integer, db.ForeignKey('ammscecond.id'))
    quarter = db.Column(db.String(20))


class Teamname(db.Model):
    __tablename__ = 'teamname'
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(20))
    flag = db.Column(db.Integer)
    name = db.Column(db.String(20))
    topic = db.Column(db.String(20))


# 接口覆盖率相关表
class Inter_data(db.Model):
    __tablename__ = 'inter_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    inter_name = db.Column(db.String(50))
    protocol = db.Column(db.String(100))
    path = db.Column(db.String(100))
    method = db.Column(db.String(50))
    dParam = db.Column(db.String(200))
    pData = db.Column(db.String(100))
    checklist = db.Column(db.String(100))
    response_data = db.Column(db.String(100))
    result = db.Column(db.String(100))
    creattime = db.Column(db.String(100))
    testdata = db.Column(db.String(100))
    comments = db.Column(db.String(100))
    inter_modure = db.Column(db.String(100))


class Modules_list(db.Model):
    __tablename__ = 'modules_list'
    module_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    module_name = db.Column(db.String(50))
    comments = db.Column(db.String(100))
    system = db.Column(db.String(10))
    systemChinese = db.Column(db.String(50))


class Modules_interface_list(db.Model):
    __tablename__ = 'modules_interface_list'
    module_name = db.Column(db.String(20))
    interface_path = db.Column(db.String(100), primary_key=True)
    is_auto = db.Column(db.String(5))
    comments = db.Column(db.String(100))
    createtime = db.Column(db.DATETIME, default=datetime.datetime.now)
    updatetime = db.Column(db.DATETIME, onupdate=datetime.datetime.now)


# 下单统计数据相关表
class Order_week_statistics(db.Model):
    __tablename__ = 'order_week_statistics'
    productType = db.Column(db.String(100))
    week = db.Column(db.String(20), primary_key=True)
    count = db.Column(db.Integer)
    isSuccess = db.Column(db.Integer)
    year = db.Column(db.String(4), default=str(datetime.datetime.now().year)+str(datetime.datetime.now().month))


# 下单终端数据库
class Order_success_terminal(db.Model):
    __tablename__ = 'order_success_terminal'
    terminal = db.Column(db.String(100), primary_key=True)
    orderCount = db.Column(db.Integer)
    productType = db.Column(db.String(100))


class Order_success_terminal_holiday(db.Model):
    __tablename__ = 'order_success_terminal_holiday'
    terminal = db.Column(db.String(100), primary_key=True)
    productTypeChild = db.Column(db.String(100))
    orderCount = db.Column(db.Integer)
    productType = db.Column(db.String(100))


class Order_failuer_statistics(db.Model):
    __tablename__ = 'order_failuer_statistics'
    productType = db.Column(db.String(100), primary_key=True)
    orderCount = db.Column(db.Integer)
    isSuccess = db.Column(db.Integer)
    failMsg = db.Column(db.String(100))


# 下单数据分析表
class Report_Analysis(db.Model):
    __tablename__ = 'report_analysis'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    content = db.Column(db.String(1000))
    time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    del_flag = db.Column(db.Integer, default=0)


# 资本化数据统计相关表
class Time_working(db.Model):
    __tablename__ = 'time_working'
    week = db.Column(db.String(50), primary_key=True)
    year = db.Column(db.String(6), default=str(datetime.datetime.now().year)+str(datetime.datetime.now().month))
    capitalizationTime = db.Column(db.Float)
    projectTime = db.Column(db.Float)
    supportTime = db.Column(db.Float)
    theoreticalTime = db.Column(db.Float)
    totalnum = db.Column(db.Integer)
    lingshouTime = db.Column(db.Float)
    zhuanhuaTime = db.Column(db.Float)
    xinkeTime = db.Column(db.Float)
    yunyingTime = db.Column(db.Float)
    jiagouTime = db.Column(db.Float)
    dabaoTime = db.Column(db.Float)
    juheTime = db.Column(db.Float)
    huiyuanTime = db.Column(db.Float)
    gongyinglianTime = db.Column(db.Float)
    dingdanTime = db.Column(db.Float)


# 工时数据detail表
class Time_working_detail(db.Model):
    __tablename__ = 'time_working_detail'
    index = db.Column(db.Integer, primary_key=True)
    姓名 = db.Column(db.String(50))
    组织架构 = db.Column(db.String(50))
    日期 = db.Column(db.String(50))
    工时 = db.Column(db.Float)
    单号 = db.Column(db.String(50))
    类型_x = db.Column(db.String(50))
    id = db.Column(db.Integer)
    LINKNAME = db.Column(db.String(50))
    SOURCE = db.Column(db.String(50))
    父级jira = db.Column(db.String(50))
    类型_y = db.Column(db.String(50))
    主题 = db.Column(db.String(50))
    描述 = db.Column(db.String(50))
    需求提出人 = db.Column(db.String(50))
    需求提出部门 = db.Column(db.String(50))
    立项项目名称 = db.Column(db.String(50))
    Epic = db.Column(db.String(50))


# 邮件接收者表
class Receiver(db.Model):
    __tablename__ = 'receiver'
    receiver_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    receiver_name = db.Column(db.String(100))
    comment = db.Column(db.String(1000))


# 接口用例相关
class Interface_Mall(db.Model):
    __tablename__ = 'interface_mall'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1024))
    request = db.Column(db.Text)
    rest = db.Column(db.Text)
    data = db.Column(db.Text)
    headers = db.Column(db.Text)
    expected_response = db.Column(db.Text)
    assert_info = db.Column(db.Text)
    global_var = db.Column(db.Text)
    update_time = db.Column(db.TIMESTAMP(True), nullable=False)
    tree_id = db.Column(db.Integer)
    tag = db.Column(db.Text)
    env = db.Column(db.Text)
    dParam = db.Column(db.Text)
    request_type = db.Column(db.String(10), default='rest')
    isBase64Encode = db.Column(db.Boolean, default=False)
    regex_checklist = db.Column(db.Text)  # 20190902 dff: 批量正则校验字段列表
    isBase64Decode = db.Column(db.Boolean, default=False) #dff-20191009 新增
    queryMethod = db.Column(db.Text) #20191225 dff增加用于存储pepple接口的查询方法

    def __repr__(self):
        return '<Interface_Mall %r>' % self.name


# class Interface_Task(db.Model):
#     __tablename__ = 'interface_task'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     task_name = db.Column(db.String(1024))
#     task_ids = db.Column(db.String(1024))
#     task_makecasename = db.Column(db.String(1024))
#     task_casename = db.Column(db.Text)
#     create_time = db.Column(db.TIMESTAMP(True), nullable=False)
#
#     def __repr__(self):
#         return '<interface_task %r>' % self.name


class Parms_Enviroment(db.Model):
    __tablename__ = 'parms_enviroment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # environment=db.Column(db.String(1024))
    parms_key = db.Column(db.String(1024))
    parms_value = db.Column(db.String(1024))
    create_time = db.Column(db.TIMESTAMP(True), nullable=False)
    create_user = db.Column(db.String(1024))
    parms_env = db.Column(db.String(10))
    parms_type = db.Column(db.String(10),nullable=False,default="user")

    # def __repr__(self):
    #     return '<parms_enviroment %r>' % self.name


class Tree_Task(db.Model):
    __tablename__ = 'tree_task'
    tree_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # environment=db.Column(db.String(1024))
    tree_name = db.Column(db.String(50), nullable=False)
    tree_order = db.Column(db.Integer, nullable=False)
    parent_id = db.Column(db.Integer, nullable=False, default=0)
    tree_type = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<tree_task %r>' % self.name


class TAG(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(50), nullable=False)
    del_flag = db.Column(db.String(50), nullable=False)


class Report(db.Model):
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(100))
    case_id = db.Column(db.Integer, nullable=False)
    runtime = db.Column(db.Integer)
    result = db.Column(db.String(1024))
    inparams = db.Column(db.Text)
    outparams = db.Column(db.Text)
    checkout = db.Column(db.Text)
    count = db.Column(db.Integer,index=True)
    create_time = db.Column(db.TIMESTAMP(True), nullable=False, index=True)
    rest = db.Column(db.String(1024))


# 技术支持表

class Technical_Support(db.Model):
    __tablename__ = 'support'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, default=int(datetime.datetime.now().year))
    week = db.Column(db.Integer)
    newnum = db.Column(db.Integer)
    closenum = db.Column(db.Integer)
    unsolvednum = db.Column(db.Integer)
    hisunsolvednum = db.Column(db.Integer)
    resolutionrate = db.Column(db.Float)
    time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    del_flag = db.Column(db.Integer, default=0)

class Technical_MonthSupport(db.Model):
    __tablename__ = 'monthsupport'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, default=int(datetime.datetime.now().year))
    month = db.Column(db.Integer)
    newnum = db.Column(db.Integer)
    closenum = db.Column(db.Integer)
    unsolvednum = db.Column(db.Integer)
    hisunsolvednum = db.Column(db.Integer)
    resolutionrate = db.Column(db.Float)
    time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    del_flag = db.Column(db.Integer, default=0)


class Technical_QuarterSupport(db.Model):
    __tablename__ = 'quartersupport'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, default=int(datetime.datetime.now().year))
    quarter = db.Column(db.Integer)
    newnum = db.Column(db.Integer)
    closenum = db.Column(db.Integer)
    unsolvednum = db.Column(db.Integer)
    hisunsolvednum = db.Column(db.Integer)
    resolutionrate = db.Column(db.Float)
    time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    del_flag = db.Column(db.Integer, default=0)


# 技术支持分析表
class Technical_Analysis(db.Model):
    __tablename__ = 'analysis'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    year = db.Column(db.Integer, default=int(datetime.datetime.now().year))
    week = db.Column(db.Integer)
    content = db.Column(db.String(1000), nullable=False)
    time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    del_flag = db.Column(db.Integer, default=0)


#技术支持分析--系统-问题类型数据统计表
#使用这个2019-11-19
class Support_types_sum(db.Model):
    __tablename__ = 'support_analysis_types'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    systemname = db.Column(db.String(30), nullable=False)
    detailsystem = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, default=int(datetime.datetime.now().year))
    week = db.Column(db.Integer)
    types=db.Column(db.Integer,default=0)
    num = db.Column(db.Integer,default=0)
    time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    del_flag = db.Column(db.Integer,default=0)

#技术支持-系统模块
#弃用2019-11-19
class Support_module(db.Model):
    __tablename__ = 'spmodule'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    systemname = db.Column(db.String(30), nullable=False)
    module_id = db.Column(db.String(100), nullable=False)

#技术支持分析--模块总数统计表
#弃用2019-11-19
class Support_sum(db.Model):
    __tablename__ = 'support_analysis'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    systemname = db.Column(db.String(30), nullable=False)
    module_id = db.Column(db.String(100), nullable=False)
    week = db.Column(db.String(40), nullable=False)
    num = db.Column(db.Integer,default=0)
    del_flag = db.Column(db.Integer,default=0)

#技术支持分析--模块-根本解决总数统计表
#弃用2019-11-19
class Support_completely_sum(db.Model):
    __tablename__ = 'support_analysis_completely'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    systemname = db.Column(db.String(30), nullable=False)
    module_id = db.Column(db.String(100), nullable=False)
    week = db.Column(db.String(40), nullable=False)
    completely=db.Column(db.Integer,default=0)
    num = db.Column(db.Integer,default=0)
    del_flag = db.Column(db.Integer,default=0)




class Case_Level(db.Model):
    __tablename__ = 'case_level'
    case_id= db.Column(db.Integer,primary_key=True,index=True)
    levels= db.Column(db.String(40))

class Jenkins_Case_Build(db.Model):
    __tablename__ = 'jenkins_case_build'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    group_name=db.Column(db.String(20),index=True)
    report_num=db.Column(db.Integer,primary_key=True)
    tag=db.Column(db.String(40))
    env=db.Column(db.String(20))
    build_result=db.Column(db.Integer,comment='0:失败，1为成功')
    success_case_count=db.Column(db.Integer)
    fail_case_count=db.Column(db.Integer)
    start_time=db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    end_time=db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    week=db.Column(db.Integer,index=True)


class FlightData(db.Model):
    __tablename__ = 'flightdata'
    date_time = db.Column(db.String(20), primary_key=True,nullable=False)
    defaultRecommed = db.Column(db.Integer)
    defaultFailed = db.Column(db.Integer)
    defaultPercent = db.Column(db.Float)
    systemProduct = db.Column(db.Integer)
    systemFailed = db.Column(db.Integer)
    systemPercent = db.Column(db.Float)
    checkPrice = db.Column(db.Integer)
    checkFailed = db.Column(db.Integer)
    checkPercent = db.Column(db.Float)
    shoppingCart = db.Column(db.Integer)
    shoppingFailed = db.Column(db.Integer)
    shoppingPercent = db.Column(db.Float)
    orderPage = db.Column(db.Integer)
    orderFailed = db.Column(db.Integer)
    orderPercent = db.Column(db.Float)


class HotelData(db.Model):
    __tablename__ = 'hoteldata'
    date_time = db.Column(db.String(20),primary_key=True, nullable=False)
    defaultRecommed = db.Column(db.Integer)
    defaultFailed = db.Column(db.Integer)
    defaultPercent = db.Column(db.Float)
    systemProduct = db.Column(db.Integer)
    systemFailed = db.Column(db.Integer)
    systemPercent = db.Column(db.Float)
    checkPrice = db.Column(db.Integer)
    checkFailed = db.Column(db.Integer)
    checkPercent = db.Column(db.Float)
    shoppingCart = db.Column(db.Integer)
    shoppingFailed = db.Column(db.Integer)
    shoppingPercent = db.Column(db.Float)
    orderPage = db.Column(db.Integer)
    orderFailed = db.Column(db.Integer)
    orderPercent = db.Column(db.Float)


class TicketData(db.Model):
    __tablename__ = 'ticketdata'
    date_time = db.Column(db.String(20),primary_key=True, nullable=False)
    defaultRecommed = db.Column(db.Integer)
    defaultFailed = db.Column(db.Integer)
    defaultPercent = db.Column(db.Float)
    checkPrice = db.Column(db.Integer)
    checkFailed = db.Column(db.Integer)
    checkPercent = db.Column(db.Float)
    shoppingCart = db.Column(db.Integer)
    shoppingFailed = db.Column(db.Integer)
    shoppingPercent = db.Column(db.Float)
    orderPage = db.Column(db.Integer)
    orderFailed = db.Column(db.Integer)
    orderPercent = db.Column(db.Float)

class PackageBookData(db.Model):
    __tablename__ = 'bookdata'
    date_time = db.Column(db.String(20),primary_key=True, nullable=False)
    packageNum = db.Column(db.Integer)
    packageFailed = db.Column(db.Integer)
    packagePercent = db.Column(db.Float)
    enterBookNum = db.Column(db.Integer)
    orderNum = db.Column(db.Integer)
    resign = db.Column(db.Integer)
    orderNumforHS = db.Column(db.Integer)
    resignforHS = db.Column(db.Integer)

class ForeignFlightData(db.Model):
    __tablename__ = 'foreignflightdata'
    date_time = db.Column(db.String(20), primary_key=True,nullable=False)
    defaultRecommed = db.Column(db.Integer)
    defaultFailed = db.Column(db.Integer)
    defaultPercent = db.Column(db.Float)
    checkPrice = db.Column(db.Integer)
    checkFailed = db.Column(db.Integer)
    checkPercent = db.Column(db.Float)
    shoppingCart = db.Column(db.Integer)
    shoppingFailed = db.Column(db.Integer)
    shoppingPercent = db.Column(db.Float)
    orderPage = db.Column(db.Integer)
    orderFailed = db.Column(db.Integer)
    orderPercent = db.Column(db.Float)


class ForeignHotelData(db.Model):
    __tablename__ = 'foreignhoteldata'
    date_time = db.Column(db.String(20),primary_key=True, nullable=False)
    defaultRecommed = db.Column(db.Integer)
    defaultFailed = db.Column(db.Integer)
    defaultPercent = db.Column(db.Float)
    checkPrice = db.Column(db.Integer)
    checkFailed = db.Column(db.Integer)
    checkPercent = db.Column(db.Float)
    shoppingCart = db.Column(db.Integer)
    shoppingFailed = db.Column(db.Integer)
    shoppingPercent = db.Column(db.Float)
    orderPage = db.Column(db.Integer)
    orderFailed = db.Column(db.Integer)
    orderPercent = db.Column(db.Float)


class ForeignTicketData(db.Model):
    __tablename__ = 'foreignticketdata'
    date_time = db.Column(db.String(20),primary_key=True, nullable=False)
    defaultRecommed = db.Column(db.Integer)
    defaultFailed = db.Column(db.Integer)
    defaultPercent = db.Column(db.Float)
    checkPrice = db.Column(db.Integer)
    checkFailed = db.Column(db.Integer)
    checkPercent = db.Column(db.Float)
    shoppingCart = db.Column(db.Integer)
    shoppingFailed = db.Column(db.Integer)
    shoppingPercent = db.Column(db.Float)
    orderPage = db.Column(db.Integer)
    orderFailed = db.Column(db.Integer)
    orderPercent = db.Column(db.Float)

class ForeignPackageBookData(db.Model):
    __tablename__ = 'foreignbookdata'
    date_time = db.Column(db.String(20),primary_key=True, nullable=False)
    packageNum = db.Column(db.Integer)
    packageFailed = db.Column(db.Integer)
    packagePercent = db.Column(db.Float)
    enterBookNum = db.Column(db.Integer)
    orderNum = db.Column(db.Integer)
    resign = db.Column(db.Integer)
    orderNumforHS = db.Column(db.Integer)
    resignforHS = db.Column(db.Integer)


class SysParams(db.Model):
    __tablename__ = 'sysparams'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sys_paramname = db.Column(db.String(50),nullable=False)
    sys_paramstatus = db.Column(db.Boolean, default=True)
    sys_paramremark = db.Column(db.String(254))

class Scrum_Req_Info(db.Model):
    __tablename__ = 'scrum_req_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(20),nullable = False)
    permalink = db.Column(db.String(50),nullable = False)
    summary = db.Column(db.String(200),nullable = False)
    owner_team = db.Column(db.String(10))
    owner_project = db.Column(db.String(20))
    owner_version = db.Column(db.String(20))
    type = db.Column(db.Integer,default = 0)
    reporter = db.Column(db.String(20))
    assigner = db.Column(db.String(20))
    points = db.Column(db.Integer)
    subreqnum = db.Column(db.Integer)
    status = db.Column(db.String(10))
    isdelay = db.Column(db.Integer,default = 0)
    isinsert = db.Column(db.Integer,default = 0)
    process = db.Column(db.String(500))
    insert_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    delay_version = db.Column(db.String(20))

class Scrum_Req_TeamInfo(db.Model):
    __tablename__ = 'scrum_req_teaminfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    req_team = db.Column(db.String(10))
    req_project = db.Column(db.String(20))
    req_version = db.Column(db.String(20))
    del_flag = db.Column(db.Integer,default=0)

class Worker_ScrumTeam(db.Model):
    __tablename__ = 'worker_scrumteam'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    worker_name = db.Column(db.String(14))
    scrum_team = db.Column(db.String(10))
    status = db.Column(db.Boolean, default = True)