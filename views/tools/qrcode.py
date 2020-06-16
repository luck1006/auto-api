# -*- coding: utf-8 -*-

from flask import request
import json
from urllib.parse import unquote, quote
from . import tool

# 小程序码生成 https://m.tuniu.com/mzt/createWeappQrCode/sh?clearcache=1



# 用于生成小程序码暂时仅支持h5
@tool.route('/getQrCodeForWeiXin', methods=['GET'])
def getQrCodeForWeiXin():
    query_string = request.query_string.decode('utf-8')
    query_string = unquote(query_string)
    para_dict = json.loads(query_string)
    scene = para_dict['url']
    url = 'https://api.tuniu.com/dany/weixin/miniApp/getQrCodeForWeiXin'
    d = {
        "page": "npm/@tuniu/wepy-component-webview/web",
        "needShortUrl": True,
        "width": 200,
        "scene": scene
    }
    wx_url = url + "?" + 'd=' + quote(json.dumps(d))

    html = f'''
 <!DOCTYPE html>
             <html lang="en">
<head>
    <meta charset="UTF-8">
    <title>小程序码</title>
</head>
    <body>
    <img src= {wx_url} style="width: 200px; height: 200px; display: block;">
    </body>       
    '''
    return html
