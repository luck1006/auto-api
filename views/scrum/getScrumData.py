# 统计迭代功能点数
author = "zhy"
date = "2019/5/28"
from app.models.models import *
from app import db,cache
from flask import Blueprint, request
from app.actions.scrum.getJira import GetJira
from concurrent.futures import ThreadPoolExecutor
from app.actions.tools.conf import cors_response
import logging
executor =ThreadPoolExecutor(1)

sync= Blueprint('sync', __name__)

@sync.route('/syncScrum',methods=['GET','POST'])

def sync1():
    data = request.get_json('data')
    # print(data)
    executor.submit(syncScrumInfo,data)
    response = {"success": "true", "msg": "同步进行中，请稍后查看~~"}
    # print("aa")
    # print(response)
    return cors_response(response)


def syncScrumInfo(data):
    try:


        # data = request.get_json('data')
        vers = data['vers']
        # print(vers)

        # 一共2个看板，线上团队一个看板，度假三个团队一个看板
        #删除版本号相同的信息
        Scrumteam.query.filter(Scrumteam.vers == vers).delete()
        db.session.commit()
        GetJ = GetJira()
        msg=GetJ.save_Excel(vers)

        # print("+++++++++++++++++++++++++=============")
        #保存信息
        # engine = create_engine('mysql+mysqlconnector://root:tuniu520@localhost/maxdata')
        # fp.to_sql(Scrumteam.__tablename__, con=engine, schema="maxdata", index=False, index_label=False, if_exists='append', chunksize=1000)
        response = ({"success": "true", "msg": msg})
    except Exception as e:
        raise e
        db.session.rollback()
        response = ({"success": "true", "msg": "同步失败～"})
    response = json.dumps(response)
    cache.delete('getScrumInfo')
    return response

