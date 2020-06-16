# -*- coding:UTF-8 -*-
import time
import datetime
import xlrd
import xlwt
import os
# import xlutils.copy
import platform
from os import path
from app.actions.tools.BaseCommon import BaseCommon
#from _01Commonkeyword._01Basemethod.LogHtml import logHtml


class CommonKeyword(BaseCommon):
    # def __init__(self):
    #     self.loggers = self.logger().getLogger(__name__)
    # loggers = BaseCommon().logger().getLogger(__name__)
    def date_s(self,days):
        now = datetime.datetime.now()
        datesum = now.strftime('%Y-%m-%d')
        curday = 1
        while curday < days:
            date = now + datetime.timedelta(days=curday)
            date = date.strftime('%Y-%m-%d')
            datesum = str(datesum)+","+str(date)
            curday=curday+1
        print (datesum)
        return str(datesum)
    def getMap(self,cls):
        map = {}
        for key, value in vars(cls).items():
            if (value != None):
                map[key] = value
        return map
    #设置等待时间
    def wait(self,count):
        self.pyprint("info:" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ":" + self.wait.__name__ + "开始执行",1)
        time.sleep(count)
        self.pyprint("等待"+str(count)+"s",1)
        self.pyprint("info:"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+":"+self.wait.__name__+"执行成功",1)

    #定义变量
    def var(self,var):
        self.pyprint(str(var),1)
        return str(var)
    #打印
    def pyprint(self,printvar,level):
        if level==1:
            self.loggers.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+":"+str(printvar))
        elif level==2:
            self.loggers.error(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ":" + str(printvar))
        elif level==3:
            self.loggers.debug(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ":" + str(printvar))

    def currentdir(self):
        self.pyprint(path.dirname(__file__),1)

    def updir(self):
        self.pyprint(path.dirname(path.dirname(__file__)),1)

    def comparestr(self,str1,str2):
        if str(str1) == str(str2):
            self.pyprint('相等,'+'str1:'+str(str1)+';str2:'+str(str2),1)
        else:
            self.pyprint('不相等,'+'str1:'+str(str1)+';str2:'+str(str2),2)
    def comparenum(self,num1,num2):
        try:
            str(num2).index(str(num1))
            str(num1).index(str(num2))
            self.pyprint('相等,'+'num1:'+str(num1)+';num2:'+str(num2),1)
            return True
        except:
            self.pyprint('不相等,' + 'num1:' + str(num1) + ';num2:' + str(num2), 2)
            return False
    def compare_contains(self,str1,str2):
        try:
            str1 in str2
            self.pyprint("包含："+str1 +"<包含>"+str2,1)
            return True
        except:
            self.pyprint("不包含："+str1 + "<不包含>" + str2, 2)
            return False
    #字符串/数字不相等
    def compare_distrinct(self,opt1,opt2):
        if str(opt1) is not str(opt2):
            self.pyprint('不相等,'+'opt1:'+str(opt1)+';opt2:'+str(opt2),1)
            return True
        else:
            self.pyprint('相等,'+'opt1:'+str(opt1)+';opt2:'+str(opt2),2)
            return True

    #获取excel内容
    def getExcel(self,filepath):
        fname = filepath
        bk = xlrd.open_workbook(fname)
        shxrange = range(bk.nsheets)
        try:
            sh = bk.sheet_by_name("Sheet1")
        except:
            print ("no sheet in %s named Sheet1" % fname)

        return sh
    #获取excel第i行，第j列数据
    def getExcelij(self,filepath,i,j):
        fname = filepath
        bk = xlrd.open_workbook(fname)
        shxrange = range(bk.nsheets)
        try:
            sh = bk.sheet_by_name("Sheet1")
        except:
            print ("no sheet in %s named Sheet1" % fname)

        return sh.row_values(i)[j]
    #写数据到excel,传入数据自动生成excel,excel名称可以自定义







