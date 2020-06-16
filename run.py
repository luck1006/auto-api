from app import app
from views.Package.GetPackageData import GetPackageData
from views.demo1 import *
from views.quicklyOrder.FHPackagequicklyOrder.FHPackagequicklyOrder import FHPackageOrder
from views.quicklyOrder.getcancelOrder import CancelOrder
from views.scrum.scrum import *
from views.scrum.amm import *
from views.scrum.scrumComm import *
from views.scrum.getScrumData import *
from views.scrum.sprint import *
from views.interfaceAuto.interface import interface
from flask_restful import Api
from werkzeug.serving import run_simple
from views.interfaceAuto.interfaceCoverage import *
from views.bbt.bbtChange import bbt
from views.tools.qrcode import tool
from views.orderLogin.orderLogin import *
from views.timeStatistic.timeStatistic import *
from views.timeStatistic.timeworking import *
from views.timeStatistic.getweek import *
from views.orderLogin.orderLoginReport import *
from views.orderLogin.saveReportAnalysis import *
from views.orderLogin.getReceiver import *
from views.tardis.view_log import viewLog
from views.wangyi.wy import *
from views.wangyi.worktime import *
from views.technicalSupport.getTechnicalSuppot import *
from views.technicalSupport.addTechnicalSupport import *
from views.technicalSupport.saveTechnicalAnalysis import *
from views.shotEmail import *
from views.orderLogin.orderWeeks import *
from views.login.login import login

from views.Technicalsupportanalysis.getmodule import *
from views.Technicalsupportanalysis.getanalysiscplete import *
from views.Technicalsupportanalysis.getanalysistypes import *
from views.Technicalsupportanalysis.getanalysisdata import getanalysisdatas
from views.Technicalsupportanalysis.addanalysiscplete import *
from views.Technicalsupportanalysis.addanalysisdata import *
from views.Technicalsupportanalysis.addanalysistypes import *
from views.Technicalsupportanalysis.getnewall import *
from tnechart import echart

app.register_blueprint(echart)

from views.requirement.transXmind import *
import logging
from views.InternalInterface.FindInternalInterface import FindInternalInterface
from views.PenetrationTest.filedownload import penetration
from views.reqinfo.reqinfo import reqinfo

from views.interfaceAuto.appUrlCheck import appurlcheck

from views.productOrder.Workflow.Zizhu_Order_ziyuanzuhe import *
from views.productOrder.Workflow.Zizhu_Order_train import *
from views.productOrder.Workflow.Zizhu_Order_flight import *
from views.productOrder.Workflow.Zizhu_Order_dabao import *
from views.productOrder.Workflow.Zijia_Order import *
from views.productOrder.Workflow.Menpiao_Order import *
from views.productOrder.Workflow.GenTuan_Order_train import *
from views.productOrder.Workflow.GenTuan_Order_flight import *
from views.productOrder.Workflow.GenTuan_Order_dabao import *

from views.TNJ.tnj import tnj

app.register_blueprint(tnj)

# from app.loggerutil import Logger
# 注册蓝图
# 团队point+缺陷率
app.register_blueprint(scrum)
app.register_blueprint(sprint)
# 敏捷成熟度模型
app.register_blueprint(amm)
# 敏捷团队信息
app.register_blueprint(scrumComm)

# 用例接口相关接口
app.register_blueprint(interface)

# 接口自动化用例覆盖率
app.register_blueprint(interfaceCoverage)

# 每周下单&登录统计数据
app.register_blueprint(orderLogin)
# 每周下单&登录统计报表
app.register_blueprint(orderLoginReport)

# 邮件接受者
app.register_blueprint(getReceiver)

# 10周下单成功趋势统计数据
app.register_blueprint(orderWeeks)
# 一键下单
app.register_blueprint(zizhu_ziyuanzuhe)
app.register_blueprint(zizhu_train)
app.register_blueprint(zizhu_flight)
app.register_blueprint(zizhu_dabao)
app.register_blueprint(zijia)
app.register_blueprint(menpiao)
app.register_blueprint(gentuan_train)
app.register_blueprint(gentuan_flight)
app.register_blueprint(gentuan_dabao)
# 资本化工时统计数据
app.register_blueprint(timeStatistic)
# 资本化工时周统计数据
app.register_blueprint(timeworking)
# 资本化数据的周数
app.register_blueprint(getweek)

# 登录
app.register_blueprint(login)

app.register_blueprint(tool)
app.register_blueprint(bbt)
app.register_blueprint(wangyi)
app.register_blueprint(wt)
app.register_blueprint(technicalSupport)
app.register_blueprint(addTechnical)
app.register_blueprint(resolutionRate)
app.register_blueprint(exporttechnicalSupport)
app.register_blueprint(analysis)
app.register_blueprint(reportanalysis)

app.register_blueprint(sync)
app.register_blueprint(viewLog)
app.register_blueprint(shotEmail)
app.register_blueprint(getXmind)

api = Api(app)
api.add_resource(TodoList, '/todos')

# 技术支持分析
app.register_blueprint(getmodules)
app.register_blueprint(getanalysisdatas)
app.register_blueprint(getanalysiscpletes)
app.register_blueprint(modulegetty)
app.register_blueprint(gettyall)
app.register_blueprint(gettynew)
app.register_blueprint(getnewallnum)
app.register_blueprint(addalysdatas)
app.register_blueprint(addalystypes)
app.register_blueprint(adycpletes)
# 备注：蓝图与flaflask_restful 扩展二选一
app.register_blueprint(FindInternalInterface)
app.register_blueprint(penetration)
app.register_blueprint(CancelOrder)
app.register_blueprint(FHPackageOrder)
app.register_blueprint(GetPackageData)

# 注册app接口url可访问性蓝图
app.register_blueprint(appurlcheck)
# 迭代过程管理
app.register_blueprint(reqinfo)
# if __name__ != '__main__':
#     # 服务器上的日志路径
#     filename = '/opt/tuniu/www/AutoPlatForm/log/gunicorn_acess.log'
#     logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
#                         datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    app_options = {'use_reloader': True, 'use_debugger': True}
    # run_simple('172.31.85.11', 5001, app, **app_options)
    run_simple('127.0.0.1', 5001, app, threaded=True, **app_options)
