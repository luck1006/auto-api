# -*- coding: utf-8 -*-
# TIME:         下午7:13
# Author:       xutaolin

from flask import Flask  # 引入Flask类
from flask_cors import CORS
from config import config
import socket
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask import Response, Request
from werkzeug.datastructures import Headers

app = Flask(__name__)  # app是Flask的实例
cache = Cache()

CORS(app, supports_credentials=True)  # 用于处理跨域问题


class MyResponse(Response):
    def __init__(self, response=None, **kwargs):
        kwargs['headers'] = ''
        headers = kwargs.get('headers')
        # 跨域控制
        header = ('Access-Control-Allow-Headers', "*")
        origin = ('Access-Control-Allow-Origin', '*')
        methods = ('Access-Control-Allow-Methods', 'HEAD, OPTIONS, GET, POST, DELETE, PUT')
        if headers:
            headers.add(*origin)
            headers.add(*methods)
            headers.add(*header)
        else:
            headers = Headers([origin, methods, header])
        kwargs['headers'] = headers
        return super().__init__(response, **kwargs)


def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app=app)
    app.response_class = MyResponse
    # register_logging(app)
    return app


hostname = socket.gethostname()
if (hostname == 'vm-prd-tnauto-occamrazor-185-170.tuniu.org'):
    app = create_app('production')
else:
    app = create_app('default')
db = SQLAlchemy(app)  # 实例化db对象
cache.init_app(app)
