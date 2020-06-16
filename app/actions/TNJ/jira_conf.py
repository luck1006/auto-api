# -*- coding: UTF-8 -*-
import json
import requests

#  -*-  coding: utf-8  -*-
import pymysql
import time
from DBUtils.PooledDB import PooledDB


# https://www.cnblogs.com/huay/p/11562094.html
class JIRA_CONFIG():
    FLAG = 0

    def __init__(self, *args, **kwargs):
        if JIRA_CONFIG.FLAG:
            return
        print(1111)
        self.jira_db = {}
        r = requests.get('http://magic-box.api.tuniu.org/query/jira/conf')
        # db_port db_host db_user db_password
        for i in json.loads(r.text):
            self.jira_db[i.split('=')[0].replace(' ', '')] = i.split('=')[1].replace(' ', '').replace('\n', '')
        self.POOL = PooledDB(pymysql, 5, host=self.jira_db['db_host'], user=self.jira_db['db_user'],
                             passwd=self.jira_db['db_password'],
                             db='jira', port=int(self.jira_db['db_port']), setsession=[
                'SET AUTOCOMMIT = 1'],
                             cursorclass=pymysql.cursors.DictCursor)  # 5为连接池里的最少连接数，setsession=['SET AUTOCOMMIT = 1']是用来设置线程池是否打开自动更新的配置，0为False，1为True
        JIRA_CONFIG.FLAG = 1
        return

    def __new__(cls, *args, **kw):
        '''
        启用单例模式
        :param args:
        :param kw:
        :return:
        '''
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def connect(self):
        '''
        启动连接
        :return:
        '''
        conn = self.POOL.connection()
        cursor = conn.cursor()
        return conn, cursor

    def connect_close(self, conn, cursor):
        '''
        关闭连接
        :param conn:
        :param cursor:
        :return:
        '''
        cursor.close()
        conn.close()

    def fetch_all(self, sql):
        '''
        批量查询
        :param sql:
        :param args:
        :return:
        '''
        conn, cursor = self.connect()
        cursor.execute(sql)
        record_list = cursor.fetchall()
        self.connect_close(conn, cursor)
        return record_list


def execute(sql):
    url = 'http://magic-box.api.tuniu.org/execute'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {'sql': sql}
    try:
        response = requests.request("POST", url, headers=headers, json=data)
    except Exception as e:
        raise e
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception
    # cur = conn.cursor()
# SQL = 'select * from t_oa_user limit 10 '
# count = cur.execute(SQL)
# print(count)
# results = cur.fetchall()
# print(results)
# cur.close()
# conn.close()
# return results

# d = JIRA_CONFIG()
# d.jira_sql_pool()

# from orm_pool import db_pool
# import pymysql
#
#
# class Mysql(object):
#     def __init__(self):
#         self.conn = db_pool.POOL.connection()
#         self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
#
#     def closed_db(self):
#         self.cursor.close()
#         self.conn.close()
#
#     def select(self, sql, args=None):
#         self.cursor.execute(sql, args)
#         res = self.cursor.fetchall()
#         return res
#
#     def execute(self, sql, args):
#         try:
#             self.cursor.execute(sql, args)
#         except BaseException as e:
