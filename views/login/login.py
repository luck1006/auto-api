# -*- coding: utf-8 -*-
# TIME:         下午5:48
# Author:       xutaolin
from flask import Blueprint,request,jsonify,g
import requests
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from app import app
import json

# 设置蓝图
login = Blueprint('login', __name__, url_prefix="")

#生成token接口
def generate_auth_token(info,expiration=7200):
    serializer = Serializer(app.config["SECRET_KEY"], expires_in=expiration)
    token = serializer.dumps(info)
    return token.decode("ascii")

#校验token
def check_auth(token,expiration=7200):
    serializer = Serializer(app.config["SECRET_KEY"], expires_in=expiration)
    try:
        s = serializer.loads(token)
        s['access']=True
    except BadSignature:
        s={"msg":"token is invalid","access":[]}
    except SignatureExpired:
        s={"msg":"token is expired","access":[]}
    return s

#登录接口
@login.route('/login', methods=['POST'])
def pandoraLogin():
    username=request.get_json().get('userName')
    password=request.get_json().get('password')
    data={"username":username,"password":password}
    res=requests.post(app.config["REST_URL"],data=data)
    print(res.json)
    res_new = res.json()
    # print(res_new)
    if(res_new['success']==True):
        token=generate_auth_token(info={"id":res_new['data']['sales'][0]['salerId'],"name":res_new['data']['sales'][0]['name']})
        res_new['data']['token'] = token
    return jsonify(res_new)

#获取用户信息接口(入参为token)
@login.route('/getUserInfo', methods=['GET'])
def getUserInfo():
    token=request.args['token']
    info=check_auth(token=token)
    if(info['access']==True):
        res={"avator":"","name":info["name"],"user_id":info['id'],"access":[info["name"]],"msg":"OK"}
    else:
        res = {"avator": "", "name": "", "user_id":None, "access": [], "msg": info['msg']}
    return jsonify(res)



