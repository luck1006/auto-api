# -*- coding: utf-8 -*-
import json, time
from urllib.parse import unquote, quote
from flask import Blueprint, request
from app import cache
from app.actions.tools.queryFromSql import queryFromSql
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Page, Pie
from pyecharts.globals import CurrentConfig, ThemeType
from pyecharts.commons.utils import JsCode
import logging

# 关于 CurrentConfig，可参考 [基本使用-全局变量]
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))

# 引用的js
CurrentConfig.ONLINE_HOST = 'http://121.199.57.163:8080/var/www/echartsjs/'
echart = Blueprint('tnechart', __name__)


def line_markpoint(x_list, y_line_list, title) -> Line:
    line = Line(init_opts=opts.InitOpts())
    line.set_colors(['#f00915', '#fdc043', '#1d953f', '#411445'])
    line.set_global_opts(title_opts=opts.TitleOpts(title=title))
    for x in x_list:
        line.add_xaxis(x)
    for y in y_line_list:
        for k, v in y.items():
            line.add_yaxis(k, v, is_smooth=True,
                           markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]))
    return line


def bar_datazoom_slider(x_list, y_bar_list, title) -> Bar:
    bar = Bar(init_opts=opts.InitOpts(
        page_title='echart'))
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        toolbox_opts=opts.ToolboxOpts()
    )
    for x in x_list:
        bar.add_xaxis(x)
    for y in y_bar_list:
        for k, v in y.items():
            bar.add_yaxis(k, v)
    return bar


def jajj(data):
    page = Page(layout=Page.SimplePageLayout)
    map = None
    for i in data:
        title = i['title']
        db = i['db']
        sql = i['sql']
        type = i['type']
        d_soure = queryFromSql(db, sql, 0).toechart()
        y_bar_list = []
        y_line_list = []
        x_list = []
        bar_line_list = []
        for i in range(len(d_soure)):
            try:
                if type[i] == 0:
                    x = d_soure[i][1:]
                    x_list.append(x)
                elif type[i] == 1:
                    y = {d_soure[i][0]: d_soure[i][1:]}
                    y_bar_list.append(y)
                elif type[i] == 2:
                    y = {d_soure[i][0]: d_soure[i][1:]}
                    y_line_list.append(y)
                try:
                    bar = bar_datazoom_slider(x_list, y_bar_list, title)
                except Exception as e:
                    logging.exception(e)
                try:
                    if y_line_list != []:
                        line = line_markpoint(x_list, y_line_list, title)
                except Exception as e:
                    logging.exception(e)
                finally:
                    if 2 in type:
                        map = bar.overlap(line)
                    else:
                        map = bar
            except Exception as e:
                logging.exception(e)
        page.add(map)
    return Markup(page.render_embed())


@echart.route('/echart/hi/<p>')
@cache.cached(query_string=True, timeout=60 * 60 * 4)
def hi(p):
    # time.sleep(1)
    d = {"id": 1}
    return json.dumps(d)


