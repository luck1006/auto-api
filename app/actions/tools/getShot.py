# -*- coding: utf-8 -*-
# TIME:         7.22
# Author:       zhuhaiyan
# Explain：     调用node.js实现截图功能


from Naked.toolshed.shell import execute_js, muterun_js
from app.actions.tools import sendEmail
import datetime
import socket
import logging
from app.models.models import *
# from app.actions.tools import conf

def getShot(selector,to,cc,subject,content=''):


    arr=selector.split(",")
    type=arr[0]

    # today=str(datetime.date.today())
    hostname = socket.gethostname()
    if (hostname == 'vm-prd-tnauto-occamrazor-185-170.tuniu.org'):
        path = '/opt/tuniu/www/Pandora/iview-admin/src/job/screenshot.js'
        picaddr='/opt/tuniu/www/Pandora/autoapi/logx'
    else:
        if (hostname == 'vm-sit-tnauto-occamrazor-32-130.tuniu.org'):
            path = '/opt/tuniu/www/AutoPlatForm/iview-admin/src/job/screenshot.js'
            picaddr = '/opt/tuniu/www/AutoPlatForm/autoapi/logx'
        else:
            path = '/workspace/iview-admin/src/job/screenshot.js'
            picaddr = '/workspace/autoapi/logx'

    picaddr=picaddr+'/panel-'+type+'.png'

    selector = selector + "," + picaddr


    # 页面截图选择器
    # row=".content-wrapper"
    # panel=".ivu-card"
    # selector='support'+','+row+","+panel
    # to="zhuhaiyan@tuniu.com"
    # subject="本周度假技术支持分析"
    # msg='''<html lang="en">
    #     <body>
    #     <h1>Dear all</h1>
    #     <pre><p style="font-size: 16px">'''+content+'''</p></pre>
    #     <img src="cid:image1">
    #     </body>
    #     </html>'''



    # 调用node.js文件

    result = execute_js(path,selector)
    logging.info(result)
    if result:
        logging.info("success")

        print("截图成功～～")
        # print("??????????????????"+subject)
        sendEmail.send_email(to,subject,content,cc=cc,picaddr=picaddr)
        print("发送邮件成功～～")
        return (True)
    else:
        logging.info("failed")
        print("截图失败～～")
        return (False)