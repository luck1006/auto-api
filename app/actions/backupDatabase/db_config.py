# -*- coding: utf-8 -*-
# TIME:         下午1:12
# Author:       xutaolin
import time
#定义服务器，用户名、密码、数据库名称（多个库分行放置）和备份的路径
class Config(object):
    DB_HOST='10.28.32.130'
    DB_USER = 'root'
    DB_USER_PASSWD='@MonLey880124'
    DB_NAME='pandora'
    BACKUP_PATH = '/opt/tuniu/www/db_bak/'
    DATETIME = time.strftime('%Y%m%d-%H%M%S')
    TODAYBACKUPPATH = BACKUP_PATH + DATETIME

