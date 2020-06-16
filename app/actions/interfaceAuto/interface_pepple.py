# -*- coding: utf-8 -*-
# TIME:         20191224
# Author:       dff & 参考https://wiki.tuniu.org/pages/viewpage.action?pageId=100239658
import json, requests
# from http import cookiejar
# import urllib, urllib3
from app.actions.interfaceAuto.GetParmsValue import GetParmsValue

pepple_conf = {
    "username": "dongfangfang",
    "password": "eat.art.dff-1220",
    "sit": {
        "pepple_login": "http://public-api.infra.pebble.tuniu-sit.org/pebble-web/sys/login",
        "pepple_provider": "http://public-api.infra.pebble.tuniu-sit.org/pebble-web/service/provider/list",
        "pepple_version": "http://public-api.infra.pebble.tuniu-sit.org/pebble-web/mock/proxy/query",
        "pepple_run": "http://public-api.infra.pebble.tuniu-sit.org/pebble-web/mock/proxy/invoke",
        "pepple_exceute": "http://pebble-mock.api.tuniu-sit.org/pebble-mock-web/proxy/execute", # 暂时未用该接口
        "pepple_method": "http://public-api.infra.pebble.tuniu-sit.org/pebble-web/mock/proxy/methods",
        "pepple_params": "http://public-api.infra.pebble.tuniu-sit.org/pebble-web/mock/proxy/method/params"
    }
}

