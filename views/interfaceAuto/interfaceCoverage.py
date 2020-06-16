# -*- coding: utf-8 -*-
# TIME:         6.10
# Author:       huangfang
# Explain：     获取接口覆盖率信息

from app.models.models import *
from flask import Blueprint
from sqlalchemy import func, and_, desc
import json
import sys
from flask import current_app

# 设置蓝图
interfaceCoverage = Blueprint('interfaceCoverage', __name__)




@interfaceCoverage.route('/interfaceCoverage')
def getinterfaceCoverage():
    # 查询模块自动化接口覆盖率
    infos = []
    # 查询总的接口数
    interfaceCount = db.session.query(Modules_interface_list).count()
    # 查询已经实现自动化的接口数
    isautoCount = db.session.query(Modules_interface_list).filter(Modules_interface_list.is_auto==1).count()
    # 计算总的接口自动化覆盖率
    percentage ="%.2f%%" % ((isautoCount/interfaceCount) * 100)


    try:
        # 获取每个模块的用例总数，已经实现自动化用例数，自动化覆盖率信息
        interfaceInfos = []
        moduleName = db.session.query(Modules_list.systemChinese).filter(Modules_list.systemChinese.in_(["供应链","零售","详情预定","聚合","会员","订单","任务中心"])).distinct().all()
        #print(moduleName)

        for i in range(len(moduleName)):

           moduleInterfaceCount=db.session.query(Modules_interface_list.module_name).filter(
               Modules_list.module_name == Modules_interface_list.module_name).filter(Modules_list.systemChinese == moduleName[i][0]).count()
           moduleAutoCount = db.session.query(Modules_interface_list.module_name).filter(
               Modules_list.module_name == Modules_interface_list.module_name).filter(
        Modules_interface_list.is_auto==1).filter(
               Modules_list.systemChinese == moduleName[i][0]).count()
           #print ("moduleinterfaceCount123====",moduleInterfaceCount)
           data = {
                    "moduleName": moduleName[i][0],
                    "interfaceCount":moduleInterfaceCount,
                    "isauto":moduleAutoCount,
                    "percentage":"%.2f%%" % ((moduleAutoCount/moduleInterfaceCount)*100),
                   }
           interfaceInfos.append(data)
        response = ({"success": "true", "msg": "OK", "data":{"interfaceCount": interfaceCount, "isautoCount": isautoCount, "percentage": percentage, "interfaceInfos":interfaceInfos}})
    except Exception as e:
        raise e
        response = {"success": "false", "msg": "查询失败~~"}
    response = json.dumps(response)
    return response

if __name__ == '__main__':
    #pass
    moduleName = db.session.query(Modules_list.system).distinct().all()
    print (moduleName[0][0])
    moduleinterfaceCount = db.session.query(Modules_interface_list.module_name).filter(
        Modules_list.module_name == Modules_interface_list.module_name).filter(
        Modules_interface_list.is_auto == 1).filter(Modules_list.system == moduleName[0][0]).count()
    isautoCount = db.session.query(Modules_interface_list).filter(Modules_interface_list.is_auto==1).count()

    print("moduleinterfaceCount====", moduleinterfaceCount)
    #print("isautoCount====", isautoCount)

