#./user/bin/python
#coding=UTF_8
from app.models.models import *
from flask import Blueprint
from sqlalchemy import func, and_, desc
import json
import sys
from flask import current_app
import xlrd
from flask import Blueprint,request
# 设置蓝图
getmodules = Blueprint('getmodules', __name__)
@getmodules.route('/getmodules')
def getmodule():
 try:
    dict = request.args
    if len(dict) >= 1:
      sysmudule =request.args["modulesystem"]
    mymodule1=[]
    mymodule=db.session.query(Support_module.module_id).filter(Support_module.systemname==sysmudule).all()
    #从数据库取出的每个记录都默认格式为数组('crm.会员标签',)，所以需要处理一下
    for i in mymodule:
        m=i[0]
        mymodule1.append(m)
    response = ({"success": "true", "msg": "OK", "data":  mymodule1})
    #print(response)
 except Exception as e:
        raise e
        response = {"success": "false", "msg": "查询失败~~"}
 response = json.dumps(response)
 return response

# if __name__ == '__main__':
#     getmodule()
