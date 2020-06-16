# -*- coding: utf-8 -*-
'''
@author:qianfeng
@time:2018-12-19-14:27
'''
import datetime
from flask import make_response
import json


exetime = {
    'startTime' : '2019-07-05 00:00:00',
    'endTime' : '2019-07-11 23:59:59'
}

def nowWeek():
    year = int(exetime["endTime"].split(" ")[0].split('-')[0])
    month = int(exetime["endTime"].split(" ")[0].split('-')[1])
    day = int(exetime["endTime"].split(" ")[0].split('-')[2])
    week = str(datetime.date(year, month, day).isocalendar()[1]) + 'W'
    return week

def nowYear():
    year = int(exetime["endTime"].split(" ")[0].split('-')[0])
    return year


def cors_response(res):
    response = json.dumps(res,ensure_ascii=False)
    response = make_response(response)
    # response.addHeader("Access-Control-Max-Age", "2592000")
    response.headers["Access-Control-Max-Age"]= "2592000"
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,POST,GET,DELETE'
    # response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, t'
    response.headers['Access-Control-Allow-Credentials'] = True
    return response


dbconf = {
    "DB_HOST":"10.28.32.130",
    "DB_PORT":"3306",
    "DB_USER":"root",
    "DB_PASS":"@MonLey880124",
    "DB_NAME":"pandora"
}

"""测试入口"""
#if __name__=='__main__':



