# -*- coding:UTF-8 -*-
import sys
import os
import requests
import json

sys.path.append(os.path.dirname(__file__) + os.sep + '..'+ os.sep ) ## “ '..'+ os.sep ” => 向上一层
## os.path.dirname(__file__) 上一级目录
from app.actions.tools import BaseApplication

s = requests.session()
class interface_pebble(BaseApplication.BaseApplication):
    def _getPebbleLogin(self):
        keywords = {'username': 'wangdan8', 'password': '@tuniu0422'}
        headersx = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}
        login = s.post("http://10.10.30.97:13043/pebble-web/sys/login", data=keywords, headers=headersx)
        return login

    def _pebble1(self,system,module,serviceName,method,version,env,body,address,pebblecookies):
    #def _pebble1():
        paramss = {"sys":"FAB","mod":"SPI","serviceName":"com.tuniu.fab.spi.service.CustSerachService","method":"queryById","version":"1.1.19","env":"SIT","body":"{\"requestVO\":{\"custId\":1,\"subSystem\":1,\"key\":1}}","address":"10.30.157.148:24993"}
        print (paramss)
        paramss['sys']=system
        paramss['mod']=module
        paramss['serviceName'] = serviceName
        paramss['method'] = method
        paramss['version'] = version
        paramss['env'] = env
        paramss['body'] = body
        paramss['address'] = address

        self.pyprint(paramss,1)
        headers = {'content-type': 'application/json'}
        aaa = s.post("http://10.10.30.97:13043/pebble-web/mock/proxy/invoke", data=json.dumps(paramss).decode("utf-8"),
                     cookies=pebblecookies, headers=headers)
        #print aaa.status_code

        self.pyprint(aaa.text,1)
        return aaa

    def _pebble(self,system,module,serviceName,method,version,env,body):
        paramss = {"sys": "FAB", "mod": "SPI", "serviceName": "com.tuniu.fab.spi.service.CustSerachService",
                   "method": "queryById", "version": "1.1.19", "env": "SIT",
                   "body": "{\"requestVO\":{\"custId\":1,\"subSystem\":1,\"key\":1}}", "address": "10.30.157.148:24993"}


        #CommonKeyword.pyprint(paramss, 1)
        paramss['sys'] = system
        paramss['mod'] = module
        paramss['serviceName'] = serviceName
        paramss['method'] = method
        paramss['version'] = version
        paramss['env'] = env
        paramss['body'] = body
        # paramss['address'] = address

        headers = {'content-type': 'application/json'}
        aaa=self.pebblePost("http://10.10.35.211:8080/dgw/proxy/execute",paramss,headers=headers)
        # aaa=self.pebblePost("http://172.31.36.74:8080/dgw/proxy/execute",paramss,headers=headers)
        #aaa=self.pebblePost("http://172.31.3.49:8080/pebble-mock-web/proxy/execute",paramss,headers=headers)
        # aaa=self.pebblePost("http://pebble-mock.api.tuniu-sst.org/pebble-mock-web/proxy/execute",paramss,headers=headers)

        return aaa

system = "FAB" #系统码
module ="SPI" #模块码
env = "CIE"  # 测试环境类型 SST/SIT/PRE/PRD
# FABSPI = "10.30.159.24:21321"  # 被测应用地址
#env = "SIT"  # 测试环境类型 SST/SIT/PRE/PRD
#FABSPI = "10.30.157.148:24993"  # 被测应用地址
serviceName = "com.tuniu.fab.spi.service.CustSerachService" #被测试pebble服务名
method = "queryById" #被测试服务的方法
version = "1.1.13"  # 被测服务pebble版本
body = "{\"requestVO\":{\"custId\":1,\"subSystem\":1,\"key\":1}}" #接口入参
#print json.loads(_pebble(system, module, serviceName, method, version, env, body, FABSPI).text)['scost']
#interface_pebble()._pebble(system, module, serviceName, method, version, env, body, FABSPI)