@echart.route("/echart")
@cache.cached(query_string=True, timeout=60 * 60 * 4)
def aaa():
    query_string = request.query_string.decode('utf-8')
    query_string = unquote(query_string)
    para_dict = json.loads(query_string)
    name = para_dict['name']
    para = {}
    rp_81 = [
        {
            "db": "d_mob_rp",
            "sqlList": [
                {
                    "sql": "select hour(create_time) 时间,count(id) 新建红包数 from rp_base_info  where activity_id = 81 and create_time>'2019-11-18 18:00' group by hour(create_time) order by hour(create_time)",
                    "desc": "81新建红包数",
                    "type": [0, 1]
                }
            ]
        }
    ]
    yunji = [
        {
            "db": "d_mdt",
            "sqlList": [
                {
                    "sql": "select date_format(add_time,'%m-%d') 日期,count(*) 订单数 from user_order  where add_time >= date_add(now(), INTERVAL - 30 day) group by date_format(add_time,'%m-%d') order by date_format(add_time,'%m-%d')",
                    "desc": "云集酒店订单数", "type": [0, 1]
                },
                {
                    "sql": "select date_format(add_time,'%m-%d') 日期,sum(payed_prices) 订单金额 from user_order  where add_time >= date_add(now(), INTERVAL - 30 day) group by date_format(add_time,'%m-%d') order by date_format(add_time,'%m-%d')",
                    "desc": "云集酒店订单金额", "type": [0, 1]
                },
                {
                    "sql": "select date_format(add_time,'%m-%d') 日期,count(*) 签约订单数 from user_order  where add_time >= date_add(now(), INTERVAL - 30 day) and order_status in ('待入住','已入住','已离店') group by date_format(add_time,'%m-%d') order by date_format(add_time,'%m-%d') ",
                    "desc": "云集酒店签约订单数", "type": [0, 1]
                },
                {
                    "sql": "select date_format(add_time,'%m-%d') 日期,sum(payed_prices) 签约订单金额 from user_order  where add_time >= date_add(now(), INTERVAL - 30 day) and order_status in ('待入住','已入住','已离店') group by date_format(add_time,'%m-%d') order by date_format(add_time,'%m-%d') ",
                    "desc": "云集酒店签约订单金额", "type": [0, 1]
                }
            ]
        }
    ]
    hercules = [
        {
            "db": "fab",
            "sqlList": [
                {
                    "sql": "select date_format(add_time,'%H') 时间,count(distinct cust_id) 用户数 from sign_gift_record  where add_time >= curdate() group by date_format(add_time,'%H') order by date_format(add_time,'%H')",
                    "desc": "签到分时用户数",
                    "type": [
                        0,
                        1
                    ]
                },
                {
                    "sql": "select date(add_time) 时间,count(distinct cust_id) 用户数 from sign_gift_record  where add_time >= date_add(now(), INTERVAL - 30 day) group by date(add_time) order by date(add_time)",
                    "desc": "签到分日用户数",
                    "type": [
                        0,
                        1
                    ]
                }
            ]
        },
        {
            "db": "d_hercules",
            "sqlList": [
                {
                    "sql": "select hour(create_time),count(distinct user_id) 用户数 from mob_hercules_user_task where create_time >= curdate() group by hour(create_time) order by hour(create_time) ",
                    "desc": "任务中心分时用户数",
                    "type": [
                        0,
                        1
                    ]
                },
                {
                    "sql": "select date(create_time) ,count(distinct user_id) 用户数 from mob_hercules_user_task where create_time >= date_add(now(), INTERVAL - 30 day) group by date(create_time) order by date(create_time)",
                    "desc": "任务中心分日用户数",
                    "type": [
                        0,
                        1
                    ]
                },
                {
                    "sql": "select date_format(create_time,'%m'),count(distinct user_id) 用户数 from mob_hercules_user_task group by date_format(create_time,'%m') order by date_format(create_time,'%m') ",
                    "desc": "任务中心分月用户数",
                    "type": [
                        0,
                        1
                    ]
                },
                {
                    "sql": "SELECT date_format(finish_time, '%H'), COUNT(*) AS 任务数 FROM mob_hercules_user_task WHERE finish_time >= curdate() GROUP BY date_format(finish_time, '%H') order by finish_time ",
                    "desc": "任务中心分时任务数",
                    "type": [
                        0,
                        1
                    ]
                },
                {
                    "sql": "select date_format(finish_time,'%m-%d') ,count(*) 任务数 from mob_hercules_user_task where finish_time >= date_add(now(), INTERVAL - 30 day) group by date_format(finish_time,'%m-%d') order by date_format(finish_time,'%m-%d')",
                    "desc": "任务中心分日任务数",
                    "type": [
                        0,
                        1
                    ]
                },
                {
                    "sql": "select date_format(finish_time,'%m'),count(*) 任务数 from mob_hercules_user_task where finish_time >= date_add(now(), INTERVAL - 6 month) group by date_format(finish_time,'%m') order by date_format(finish_time,'%m')",
                    "desc": "任务中心分月任务数",
                    "type": [
                        0,
                        1
                    ]
                }
            ]
        }
    ]
    guwen = [
        {
            "db": "d_mob_yxim",
            "sqlList": [
                {
                    "sql": "select A.a 时间,A.用户发送消息数,case when B.客服发送消息数 > 0 then B.客服发送消息数 else 0 end 客服发送消息数 from ( select date_format(msg_timestamp,'%H') a,count(*) 用户发送消息数 from mob_yxim_conversation_message where to_user_identifier IN (SELECT user_identifier FROM mob_yxim_user_identity WHERE identity_id = 2)  and conv_type = 'PERSON' AND msg_timestamp >= curdate() group by date_format(msg_timestamp,'%H') order by date_format(msg_timestamp,'%H') ) A left join ( select date_format(msg_timestamp,'%H') b,count(*) 客服发送消息数 from mob_yxim_conversation_message where from_user_identifier IN (SELECT user_identifier FROM mob_yxim_user_identity WHERE identity_id = 2)  and conv_type = 'PERSON' AND msg_timestamp >= curdate() group by date_format(msg_timestamp,'%H') order by date_format(msg_timestamp,'%H') ) B on A.a = B.b order by  A.a ",
                    "desc": "专业顾问今日咨询和回复用户数",
                    "type": [0, 1, 1]
                },
                {
                    "sql": "select A.a 时间,A.用户发送消息数,case when B.客服发送消息数 > 0 then B.客服发送消息数 else 0 end 客服发送消息数 from ( select date_format(msg_timestamp,'%H') a,count(*) 用户发送消息数 from mob_yxim_conversation_message where to_user_identifier IN (SELECT user_identifier FROM mob_yxim_user_identity WHERE identity_id = 1)  and conv_type = 'PERSON' AND msg_timestamp >= curdate() group by date_format(msg_timestamp,'%H') order by date_format(msg_timestamp,'%H') ) A left join ( select date_format(msg_timestamp,'%H') b,count(*) 客服发送消息数 from mob_yxim_conversation_message where from_user_identifier IN (SELECT user_identifier FROM mob_yxim_user_identity WHERE identity_id = 1)  and conv_type = 'PERSON' AND msg_timestamp >= curdate() group by date_format(msg_timestamp,'%H') order by date_format(msg_timestamp,'%H') ) B on A.a = B.b  order by A.a",
                    "type": [0, 1, 1],
                    "desc": "专属顾问今日咨询和回复用户数"
                },
                {
                    "sql": "select A.a 日期,A.咨询用户数,B.回复用户数,B.回复用户数/A.咨询用户数*100 回复率 from ( SELECT date_format(msg_timestamp,'%m-%d') a,count(DISTINCT from_user_identifier) 咨询用户数 FROM mob_yxim_conversation_message WHERE to_user_identifier IN (SELECT user_identifier FROM mob_yxim_user_identity WHERE identity_id = 2) AND conv_type = 'PERSON' AND msg_timestamp > date_add(now(), INTERVAL - 30 day) group by date_format(msg_timestamp,'%m-%d') order by date_format(msg_timestamp,'%m-%d')) A left join ( SELECT date_format(msg_timestamp,'%m-%d') b,count(distinct to_user_identifier) 回复用户数 from mob_yxim_conversation_message where from_user_identifier IN (SELECT user_identifier FROM mob_yxim_user_identity WHERE identity_id = 2) and conv_type = 'PERSON' AND msg_timestamp > date_add(now(), INTERVAL - 30 day) group by date_format(msg_timestamp,'%m-%d') order by date_format(msg_timestamp,'%m-%d')) B on A.a = B.b",
                    "type": [0, 1, 1, 2],
                    "desc": "专业顾问咨询和回复用户数"
                },
                {
                    "sql": "select A.a 日期,A.咨询用户数,B.回复用户数 from ( SELECT date_format(msg_timestamp,'%m-%d') a,count(DISTINCT from_user_identifier) 咨询用户数 FROM mob_yxim_conversation_message WHERE to_user_identifier IN (SELECT user_identifier FROM mob_yxim_user_identity WHERE identity_id = 1) AND conv_type = 'PERSON' AND msg_timestamp > date_add(now(), INTERVAL - 30 day) group by date_format(msg_timestamp,'%m-%d') order by date_format(msg_timestamp,'%m-%d')) A left join ( SELECT date_format(msg_timestamp,'%m-%d') b,count(distinct to_user_identifier) 回复用户数 from mob_yxim_conversation_message where from_user_identifier IN (SELECT user_identifier FROM mob_yxim_user_identity WHERE identity_id = 1) and conv_type = 'PERSON' AND msg_timestamp > date_add(now(), INTERVAL - 30 day) group by date_format(msg_timestamp,'%m-%d') order by date_format(msg_timestamp,'%m-%d')) B on A.a = B.b",
                    "type": [0, 1, 1],
                    "desc": "专属顾问咨询和回复用户数"
                },
                {
                    "sql": "select A.a 日期,A.用户发送消息数,B.客服发送消息数 from ( select date_format(msg_timestamp,'%m-%d') a,count(*) 用户发送消息数 from mob_yxim_conversation_message where to_user_identifier IN (SELECT user_identifier FROM mob_yxim_user_identity WHERE identity_id = 2)  and conv_type = 'PERSON' AND msg_timestamp > date_add(now(), INTERVAL - 15 day) group by date_format(msg_timestamp,'%m-%d') order by date_format(msg_timestamp,'%m-%d') ) A left join ( select date_format(msg_timestamp,'%m-%d') b,count(*) 客服发送消息数 from mob_yxim_conversation_message where from_user_identifier IN (SELECT user_identifier FROM mob_yxim_user_identity WHERE identity_id = 2)  and conv_type = 'PERSON' AND msg_timestamp > date_add(now(), INTERVAL - 15 day) group by date_format(msg_timestamp,'%m-%d') order by date_format(msg_timestamp,'%m-%d') ) B on A.a = B.b",
                    "type": [0, 1, 1],
                    "desc": "专业顾问咨询消息数"
                },
                {
                    "sql": "select A.a 日期,A.用户发送消息数,B.客服发送消息数 from ( select date_format(msg_timestamp,'%m-%d') a,count(*) 用户发送消息数 from mob_yxim_conversation_message where to_user_identifier IN (SELECT user_identifier FROM mob_yxim_user_identity WHERE identity_id = 1)  and conv_type = 'PERSON' AND msg_timestamp > date_add(now(), INTERVAL - 15 day) group by date_format(msg_timestamp,'%m-%d') order by date_format(msg_timestamp,'%m-%d') ) A left join ( select date_format(msg_timestamp,'%m-%d') b,count(*) 客服发送消息数 from mob_yxim_conversation_message where from_user_identifier IN (SELECT user_identifier FROM mob_yxim_user_identity WHERE identity_id = 1)  and conv_type = 'PERSON' AND msg_timestamp > date_add(now(), INTERVAL - 15 day) group by date_format(msg_timestamp,'%m-%d') order by date_format(msg_timestamp,'%m-%d') ) B on A.a = B.b",
                    "type": [0, 1, 1],
                    "desc": "专属顾问咨询消息数"
                }
            ]
        }
    ]
    t_1288 = [
        {
            "db": "d_mob_reward",
            "sqlList": [
                {
                    "sql": "select date_format(send_time,'%H'),count(distinct user_id) 用户数 from mob_reward_topic_task_reward where topic_id = 5 and send_time >= curdate() group by date_format(send_time,'%H') order by date_format(send_time,'%H')",
                    "desc": "1288分时用户数", "type": [0, 1]
                },
                {
                    "sql": "select date_format(send_time,'%m-%d') ,count(distinct user_id) 用户数 from mob_reward_topic_task_reward where topic_id = 5 and send_time >= date_add(now(), INTERVAL - 30 day) group by date_format(send_time,'%m-%d') order by date_format(send_time,'%m-%d')",
                    "desc": "1288分日用户数", "type": [0, 1]
                },
                {
                    "sql": "select date_format(send_time,'%m'),count(distinct user_id) 用户数 from mob_reward_topic_task_reward where send_time >= date_add(now(), INTERVAL - 6 month) group by date_format(send_time,'%m') order by date_format(send_time,'%m')",
                    "desc": "1288分月用户数", "type": [0, 1]
                }
            ]
        }
    ]
    guwen_maiyidu = [
        {
            "db": "adv_mng",
            "sqlList": [
                {
                    "sql": "select date_format(add_time,'%m-%d'),count(*) from adviser_comment where add_time >= date_add(now(), INTERVAL - 15 day) group by date_format(add_time,'%m-%d')",
                    "desc": "专业顾问分日评论数", "type": [0, 1]

                },
                {
                    "sql": "select date_format(add_time,'%m-%d'),avg(comment_star) from adviser_comment where add_time >= date_add(now(), INTERVAL - 15 day) group by date_format(add_time,'%m-%d')",
                    "desc": "专业顾问分日满意度", "type": [0, 1]
                },
                {
                    "sql": "select comment_star,count(*) from adviser_comment where add_time >= date_add(now(), INTERVAL - 7 day) group by comment_star",
                    "desc": "专业顾问近7天满意度分布", "type": [0, 1]
                }
            ]
        },
        {
            "db": "nebula",
            "sqlList": [
                {
                    "sql": "select date_format(add_time,'%m-%d'),count(*) from tb_vip_saler_comment where add_time >= date_add(now(), INTERVAL - 15 day) group by date_format(add_time,'%m-%d')",
                    "desc": "专属顾问分日评论数", "type": [0, 1]
                },
                {
                    "sql": "select date_format(add_time,'%m-%d'),avg(comment_star) from tb_vip_saler_comment where add_time >= date_add(now(), INTERVAL - 15 day) group by date_format(add_time,'%m-%d')",
                    "desc": "专属顾问分日满意度", "type": [0, 1]
                },
                {
                    "sql": "select comment_star,count(*) from tb_vip_saler_comment where add_time >= date_add(now(), INTERVAL - 7 day) group by comment_star",
                    "desc": "专属顾问近7天满意度分布", "type": [0, 1]
                }
            ]
        }
    ]
    para['1288'] = t_1288
    para['顾问'] = guwen
    para['云集'] = yunji
    para['任务中心'] = hercules
    para['顾问满意度'] = guwen_maiyidu
    para['rp_81'] = rp_81
    data = []
    para = json.dumps(para)
    para = json.loads(para)
    for s in para[name]:
        db = s['db']
        sqlList = s['sqlList']
        for p in sqlList:
            try:
                title = p['desc']
                sql = p['sql']
                type = p['type']
            except Exception as e:
                type = None
            one = {
                "db": db,
                "sql": sql,
                "title": title,
                "type": type
            }
            data.append(one)
    d = jajj(data)
    return d
