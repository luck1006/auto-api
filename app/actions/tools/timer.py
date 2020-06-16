# -*- coding:utf-8 -*-
import datetime
import time
import re
import json


def time_l():
    # 自动计算 上周五到本周四
    now_time = datetime.datetime.now()
    day = now_time.weekday()
    start_time = now_time + datetime.timedelta(days=-day - 3)  # -3
    start_time = start_time.date()  # datetime
    start = start_time.strftime('%Y-%m-%d')  # str
    end_time = now_time + datetime.timedelta(3 - day)
    end_time = end_time.date()  # datetime
    end = end_time.strftime('%Y-%m-%d')  # str
    return start_time, end_time, start, end, day


def save(filename, contents):
    fh = open(filename, 'w', encoding='utf-8')
    fh.write(contents)
    fh.close()


def times2d(time):
    s_time = datetime.datetime.strptime(time, "%Y-%m-%d").date()
    return s_time


def timed2s(time):
    time = time.strftime('%Y-%m-%d')
    return time


def time2any(str):
    try:
        struct_time = time.strptime(str, '%Y-%m-%d')
    except:
        struct_time = time.strptime(str, '%Y-%m-%d %H:%M:%S')
    # print(struct_time)
    tm_year = struct_time.tm_year
    tm_mon = struct_time.tm_mon
    tm_mday = struct_time.tm_mday  # 周几
    tm_hour = struct_time.tm_hour
    tm_min = struct_time.tm_min
    tm_sec = struct_time.tm_sec
    tm_wday = struct_time.tm_wday
    tm_yday = struct_time.tm_yday  # 今年第几天
    timestamp = int(time.mktime(struct_time) * 1000)
    W = int(datetime.datetime(tm_year, tm_mon, tm_mday).strftime("%W")) + 1  # 今年第几周
    res = {
        "timestamp": timestamp,
        "time": str,
        "year": tm_year,
        "month": tm_mon,
        "day": tm_mday,
        "hour": tm_hour,
        "minute": tm_min,
        "second": tm_sec,
        "week": tm_wday + 1,
        "days": tm_yday,
        "weeks": W
    }
    # print(json.dumps(res))
    return res