class InterfacePepple():

    def __init__(self,env='sit', serviceName='', queryMethod='', body=''):
        '''
        :param env: 测试环境，前台界面录入
        :param serviceName: pepple服务名称，前台界面录入
        :param queryMethod: pepple服务查询方法，前台界面录入
        :param body: pepple服务接口入参，前台界面录入
        :return: 完成登录pepple，获取登录后的cookies,并添加到公共headers中，方便下面接口调用
        '''
        self.env = env
        self.serviceName = serviceName
        self.queryMethod = queryMethod
        self.body = body.replace('\n','').replace('\t','')
        self.tmp_params = {"env": self.env}

        formData = {
            "username": pepple_conf["username"],
            "password": pepple_conf["password"]
        }
        req = requests.post(url=pepple_conf[self.env]['pepple_login'], data=formData, headers={})
        cookies = requests.utils.dict_from_cookiejar(req.cookies)   #获取登录后生成的cookies
        #将cookies转成str,以便添加到headers中供下方接口使用
        cookies_str=''
        for i in cookies.items():
            cookies_str = cookies_str + ';' + '='.join(i)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'cookie': cookies_str
        }

    def getPeppleProvider(self):
        params = {"service": self.serviceName,"limit": 10, "page":0}
        print(params)
        # cookies_str = self.peppleLogin()
        req_provider = requests.get(url=pepple_conf[self.env]['pepple_provider'],params=params, headers=self.headers)
        # print("333333---:",req_provider.content)
        try:
            req_provider = json.loads(str(req_provider.content,encoding='utf-8'))
            print("444---:",req_provider)
            ip = req_provider["list"][0]["providerConfig"]["protocolConfig"]["host"]
            port = req_provider["list"][0]["providerConfig"]["protocolConfig"]["port"]
            address = str(ip) + ":" + str(port)
            name = req_provider["list"][0]["applicationConfig"]["name"]
            pepple_sys = name.split(":")[0]
            pepple_mod = name.split(":")[1]
            self.tmp_params["sys"] = pepple_sys
            self.tmp_params["mod"] = pepple_mod
            self.tmp_params["address"] = address
        except Exception as e:
            print('服务提供者信息获取异常，异常信息如下：\n%s'%str(e))
        return self.tmp_params

    def getPeppleVersion(self):
        self.tmp_params = self.getPeppleProvider()
        params = {"service": self.serviceName, "sys": self.tmp_params["sys"], "mod": self.tmp_params["mod"],"page":1,"limit":10}
        req_Version = requests.get(url=pepple_conf[self.env]["pepple_version"], params=params,headers=self.headers)
        try:
            req_Version = json.loads(str(req_Version.content, encoding='utf-8'))
            self.tmp_params["version"] = req_Version["list"][0]["versions"][-1]
        except Exception as e:
            print('获取服务的版本信息出错，异常信息如下：\n%s'%str(e))
        # print(self.tmp_params)
        return self.tmp_params

    def getPeppleMethod(self):
        params = self.getPeppleVersion()
        get_params = {
            "service": self.serviceName,
            "sys": params["sys"],
            "mod": params["mod"],
            "version": params["version"],
            "page": 1,
            "limit": 10
        }

        response = requests.get(url=pepple_conf[self.env]["pepple_method"],params=get_params,headers=self.headers)
        try:
            response = json.loads(str(response.content, encoding='utf-8'))
        except Exception as e:
            print('获取查询方法失败，异常信息为：\n%s'%str(e))
            response = None
        # print("query-methods: ",str(response.content, encoding='utf-8'))
        # print(type(json.loads(str(response.content, encoding='utf-8'))))
        return response

    def getPeppleParams(self,method):
        params = self.getPeppleVersion()
        get_params = {
            "service": self.serviceName,
            "sys": params["sys"],
            "mod": params["mod"],
            "version": params["version"],
            "method":method
        }
        print('获取params 请求的参数：',get_params)
        response = requests.get(url=pepple_conf[self.env]["pepple_params"], params=get_params,headers=self.headers)
        try:
            response = json.loads(eval(str(response.content, encoding='utf-8')))
        except Exception as e:
            print('获取请求入参失败，异常信息为：\n%s'%str(e))
            response = None
        # print("method-params : ",eval(str(response.content, encoding='utf-8')))
        # print(type(json.loads(eval(str(response.content, encoding='utf-8')))))
        return response

    def peppleRun(self):
        params = self.getPeppleVersion()
        params["serviceName"] = self.serviceName
        params["method"] = self.queryMethod
        params["env"] = self.env
        #增加入参参数化处理
        if self.body not in ('',None):
            self.body = GetParmsValue().get_parms_value(self.body,self.env)
        params["body"] = self.body

        print(params,'\n',type(params))
        self.headers["pebble-service"] = str(self.serviceName)
        self.headers["Content-Type"] = 'application/json'
        response = requests.post(url=pepple_conf[self.env]["pepple_run"], data=json.dumps(params), headers=self.headers)
        # response = requests.post(url=pepple_conf[self.env]["pepple_exceute"],data=json.dumps(params),headers={'Content-Type':'application/json'})
        # print("pepple-resonse: ",json.loads(str(response.content, encoding='utf-8')))
        # print(type(json.loads(str(response.content, encoding='utf-8'))))
        if response.status_code == 200:
            try:
                z = json.loads(str(response.content, encoding='utf-8'))
                z = {"success": True, "data": z}
            except Exception as e:
                z = {"success": False,'data':'%s'%str(e)}
        else:
            z = {"success": False,'data':'接口请求失败，响应状态码为%s'%str(response.status_code)}
        print("pepple-resonse: ",z)
        return z

    def peppleBatchRun(self):
        params = self.getPeppleVersion()
        params["serviceName"] = self.serviceName
        params["method"] = self.queryMethod
        params["env"] = self.env
        #增加入参参数化批量处理
        body_list = []
        response_list = []
        self.headers["pebble-service"] = str(self.serviceName)
        self.headers["Content-Type"] = 'application/json'
        # print('the self.body is : ',self.body)
        if self.body not in ('',None):
            body_first,body_params_list = GetParmsValue().get_params_values_list(self.body,self.env)
            if body_params_list not in ('',[],{},None):
                body_list = GetParmsValue().set_params_list(self.body,body_params_list)
        # print('the body list is : ',body_params_list,'\n', self.body, '\n', body_list)
        if len(body_list)>0:
            for body_item in body_list:
                params["body"] = body_item
                print(params,'\n',type(params))
                time = 0
                response = {}
                try:
                    r = requests.post(url=pepple_conf[self.env]["pepple_run"], data=json.dumps(params), headers=self.headers)
                    #接口运行时间
                    time = r.elapsed.microseconds/1000
                    try:
                        r = json.loads(r.content)
                        z = json.dumps(r, ensure_ascii=False)
                        success = True
                    except:
                        z,success= r.status_code,False  if r.status_code !=200 else r.text
                    response['res']=z
                    response['success'] = success
                except Exception as e:
                    response['res'] = str(e)
                    response['success'] = False
                response['time']=time
                response['url'] = self.serviceName
                response['data'] = body_item.encode('utf-8')
                response_list.append(response)
        else:
            params['body'] = body_first
            time = 0
            response = {}
            try:
                r = requests.post(url=pepple_conf[self.env]["pepple_run"], data=json.dumps(params), headers=self.headers)
                #接口运行时间
                time = r.elapsed.microseconds/1000
                try:
                    r = json.loads(r.content)
                    z = json.dumps(r, ensure_ascii=False)
                    success = True
                except:
                    z,success= r.status_code,False  if r.status_code !=200 else r.text
                response['res']=z
                response['success'] = success
            except Exception as e:
                response['res'] = str(e)
                response['success'] = False
            response['time']=time
            response['url'] = self.serviceName
            response['data'] = self.body.encode('utf-8')
            response_list.append(response)
        print("pepple-response_list: ",response_list)
        return response_list

if __name__ == '__main__':
    serviceName='com.tuniu.fab.spi.service.CustSerachService'
    # serviceName='com.tuniu.mauritius.confirmation.occupyrecord.model.NbOccupyCommonService'
    queryMethod="queryByKey"
    # queryMethod="queryOccupyRecord"
    body='{"requestVO":{"subSystem":"mob","key":0,"searchKey":13062527068}}'
    # body='{"requestVO":{"requirementId": 350038396}}'
    aa = InterfacePepple(env='sit',serviceName=serviceName,queryMethod=queryMethod,body=body)
    # aa = InterfacePepple('sit',serviceName,queryMethod,body)
    # aa.peppleRun()
    # aa.getPeppleMethod()
    aa.getPeppleParams("queryByKey")

    # bb = InterfacePepple(serviceName=serviceName)
    # bb.getPeppleMethod()
