#  -*-  coding: utf-8  -*-
from flask import Blueprint, jsonify, request
from app.actions.view_log import viewlog
from flask import make_response, send_from_directory
from app.actions.TNJ.tn_jira import Tn_JIRA
from urllib.parse import unquote
import json
from app.actions.TNJ.result import result, detail,byepic_month
from app import cache

tnj = Blueprint('tnj', __name__, url_prefix='/tnj')


# 查询几个面板下激活的sprint
@tnj.route('/sprint', methods=['GET'])
def get_sprint():
    try:
        d = Tn_JIRA.get_sprint()
        return jsonify({"success": True, "msg": "OK", "errorCode": 720000, "data": d})
    except:
        return jsonify({"success": False, "msg": "查询失败", "errorCode": 7200001, "data": None})


@tnj.route('/worktime', methods=['GET'])
@cache.cached(query_string=True, timeout=30 * 60)
def get_work_time_by_sprint():
    try:
        type = request.args.get('type')
        sprint = request.args.get('sprint')
        print('type；', type, "sprint:", sprint)
        # query_string = request.query_string.decode('utf-8')
        # query_string = unquote(query_string)
        # para_dict = json.loads(query_string)
        # type = para_dict.get('type')
        # sprint = para_dict.get('sprint')
        if int(type) == 1:
            res = Tn_JIRA.get_work_time_by_sprint(sprint)
            df = res.groupby(['Sprint', 'Epic', '概要', 'Story状态'])[
                '预估工作量', '已完成工作量', '剩余工作量', '超预估工作量'].sum().reset_index()
            return df.to_json(orient='table')
        # 明细
        if int(type) == 2:
            res = Tn_JIRA.get_work_time_by_sprint(sprint)
            return res.to_json(orient='table')
    except Exception as e:
        print(e)
        return jsonify({"success": "true", "errorCode": 710000, "msg": "查询异常", "data": []})


@tnj.route('/queryByEpic', methods=['GET'])
def query_timespend_by_epic():
    return jsonify({"errorCode": 710000, "success": True, "msg": "ok", "data": result()})


@tnj.route('/timespend_detail', methods=['GET'])
def timespend_detail():
    return jsonify({"success":True,"errorCode":710000,"message":"ok","data":detail()})

@tnj.route('/queryEpicbyMonth', methods=['GET'])
def timespend_epicby_month():
    return jsonify({"errorCode": 710000, "success": True, "msg": "ok", "data": byepic_month()})
