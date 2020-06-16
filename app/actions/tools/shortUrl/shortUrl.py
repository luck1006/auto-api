# -*- coding: utf-8 -*-

import requests
import json


def short_url(url, tag=''):
    shorturl = 'http://devops-shorturl.api.tuniu.org/api/shorten'
    payload = {"url": url, "creator": tag}
    headers = {'Content-Type': "application/json"}
    try:
        r = requests.post(shorturl, json=payload, headers=headers)
        return json.loads(r.text)['data']['shortUrl']
    except Exception as e:
        print(e)
        return url
