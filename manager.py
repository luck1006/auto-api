# -*- coding: utf-8 -*-
# TIME:         下午1:23
# Author:       xutaolin
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand  # 载入migrate扩展
import socket

from app.models.models import *

# app = create_app('default')
hostname = socket.gethostname()
if(hostname =='vm-prd-tnauto-occamrazor-185-170.tuniu.org'):
    app = create_app('production')
else:
    app = create_app('default')

manager = Manager(app)
migrate = Migrate(app, db)  # 注册migrate到flask,第一个参数是flask实例，第二个是sqlalchemy实例
manager.add_command('db', MigrateCommand)  # manager是flask_script实例，

if __name__ == '__main__':
    manager.run()
