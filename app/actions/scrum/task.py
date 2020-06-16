# -*- coding: UTF-8 -*-


import json, os, sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from app.actions.tools.queryFromSql import queryFromSql
from app.actions.tools.dingding import dd

# args = sys.argv[1]
args = [
    {
        "db": "d_hercules",
        "sqlList": [
            {
                "sql": "select user_id,sum(money) from mob_hercules_user_reward group by user_id  order by sum(money) desc limit 5",
                "desc": "任务总金额top5"
            },
            {
                "sql": "select user_id,sum(money) from mob_hercules_user_reward where to_days(create_time)=to_days(now()) group by user_id having sum(money)>1",
                "desc": "今天获得奖励超过1元"
            }
        ],
        "tokenList": [
            {
                "token": "https://oapi.dingtalk.com/robot/send?access_token=a8d9fb85b4b3ddaef60b7a3b634c683a80e6f839b726db10bbd2c408a639d7dc",
                "desc": "测试群"
            }
        ]
    }
]

if __name__ == '__main__':
    args = sys.argv[1]
    try:
        BUILD_URL = sys.argv[2]
    except:
        BUILD_URL = ''
    args = json.loads(args)

    content = ''
    data = ''
    con1 = ''

    for i in args:
        data = ''
        db = i['db']
        total = 0
        for x in i['sqlList']:
            sql = x['sql']
            desc = x['desc']
            con1 = ''
            if BUILD_URL == '':
                title = "{}{}{}".format('**', desc, '**') + '\n'
            else:
                title = f"##### [{desc}]({BUILD_URL}parameters)  \n"
            d = queryFromSql(db, sql).querySql()
            total += len(d)
            '''
            #感觉应该先判断行 但是之前没有考虑行 后边可以优化噻 后边考虑如果没有数据 把title也不要了 101行
            列名1 列名2
            1     2

            如果行数>1 列>2 显示从第一行开始
                      列<=2 显示从第二行开始
                行数<=1 即 行数=1 仅有列名行 不显示
            '''
            # 如果大于2列 显示列名 否则不显示

            # if len(d[0]) > 2:
            #     for k in d:
            #         # 如果大于1行显示列名 否则不显示
            #         if len(d) > 1:
            #             value = "    ".join(k)
            #             con1 += '- ' + value + '\n'
            #         else:
            #             value = ""
            #             con1 += value
            #             # title = ""
            # else:
            #     for k in d[1:]:
            #         value = "    ".join(k)
            #         con1 += '- ' + value + '\n'
            # data += title + '\n' + con1 + '\n'
        # print(total,len(i['sqlList']))
        # if total > len(i['sqlList']):
        #     content = {
        #         "msgtype": "markdown",
        #         "markdown": {
        #             "title": "数据统计",
        #             "text": data
        #         },
        #         "at": {
        #             "isAtAll": False
        #         }
        #     }
            # test = {
            #     "token": "https://oapi.dingtalk.com/robot/send?access_token=a8d9fb85b4b3ddaef60b7a3b634c683a80e6f839b726db10bbd2c408a639d7dc",
            #     "desc": "机器人测试群"}
            # if test not in i['tokenList']:
            #     i['tokenList'].append(test)
            # for url in i['tokenList']:
            #     dd(content, url['token'])