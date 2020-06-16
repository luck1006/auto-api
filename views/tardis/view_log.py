# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from app.actions.view_log import viewlog, view_db
from flask import make_response, send_from_directory

from app.actions.TNJ.jira_conf import JIRA_CONFIG
import json

viewLog = Blueprint('viewlog', __name__)


@viewLog.route('/viewLog', methods=['GET'])
def view_logs():
    res = viewlog()
    return jsonify(res)


@viewLog.route('/viewLog/download', methods=['GET'])
def log_download():
    # file_path = '/Users/sunchuanxin/PycharmProjects/autoapi'
    # file_name = 'dka.log'
    file_name = 'gunicorn_error.log'
    file_path = '/opt/tuniu/www/Pandora/log'
    response = make_response(
        send_from_directory(file_path, file_name, as_attachment=True))
    response.headers["Content-Disposition"] = f"attachment;filename={file_name}"
    response.headers['Cache-Control'] = 'max-age=0'
    return response


@viewLog.route('/query/jira/conf', methods=['GET'])
def db_config():
    res = view_db()
    return jsonify(res)


@viewLog.route('/test', methods=['GET'])
def test():
    data = JIRA_CONFIG().fetch_all('select * from t_oa_user limit 10')
    return jsonify(data)


@viewLog.route('/execute', methods=['POST'])
def sql():
    sql = request.get_json().get('sql')
    data = JIRA_CONFIG().fetch_all(sql)
    return jsonify(data)
