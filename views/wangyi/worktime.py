# -*- coding: utf-8 -*-
import json
import requests
from dateutil.parser import parse
from prettytable import PrettyTable
import datetime
from urllib.parse import unquote
from flask import request
from flask import Blueprint
import pandas as pd
from app.actions.tools.timer import time2any

null = None
true = True
false = False

wt = Blueprint('wt', __name__, url_prefix="/wt")


def convertToHtml(result, title):
    # 将数据转换为html的table
    # result是list[list1,list2]这样的结构
    # title是list结构；和result一一对应。titleList[0]对应resultList[0]这样的一条数据对应html表格中的一列
    d = {}
    index = 0
    for t in title:
        d[t] = result[index]
        index = index + 1
    df = pd.DataFrame(d)
    df = df[title]
    h = df.to_html(index=False)
    return h


def ding(para):
    content = {
        "msgtype": "text",
        "text": {
            "content": f"{para}"
        },
        "at": {
            "atMobiles": [

            ],
            "isAtAll": false
        }
    }
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }
    requests.post(
        url="https://oapi.dingtalk.com/robot/send?access_token=a8d9fb85b4b3ddaef60b7a3b634c683a80e6f839b726db10bbd2c408a639d7dc",
        headers=headers, data=json.dumps(content).encode('utf-8'))


@wt.route('/worktime', methods=['GET'])
def worktime():
    """
    :param worknum: 工号牌上那个工号
    :param start:
    :param end:
    :return:
    """

    query_string = request.query_string.decode('utf-8')
    query_string = unquote(query_string)
    para_dict = json.loads(query_string)

    worknum = para_dict['worknum']
    start = para_dict['start']
    end = para_dict['end']
    ding(f' {worknum} {start} {end}')
    count = 0  # 总工时
    days = 0  # 总天数
    col_1 = []
    col_2 = []
    col_3 = []
    col_4 = []
    aa = []
    bb = []
    ww = []
    dff = []
    try:
        if start == '':
            local = datetime.datetime.now()
            start_year = local.year
            start_mon = local.month
            end_mon = start_mon - 1
            step = -1

        elif int(end) >= int(start):
            start_year = int(start[:4])
            end_year = int(end[:4])
            diff_year = end_year - start_year
            if diff_year == 0:
                start_mon = int(start[4:])
                end_mon = int(end[4:]) + 1
                step = 1

        for month in range(start_mon, end_mon, step):
            if int(month) < 10:
                month = f'0{month}'
            yearmon = str(start_year) + '-' + str(month)
            r = requests.get(
                f'http://hr.tuniu.com/index.php?m=AttendanceComposite,attendance2,AjaxGetDayresult&yearmon={yearmon}&worknum={worknum}')
            data = r.text.replace('<script>', '').replace('</script>', '').replace(
                "location.href='http://crm.tuniu.com/main.php?do=new_crm';", '')
            data = json.loads(data)
            d = 0
            workday = 0
            for i in data:
                DATENUM = data[i]['cardtime'][0]['DATENUM']
                w = time2any(DATENUM)['week']
                WORKTIME = data[i]['cardtime'][0]['WORKTIME']
                tag = data[i]['html'].replace('<ul><li>', '').replace('</li></ul>', '').replace('</li>', '').replace(
                    '<li>', '')
                y = len(data[i]['cardtime'])
                if y == 2:
                    LEAVETIME = data[i]['cardtime'][1]['LEAVETIME']
                else:
                    LEAVETIME = data[i]['cardtime'][0]['LEAVETIME']
                try:
                    a = parse(WORKTIME)
                    b = parse(LEAVETIME)
                    c = (b - a).seconds
                    if c > 0 and int(w) not in (6, 7):
                        d = d + c
                        workday = workday + 1
                        df = c / 3600
                        aa.append(a)
                        bb.append(b)
                        ww.append(w)
                        dff.append(df)
                    elif c > 0 and int(w) in (6, 7):
                        aa.append(a)
                        bb.append(b)
                        ww.append(w)
                        df = c / 3600
                        dff.append(df)
                    else:
                        aa.append(DATENUM)
                        bb.append(' ')
                        ww.append(w)
                        dff.append(tag)
                except Exception as e:
                    print(e)
            try:
                e = d / 3600 / workday
            except Exception as ex:
                e = 0
                print(ex)
            f = d / 3600
            col_1.append(yearmon)
            col_2.append(f'{workday}')
            col_3.append(f'{f}')
            col_4.append(f'{e}')
            count = count + f
            days += workday
        if days != 0:
            ava = count / days
        else:
            ava = 0
    except Exception as e:
        print(e)
        return ' 不要瞎调！'
    col_1.append('总计')
    col_2.append(days)
    col_3.append(count)
    col_4.append(ava)
    total_table = [col_1, col_2, col_3, col_4]
    tabel = convertToHtml(total_table, title=["月份", "工作天数", "总工时", "平均工时"])
    detail = [aa, bb, dff, ww]
    detail = convertToHtml(detail, title=["上班时间", "下班时间", "工作时间", '周'])
    return tabel + '<br>' + detail
