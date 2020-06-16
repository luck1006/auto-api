# -*- coding: utf-8 -*-
# TIME:         下午1:12
# Author:       xutaolin
import socket

hostname = socket.gethostname()


class Config(object):
    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False
    JSON_SORT_KEYS = False
    CACHE_TYPE = 'redis'
    REDIS_DB_URL = {
        'host': '127.0.0.1',
        'port': 6379,
        'password': '',
        'db': '0'
    }

    # 登录接口
    if (hostname == 'vm-prd-tnauto-occamrazor-185-170.tuniu.org'):
        REST_URL = "https://mall.tuniu.org/api/user/login"
    else:
        REST_URL = "http://mall.tuniu-sit.org/api/user/login"

    @staticmethod  # 此注释可表明使用类名可以直接调用该方法
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@MonLey880124@10.28.32.130/auto_platform?charset=utf8mb4"
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@MonLey880124@10.28.32.130/pandora?charset=utf8mb4"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@MonLey880124@10.28.32.130/pandora?charset=utf8mb4"


config = {
    'default': DevelopmentConfig,  # 默认开发
    'production': ProductionConfig,  # 生产环境配置
    'development': DevelopmentConfig  # 开发环境配置
}
