# -*- coding: utf-8 -*-
# Author:       liujingzu
# Explain：     文件下载

from app.models.models import *
from flask import Blueprint,current_app
from flask import make_response,send_from_directory,abort,request,jsonify,Flask,send_file
import os,json
import requests
from sys import stdout
import mimetypes
#解决跨域问题
from flask import Flask, session
from flask_cors import CORS
# 设置蓝图
penetration = Blueprint('PenetrationTest', __name__)

cors = CORS(penetration, resources={r"/.*": {"origins": "http://pandora.tuniu.org"}})   # 只允许特定域名跨域
# cors = CORS(penetration, resources={r"/.*": {"origins": "http://localhost:8081"}})   # 只允许特定域名跨域

@penetration.route('/penetration/download/doc', methods=['GET'])
# 直接返回一个response对象,注意前端解析返回类型
def doc_download_file():
    filename = "BurpSuit_Pro_Crack.docx"
    # directory = "C:\\Users\\liujingzu\\Desktop"
    # directory = os.getcwd()  # 假设在当前目录
    directory = '/opt/tuniu/software'
    try :
        response = make_response(send_from_directory(directory, filename, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
        return response
    except Exception as e:
        raise e


@penetration.route('/penetration/download/pdf', methods=['GET'])
# 直接返回一个response对象,注意前端解析返回类型
def pdf_download_file():
    filename = "burpsuite_guide.pdf"
    # directory = "C:\\Users\\liujingzu\\Desktop"
    # directory = os.getcwd()  # 假设在当前目录
    directory = '/opt/tuniu/software'
    try :
        response = make_response(send_from_directory(directory, filename, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
        return response
    except Exception as e:
        raise e

@penetration.route('/penetration/download/zip', methods=['GET'])
# 直接返回一个response对象
def zip_download_file():
    filename = "Burp_Suite_Pro_v1.7.37.zip"
    # directory = "C:\\Users\\liujingzu\\Desktop"
    # directory = os.getcwd()  # 假设在当前目录
    directory = '/opt/tuniu/software'
    try :
        response = make_response(send_from_directory(directory, filename, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
        return response
    except Exception as e:
        raise e

