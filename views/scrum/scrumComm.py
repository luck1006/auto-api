# -*- coding: utf-8 -*-
# TIME:         5.21
# Author:       zhuhaiyan
# Explain：     获取团队信息

from app.models.models import *
from flask import Blueprint
from sqlalchemy import func, and_, desc
import json
import sys
from flask import current_app

# 设置蓝图
scrumComm = Blueprint('comm', __name__)




@scrumComm.route('/teamName')
def getScrumTeam():
    # 查询所有成熟度模型
    infos = []
    try:
        listInfo = db.session.query(Teamname.team, Teamname.name).filter(Teamname.flag == 1).all()
        for i in range(len(listInfo)):
            infos.append({"teamCode": listInfo[i][0], "teamName": listInfo[i][1]})
        response = ({"success": "true", "msg": "OK", "data": infos})
    except Exception as e:
        raise e
        response = {"success": "false", "msg": "查询失败~~！！"}
    response = json.dumps(response)
    return response
