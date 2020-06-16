# -*- coding: utf-8 -*-
'''
@author:qianfeng
@time:2018-11-08-18:23
'''
from app.actions.tools.conf import dbconf
from app.actions.tools.DbUtility import DbUtility

class SaveInit(DbUtility):

    def __init__(self):
        # 获取数据库配置
        super().__init__(dbHost=dbconf["DB_HOST"], dbUser=dbconf["DB_USER"], dbPass=dbconf["DB_PASS"], dbName=dbconf["DB_NAME"],dbPort=dbconf["DB_PORT"])


if __name__=='__main__':
    sql = "select * from time_working_detail"
    save = SaveInit()
    save.connect()
    print(save.query(sql))
    save.close()



