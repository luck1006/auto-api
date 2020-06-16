#!/usr/bin env python3
import os,sys
sys.path.append('../../../')
os.path.abspath('../../../')
from app.actions.backupDatabase import db_config
import json,requests
import time
import hmac
import hashlib
import base64
import urllib.parse
#定义执行备份脚本，读取配置文件
def run_backup():
        dbname=db_config.Config.DB_NAME
        dbname = dbname.strip()
        print("now starting backup database %s" %dbname)
        print('开始备份')
        #Linux执行的是时候 需要把'--column-statistics=0'去掉
        # dumpcmd = "mysqldump" +' --column-statistics=0 '+' -h '+db_config.Config.DB_HOST +' -u '+db_config.Config.DB_USER + " -p"+db_config.Config.DB_USER_PASSWD+" " +dbname+" > "+db_config.Config.TODAYBACKUPPATH +".sql"
        dumpcmd = "mysqldump"+' -h '+db_config.Config.DB_HOST +' -u '+db_config.Config.DB_USER + " -p"+db_config.Config.DB_USER_PASSWD+" " +dbname+" > "+db_config.Config.TODAYBACKUPPATH +".sql"
        os.system(dumpcmd)
        print('备份结束')

#执行压缩的函数
def run_tar():
        print('开始压缩')
        compress_file = db_config.Config.TODAYBACKUPPATH + ".tar.gz"
        compress_cmd = "tar -czvf " +compress_file+" "+db_config.Config.DATETIME+".sql"
        os.chdir(db_config.Config.BACKUP_PATH)
        os.system("pwd")
        os.system(compress_cmd)
        print("压缩完成!")
        #删除备份文件夹
        remove_cmd = "rm -rf "+db_config.Config.DATETIME+".sql"
        os.system(remove_cmd)
        print("删除sql文件成功")
#删除 n天前生成的 文件夹
def rm_before_eight_days_files():
        try:
                os.chdir(db_config.Config.BACKUP_PATH)
                #删除最后一次文件内容修改发生在 (n+1)天 之外
                rm_cmd='find'+ " "+db_config.Config.BACKUP_PATH + ' '+'-name "*" -mtime +7 -exec rm -rfv {} \;'
                # rm_cmd='find /Users/xutaolin/AutoPlatForm/autoapi/test/ -name "*" -mmin +2 -exec rm -rfv {} \;'
                print(rm_cmd)
                os.system(rm_cmd)
                print('删除8天之前的文件')
        except:
                print("删除文件失败")


def dingMessage(content):
        #获取时间戳以及签名
        timestamp = round(time.time() * 1000)
        secret = 'SEC844989635f2814568700d91bf7f22d74d76607dd6611343eff1e22a95430db1c'
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        print(timestamp)
        print(sign)
        #WebHook地址
        webhook = "https://oapi.dingtalk.com/robot/send?access_token=895b1044c5e485221895901b8d7130fd97253d09bdaef06bf9b4b229f30fcdb9&timestamp="+str(timestamp)+'&'+'sign='+sign
        #请求头
        header ={"Content-Type":"application/json","charset":"utf-8"}
        # 是指发送信息内容
        infoPs = '## 数据库备份\n' + content + '\n'

        txt = {"msgtype": "markdown",
               "markdown": {
                   "title": "数据库备份",
                   "text": infoPs,
                   "at": {
                       "isAtAll": True
                   }
               },
               }
        # 转成json对象
        message_json = json.dumps(txt).encode('utf-8')
        # 发送钉钉信息
        msg = requests.post(url=webhook, data=message_json, headers=header)
        # 打印返回值
        print(msg.text)


if __name__ == '__main__':
        print(db_config.Config.BACKUP_PATH)
        # 创建备份文件夹
        if not os.path.exists(db_config.Config.BACKUP_PATH):
                os.makedirs(db_config.Config.BACKUP_PATH)
        try:
                #备份
                run_backup()
                #压缩
                run_tar()
                #删除多余文件，节省空间
                rm_before_eight_days_files()
                #发动钉钉
                dingMessage("备份成功")
        except Exception as e:
                print(e)
                # 发动钉钉
                dingMessage("备份失败")


