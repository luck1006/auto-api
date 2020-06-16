# -*- coding: UTF-8 -*-

import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


from email.header import Header
import logging
import datetime



# from exchangelib import DELEGATE, Account, Credentials, Configuration, NTLM, Message, Mailbox, HTMLBody
# from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
'''
线上BU/应用研发A部 <g-int-a@tuniu.com>; 
线上BU/应用研发B部 <g-int-b@tuniu.com>; 
线上BU/质量部 <g-int-qa@tuniu.com>; 
线上BU/底层研发部 <g-int-system@tuniu.com>; 
线上BU总监群 <g-int-master@tuniu.com>; 
线上BU/产品部 <g-int-product@tuniu.com>

'''

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')



def send_email(to_addr, subject, message, cc=None, subtype='html', picaddr=""):
    """
    :param to_addr str: 收件人
    :param cc str: 抄送
    :param subject str: 主题
    :param message str: 内容
    :param subtype str: 发送类型
    :param picaddr str: 图片相关
    :return:
    """
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    print(now_time)

    smtp_server = 'mail.tuniu.com'
    from_addr = 'pandora@tuniu.com'
    password = 'projectX-IN2'
    user = 'pandora'
    if isinstance(to_addr, str) and (isinstance(cc, str) or cc == None):
        to_addrs = to_addr.split(',')
        # 邮件发送到潘多拉 用于备份
        to_addrs.append('pandora@tuniu.com')
        ssl = []
        if cc != None:
            ssl = cc.split(',')
        to_addrs += ssl

        msg = MIMEMultipart('related')
        msg['Subject'] = subject
        msg['from'] = from_addr
        msg['to'] = to_addr
        msg['Cc'] = cc

        if picaddr != "":
            message1 = '''<html lang="en">
                   <body>
                   <h1>Dear all</h1>
                   <pre><p style="font-size: 16px">''' + message + '''</p></pre>
                   <img src="cid:image%s">
                   </body>
                   </html>'''%(str(now_time))
            message=message1
            msg.attach(MIMEText(message, f'{subtype}', 'utf-8'))
            fp = open(picaddr, 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()
            # 定义图片 ID，在 HTML 文本中引用
            msgImage.add_header('Content-ID', '<image%s>' % (str(now_time)))
            msg.attach(msgImage)
        else:
            msg.attach(MIMEText(message, f'{subtype}', 'utf-8'))



        # ctype = 'application/octet-stream'
        # maintype, subtype = ctype.split('/', 1)
        # 附件-图片
        # image = MIMEImage(open(picaddr, 'rb').read(), _subtype=subtype)
        # image.add_header('Content-Disposition', 'attachment', filename=str(now_time)+'.jpg')
        # msg.attach(image)



        # if picaddr != "":
        #     with open(picaddr, 'rb') as f:
        #         mime = MIMEBase('image', 'png', filename=str(now_time)+'.png')
        #         mime.add_header('Content-Disposition', 'attachment', filename=str(now_time)+'.png')
        #         mime.add_header('Content-ID', '<image1>')
        #         mime.add_header('X-Attachment-Id', '0')
        #         # mime.set_payload(f.read())
        #         # encoders.encode_base64(mime)
        #         msg.attach(mime)

        server = smtplib.SMTP(smtp_server, 25)
        server.login(user, password)
        server.sendmail(from_addr, to_addrs, msg.as_string())
        logging.info(f'to_addrs: {to_addrs}')
        logging.info(f'msg.as_string: {msg.as_string()}')
        server.quit()
    else:
        logging.error('发送邮件失败')
        logging.error(f'{to_addr};{subject};{message};{cc};{subtype},{picaddr}')

def send_email_exchange(to_addr, subject, message):
    """
    :param to_addr list: 收件人list
    :param subject str: 主题
    :param message str: 内容
    :return:
    """
    BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter
    cred = Credentials('pandora', 'projectX-IN1')
    config = Configuration(
        server='mail.tuniu.com',
        credentials=cred,
        auth_type=NTLM
    )
    account = Account(
        primary_smtp_address='pandora@tuniu.com',
        config=config,
        autodiscover=False,
        access_type=DELEGATE
    )
    if isinstance(to_addr, list):
        recipients = []
        for i in to_addr:
            recipients.append(Mailbox(email_address=i))
    else:
        recipients = [Mailbox(email_address=to_addr)]

    m = Message(
        account=account,
        folder=account.sent,
        subject=subject,
        body=HTMLBody(message),
        to_recipients=recipients
    )
    m.send_and_save()


if __name__ == '__main__':
    send_email(to_addr='sunchuanxin@tuniu.com', subject='6666', message='hhhh', cc='sunchuanxin94@dingtalk.com')