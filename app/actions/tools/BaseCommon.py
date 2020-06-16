# -*- coding:UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import json
import jsonpath
import datetime
import sys
import os
import platform
from app.actions.tools import config
#'%(asctime)s - %(pathname)s %(filename)s %(funcName)s %(lineno)s - %(levelname)s - %(message)s'
# logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(pathname)s[line:%(lineno)s] - %(levelname)s - %(message)s')

class logger:
    def __init__(self):
        # self.loggers = logging.getLogger(__name__)
        self._setLevel(config.loggerlevel)
        self.dateFlag=datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
    def debug(self, message):
        self._println(message,"DEBUG")
        # self.loggers.debug(message)
    def info(self, message):
        self._println(message, "INFO")
        # self.loggers.info(message)
    def warning(self, message):
        self._println(message, "WARNING")
        # self.loggers.warn(message)
    def error(self, message):
        frame = sys._getframe()
        list=[]
        strs=""
        self._errorLog(frame,list)
        for obj in list:
            strs+=obj+"\n"
        strs=strs.strip("\n")
        self._println(message+"\n"+strs, "ERROR")
        # self.loggers.error(message+"\n"+strs)
        # print("\033[1;31;40m"+strs+"\033[0m")
    def exception(self,message):
        self.error(message)
        exit()
    def _errorLog(self,frame,strs):
        if(frame.f_back!=None):
            strs.append("   "+frame.f_code.co_filename + ",line " + str(frame.f_lineno) + ", in " + frame.f_code.co_name)
            self._errorLog(frame.f_back,strs)
        else:
            strs.append("   "+frame.f_code.co_filename + ",line " + str(frame.f_lineno) + ", in " + frame.f_code.co_name)

    def _println(self,message,type):
        switch = {
            "DEBUG":36,
            "INFO":37,
            "WARNING":35,
            "ERROR":31
        }
        if type in self.level:
            strMessage=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" - "+sys._getframe().f_back.f_back.f_code.co_filename+"[line "+str(sys._getframe().f_back.f_back.f_lineno)+"]"+" - "+str(type)+":" + str(message)
            print("\033[1;" + str(switch[type]) + ";0m" + strMessage+ "\033[0m")
            if config.loggerWrite:
                basePath = os.path.dirname(os.path.realpath(__file__))
                if 'Windows' in platform.system():
                    separator = '\\'
                else:
                    separator = '/'
                p = basePath.split(separator)
                basePath = basePath[:(0 - len(p[len(p) -1])-len(p[len(p) -2]))-1]
                filename = basePath + "log" + separator + "log" + separator + "catalina_"+self.dateFlag+".out"
                if not os.path.exists(filename):
                    f2=open(filename, 'w')
                    f2.close()
                f=open(filename, 'a')  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                f.write(strMessage+"\n")
                f.close()

            # print("\033[1;"+str(switch[type])+";0m"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" - "+sys._getframe().f_back.f_back.f_code.co_filename+"[line "+str(sys._getframe().f_back.f_back.f_lineno)+"]"+" - "+str(type)+":" + str(message) + "\033[0m")


    def _setLevel(self,level):
        if level==10:
            self.level=["DEBUG","INFO","WARNING","ERROR"]
        elif level==20:
            self.level = ["INFO", "WARNING", "ERROR"]
        elif level==30:
            self.level = ["WARNING", "ERROR"]
        elif level==40:
            self.level = ["ERROR"]

class BaseCommon:
    WARNING = 30
    INFO = 20
    DEBUG = 10
    ERROR = 40
    # invokefuncName = sys._getframe().f_code.co_name  # 获取执行函数名
    # invokdelineNumber = sys._getframe().f_lineno  # 获取行号
    # invokefuncName2 = sys._getframe().f_back.f_code.co_name  # 获取调用函数名
    # invokdelineNumber2= sys._getframe().f_back.f_lineno  # 获取行号
    loggers=logger()
    def jsonloads(self,dictstr):
        #r= json.dumps(dictstr)
        return json.loads(dictstr)
    def jsonpath(self,jsonstr,jsonpaths):
        jsonpath.jsonpath(jsonstr,jsonpaths)

    def send_mail(self,title, messages,to_addr=['tangmingyuan@tuniu.com']):
        from_addr = r'wangdan8@tuniu.com'  # 设置发件人邮箱地址
        password = r'@tuniu0422'  # 发件人邮箱密码
        # SMTP服务器
        smtp_server = 'smtp.tuniu.com'  # 设置SMTP服务器
        msg = MIMEText(messages, 'html', 'utf-8')
        # 设置邮件主题（要先实例化msg后才能设置主题）
        msg['From'] = from_addr
        msg['To'] = ','.join(to_addr)  # 据说这是一个bug，只有这样才能群发邮件
        msg['Subject'] = title
        try:
            # 连接服务器发送邮件
            server = smtplib.SMTP(smtp_server, 25)
            server.connect(smtp_server)
            # server.starttls()  #开启加密传输
            # server.set_debuglevel(1)
            server.login(from_addr, password)
            server.sendmail(from_addr, to_addr, msg.as_string())
        except:
            print("邮件发送失败！")
        else:
            print("邮件发送成功！")
        finally:
            server.quit()

    def send_email_addtion_html(self,path,subject='', content='',recipientAddrs=['g-PJB-qc@tuniu.com']):
        user = r"autoreminders"
        # sendAddr = r'autoreminders@tuniu.com'  # 设置发件人邮箱地址
        sendAddr = user + r'@tuniu.com'  # 设置发件人邮箱地址
        password = r'@tuniu04220'  # 发件人邮箱密码
        # recipientAddrs= r'tangmingyuan@tuniu.com'
        smtpHost= 'smtp.tuniu.com'
        msg = MIMEMultipart()
        msg['from'] = sendAddr
        msg['to'] = ','.join(recipientAddrs)
        msg['subject'] = subject
        content = content
        # txt = email.mime.text.MIMEText(content, 'plain', 'utf-8')
        txt = MIMEText(content, 'html', 'utf-8')
        msg.attach(txt)

        # 添加附件，传送D:/软件/yasuo.rar文件
        part = MIMEApplication(open(path, 'rb').read())
        part.add_header('Content-Disposition', 'html', filename="自动化测试报告.html")
        msg.attach(part)

        smtp = smtplib.SMTP()

        smtp.connect(smtpHost)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(user, password)
        smtp.sendmail(sendAddr, recipientAddrs, str(msg))
        # smtp.connect(smtpHost, '25')
        # smtp.login(sendAddr, password)
        # smtp.sendmail(sendAddr, recipientAddrs, str(msg))
        print("发送成功！")
        smtp.quit()
        result = {"success": True}
        return result
