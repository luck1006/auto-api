# -*- coding: utf-8 -*-
'''
@author:qianfeng
@time:2018-11-08-19:16
'''
import pymysql

class DbUtility:
    def __init__(self, dbHost, dbPort, dbUser, dbPass, dbName):
        self.__dbHost = dbHost
        self.__dbPort = dbPort
        self.__dbUser = dbUser
        self.__dbPass = dbPass
        self.__dbName = dbName

    def connect(self):
        self.conn = pymysql.connect(self.__dbHost, self.__dbUser, self.__dbPass, self.__dbName, int(self.__dbPort), charset='utf8')
        if self.conn.open == False:
            raise None

    def query(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def insert(self, sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()

    def insertmany(self, sql, param):
        cursor = self.conn.cursor()
        try:
            cursor.executemany(sql, param)
            self.conn.commit()
        except:
            self.conn.rollback()

    def update(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        return cursor.fetchall()


    def close(self):
        self.conn.close()

    @property
    def dbHost(self):
        return self.__dbHost

    @dbHost.setter
    def dbHost(self, value):
        self.__dbHost = value

    @property
    def dbPort(self):
        return self.__dbPort

    @dbPort.setter
    def dbPort(self, value):
        self.__dbPort = value

    @property
    def dbUser(self):
        return self.__dbUser

    @dbUser.setter
    def dbUser(self, value):
        self.__dbUser = value

    @property
    def dbPass(self):
        return self.__dbPass

    @dbPass.setter
    def dbPass(self, value):
        self.__dbPass = value

    @property
    def dbName(self):
        return self.__dbName

    @dbName.setter
    def dbName(self, value):
        self.__dbName = value