# encode=utf-8
from app.models.models import *
from flask import jsonify, Blueprint, request
import json
from app.actions.tools.timer import time2any
from urllib.parse import unquote

sprint = Blueprint('time', __name__, url_prefix='/sprint')


@sprint.route('/time')
def time():
    # print(request.headers.get('content-type'))
    query_string = request.query_string.decode('utf-8')
    query_string = unquote(query_string)
    para_dict = json.loads(query_string)
    return jsonify(time2any(para_dict['time']))


@sprint.route('/version')
def version():
    data = db.session.query(app_version).order_by(app_version.version.desc()).limit(10).offset(0)
    list = []
    for t in data:
        dic = {
            "id": t.id,
            "version": t.version,
            "startTime": t.start_time,
            "endTime": t.end_time,
            "tester": t.tester,
            "ios": t.ios,
            "android": t.android,
            "remark": t.remark
        }
        list.append(dic)
    res = {
        "success": True,
        "msg": "ok",
        "code": 720000,
        "data": list
    }

    return jsonify(res)


@sprint.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    id = data['id']
    version = data['version']
    start_time = data['startTime']
    end_time = data['endTime']
    ios = data['ios']
    android = data['android']
    tester = data['tester']
    remark = data['remark']
    if id == '':
        db.session.add(
            app_version(version=version, start_time=start_time, end_time=end_time, tester=tester, ios=ios,
                        android=android, remark=remark, create_time=datetime.datetime.now()))
        db.session.commit()
    else:
        db.session.execute(f'''update app_version set version = '{version}' ,start_time='{start_time}',end_time='{end_time}',tester='{tester}',ios='{ios}',android='{android}',remark='{remark}',update_time ='{datetime.datetime.now()}' where id = '{id}' ''')
        db.session.commit()
    return jsonify({
        "success": True,
        "msg": "ok",
        "code": 720000,
        "data": True
    }
    )
