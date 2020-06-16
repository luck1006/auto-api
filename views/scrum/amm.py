# -*- coding: utf-8 -*-
# TIME:         下午2:56
# Author:       zhuhaiyan
# Explain：     获取敏捷成熟度模型

from app.models.models import *
from flask import Blueprint,current_app,request,flash
from sqlalchemy import func, and_, desc
import json
import sys

# 设置蓝图
amm = Blueprint('ammInfo', __name__)
# def cors_response(res):
#     response = json.dumps(res,ensure_ascii=False)
#     # response = make_response(jsonify(res))
#     response = make_response(response)
#     # response = make_response(res)
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Methods'] = 'PUT,POST,GET,DELETE,OPTIONS'
#     # response.headers['Access-Control-Request-Method']='PUT,POST,GET,DELETE,OPTIONS'
#     response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, t'
#     response.headers['Access-Control-Allow-Credentials'] = true
#     return response

@amm.route('/ammInfo')
def getAmmInfo():
    # 查询所有成熟度模型
    try:
        listInfo = db.session.query(Ammfirst.id, Ammfirst.title).all()
        ammInfos = []  # 6个维度
        levels = []  # level
        infos = []  # 具体标准
        for i in range(len(listInfo)):
            for j in range(5, 0, -1):
                secendInfo = db.session.query(Ammsecond.id, Ammsecond.title, Ammsecond.point, Ammlevel.levleid,
                                              Ammlevel.title,Ammsecond.comment).filter(
                    and_(Ammsecond.firstid == listInfo[i][0], Ammsecond.level == j,
                         Ammsecond.level == Ammlevel.levleid)).all()
                for z in range(len(secendInfo)):
                    # current_app.logger.info(secendInfo[z])
                    infos.append({"id": secendInfo[z][0], "title": secendInfo[z][1], "point": secendInfo[z][2],"comment":secendInfo[z][5]})
                levels.append({"levelid": secendInfo[z][3], "level": secendInfo[z][4], "data": infos})
                infos = []
            ammInfos.append({"layer": listInfo[i][0], "title": listInfo[i][1], "ammInfo": levels})
            levels = []
        response = ({"success": "true", "msg": "OK", "data": ammInfos})
    except Exception as e:
        raise e
    response = json.dumps(response)
    return response


@amm.route('/commitAmm',methods=['GET','POST'])
def commitAmm():
    try:
        data=request.get_json('data')

        team=data['team']
        quarter=data['quarter']
        secondId=data['secondId']

        Ammteam.query.filter(and_(Ammteam.team == team, Ammteam.quarter == quarter)).delete()
        # db.session.commit()
        for id in secondId:
            count = db.session.query(Ammteam.secondid).filter(and_(Ammteam.secondid==id,Ammteam.team==team,Ammteam.quarter == quarter)).count()
            if count==0 :
                print("新增")
                add = Ammteam(
                            team=team,
                            secondid=id,
                            quarter=quarter
                                     )
                db.session.add(add)
                # print("+++++")
            else:
                # print("更新")
                Ammteam.query.filter(and_(Ammteam.secondid==id,Ammteam.team==team)).update({'team': team, 'quarter': quarter})
        db.session.commit()
        response = ({"success": "true", "msg": "ok"})
    except Exception as e:
        raise e
        response=({"success": "false", "msg": "操作失败～～"})
        db.session.rollback()
    response = json.dumps(response)
    return response
    # return cors_response(response)

#通过scrumteam获取团队的成熟度信息
@amm.route('/queryByteam',methods=['GET','POST'])
def queryByteam():
    # print("*******")
    list=[]
    try:
        dict=request.args
        if len(dict)==2:
            team = request.args["team"]
            quarter= request.args["quarter"]
            secendInfo = db.session.query(Ammteam.secondid).filter(
                and_(Ammteam.team == team, Ammteam.quarter == quarter)).all()
            for id in secendInfo:
                list.append(id[0])
                # print(list)
        response = ({"success": "true", "msg": "OK", "data": list})
    except Exception as e:
        raise e
        response = ({"success": "false", "msg": "操作失败～～"})
    response = json.dumps(response)
    return response