# -*- coding:utf-8 -*-

import requests
import json
from urllib3 import encode_multipart_formdata


def excel_url(filepath):
    '''
    文件转成外网链接
    '''
    url = "http://public-api.nj.pla.tuniu.org/filebroker/upload?folder=cdn"
    excel_url = ''
    data = {}
    header = {}
    data['file'] = (filepath, open(filepath, 'rb').read())
    encode_data = encode_multipart_formdata(data)
    data = encode_data[0]
    header['Content-Type'] = encode_data[1]
    r = requests.post(url, headers=header, data=data)
    res = json.loads(r.text)
    #print('res==',res)
    for l in res['data']:
        if 'm.tuniucdn.com' in l['url']:
            excel_url = l['url']
    return excel_url

