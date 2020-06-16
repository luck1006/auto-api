# -*- coding: utf-8 -*-
# TIME:         7.22
# Author:       zhuhaiyan
# Explain：     截图并发送邮件


from flask import Blueprint
import json
import time
from flask import current_app,request
from app.actions.tools.getShot import getShot
from app.actions.tools.conf import cors_response
from concurrent.futures import ThreadPoolExecutor
import logging
executor =ThreadPoolExecutor(1)



# 设置蓝图
shotEmail = Blueprint('shotEmail', __name__)

@shotEmail.route('/shotEmail',methods=['GET','POST'])

def shot():
    data = request.get_json('data')
    executor.submit(getShotEail,data)
    response = {"success": "true", "msg": "请稍后查看邮箱是否收到邮件~~"}
    return cors_response(response)

def getShotEail(data):
    logging.info("异步调用～～")
    url = data['url']
    subject = data['subject']
    to =data['to'] # 收件人
    cc=data['cc'] # 抄送人
    type=data['type'] #截图类型
    row=data['row'] #selector 选择器
    panel=data['panel'] #selector 选择器
    content=data['content']
    '''
    :param selector str: 选择器，需要截图的row 和 panel 的class
    :param to str: 收件人地址
    :param to subject: 邮件主题
    '''
    # type="support"

    # hostname = socket.gethostname()
    # if (hostname == 'vm-prd-tnauto-occamrazor-185-170.tuniu.org'):
    #     url = 'http://pandora.tuniu.org/support'
    # else:
    #     if (hostname == 'vm-sit-tnauto-occamrazor-32-130.tuniu.org'):
    #         url = 'http://10.28.32.130/support'
    #     else:
    #         url = "http://localhost:8082/support"

    # row = ".content-wrapper"
    # panel = ".ivu-card"
    selector =type+',' +url+','+ row + "," + panel
    # to= "zhuhaiyan@tuniu.com"
    # subject="本周度假技术支持分析"

    try:
        if getShot(selector,to,cc,subject,content):
            logging.info("aa")
            response={"success": "true", "msg": "发送邮件成功~~"}
        else:
            logging.info("bb")
            response = {"success": "false", "msg": "发送邮件失败~~"}

    except Exception as e:
        raise e
        response = {"success": "false", "msg": "发送邮件失败~~"}
    response = json.dumps(response,ensure_ascii=False)
    return cors_response(response)