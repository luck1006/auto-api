# -*- coding: utf-8 -*-
# TIME:         20190701
# Author:       dff
from app.actions.interfaceAuto.GetParmsValue import GetParmsValue
from collections import OrderedDict
import ast
from urllib import parse
from app.actions.interfaceAuto.interface_tsp import *
import requests
requests.adapters.DEFAULT_RETRIES = 10
s = requests.session()
s.keep_alive = False


class Parameter_Interface:

    def getinterfaceone(self, rest, data, env, headers, dParam='', isBase64Encode=False, isBase64Decode=False):
        response_list = []
        getparmsvalue = GetParmsValue()
        # rest = getparmsvalue.get_parms_value(rest, env)
        new_rest, params_list = getparmsvalue.get_params_values_list(rest, env)   # new_rest得到第1次参数化后的请求rest
        rest_list = []
        if params_list != {}:
            rest_list = getparmsvalue.set_params_list(rest, params_list)  #得到rest参数化后的列表
            print("rest_list:", rest_list)
        success=True

        #dff: 20190704 对d参数进行处理
        param = {}
        d_list = []   #存放rest与d参数合并后的请求url列表,或d_list为[],后面请求只需根据url调接口即可，否则直接使用d_list做为url调接口（因为已将上面url合并在一起了）
        if dParam is not None and dParam != '':
            # dParam = getparmsvalue.get_parms_value(dParam, env)
            new_dParam, params_list = getparmsvalue.get_params_values_list(dParam,env)
            if params_list != {}:  # d需要参数化
                dParam_list = getparmsvalue.set_params_list(dParam,params_list)  #a获取到d参数化后的请求列表
                if rest_list != []:   #当url中也有参数化存在时，与d循环组合在一起
                    for rest_item in rest_list:
                        for d_item in dParam_list:
                            param['d'] = d_item
                            # dff: 20190701 将请求d参数编码
                            encodeParam = parse.urlencode(param)
                            # rest = rest +'&'+ encodeParam
                            d_list.append(rest_item+'&'+encodeParam)
                    print('111--dparam_list:', d_list)
                else:  # 当rest_list==[]时，url无参数化，只需针对d参数列表循环处理
                    for d_item in dParam_list:
                        param['d'] = d_item
                        encodeParam = parse.urlencode(param)
                        d_list.append(new_rest+'&'+encodeParam)
                    print('222--dparam_list:', d_list)
            else:   # d 不需要参数化
                param['d'] = new_dParam
                encodeParam = parse.urlencode(param)
                if rest_list !=[]:   # 上面的url需要参数化
                    for rest_item in rest_list:
                        d_list.append(rest_item+'&'+encodeParam)
                    print('333--dparam_list:',d_list)
                else: # 上面的url 不需要参数化
                    new_rest = new_rest + '&' + encodeParam

        try:
            if (data != '' and data != None):
                if (headers != ''):
                    if ('{{' in headers):
                        headers = getparmsvalue.get_parms_value(headers, env)
                    headers = eval(headers)
                # data = getparmsvalue.get_parms_value(data, env)
                new_data, params_list = getparmsvalue.get_params_values_list(data, env)
                #20190816-dff: 兼容未使用参数且需base64编码处理时，也需要对new_data处理
                if isBase64Encode:
                    new_data = base64Encode(new_data)
                if params_list != {}:  #  data 需要参数化
                    data_list = getparmsvalue.set_params_list(data, params_list)
                    print("data_list:", data_list)
                    ###20190727-dff: 对入参需要base64编码进行单独处理
                    if isBase64Encode:
                        data_list_tmp = []
                        for item in data_list:
                            data_list_tmp.append(base64Encode(item))
                        data_list = data_list_tmp
                    ######------------dff 20190727 以上 ------------####
                    #循环执行参数化后的data入参
                    if d_list !=[]:
                        for url_item in d_list:
                            for data_item in data_list:
                                time=0
                                response = {}
                                try:
                                    r = requests.get(url_item, headers=headers, params=data_item)
                                    #接口运行时间
                                    time = r.elapsed.microseconds/1000
                                    try:
                                        r = json.loads(r.text, object_pairs_hook=OrderedDict);
                                        z = json.dumps(r, ensure_ascii=False)
                                    except:
                                        z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                                    # dff - 20191012 增加对出参是否需base64解码的判断处理
                                    if isBase64Decode:
                                        z = base64Decode(z)
                                    response['res']=z
                                    response['success'] = success
                                except Exception as e:
                                    response['res'] = e
                                    response['success'] = False
                                response['time']=time
                                response['url'] = url_item
                                response['data'] = data_item.encode('utf-8')
                                response_list.append(response)

                    elif rest_list != [] and d_list == []:
                        for url_item in rest_list:
                            for data_item in data_list:
                                time = 0
                                response = {}
                                try:
                                    r = requests.get(url_item, headers=headers, params=data_item)
                                    # 接口运行时间
                                    time = r.elapsed.microseconds / 1000
                                    try:
                                        r = json.loads(r.text, object_pairs_hook=OrderedDict);
                                        z = json.dumps(r, ensure_ascii=False)
                                    except:
                                        z = r.text
                                    # dff - 20191012 增加对出参是否需base64解码的判断处理
                                    if isBase64Decode:
                                        z = base64Decode(z)
                                    response['res'] = z
                                    response['success'] = success
                                except Exception as e:
                                    response['res'] = e
                                    response['success'] = False
                                response['time'] = time
                                response['url'] = url_item
                                response['data'] = data_item.encode('utf-8')
                                response_list.append(response)
                    else:
                        for data_item in data_list:
                                time=0
                                response={}
                                try:
                                    r = requests.get(new_rest, headers=headers, params=data_item)
                                    #接口运行时间
                                    time = r.elapsed.microseconds/1000
                                    try:
                                        r = json.loads(r.text, object_pairs_hook=OrderedDict);
                                        z = json.dumps(r, ensure_ascii=False)
                                    except:
                                        z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                                    # dff - 20191012 增加对出参是否需base64解码的判断处理
                                    if isBase64Decode:
                                        z = base64Decode(z)
                                    response['res'] = z
                                    response['success'] = success
                                except Exception as e:
                                    response['res'] = e
                                    response['success'] = False
                                response['time']=time
                                response['url'] = new_rest
                                response['data'] = data_item.encode('utf-8')
                                response_list.append(response)
                else: #data 无需参数化
                    if d_list != []:
                        for url_item in d_list:
                            time = 0
                            response = {}
                            try:
                                r = requests.get(url_item, headers=headers, params=new_data)
                                    #接口运行时间
                                time = r.elapsed.microseconds/1000
                                try:
                                    r = json.loads(r.text, object_pairs_hook=OrderedDict);
                                    z = json.dumps(r, ensure_ascii=False)
                                except:
                                    z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                                # dff - 20191012 增加对出参是否需base64解码的判断处理
                                if isBase64Decode:
                                    z = base64Decode(z)
                                response['res'] = z
                                response['success'] = success
                            except Exception as e:
                                response['res'] = e
                                response['success'] = False
                            response['time']=time
                            response['url'] = url_item
                            response['data'] = new_data.encode('utf-8')
                            response_list.append(response)

                    elif rest_list != [] and d_list == []:
                        for url_item in rest_list:
                            time = 0
                            response = {}
                            try:
                                r = requests.get(url_item, headers=headers, params=new_data)
                                    #接口运行时间
                                time = r.elapsed.microseconds/1000
                                try:
                                    r = json.loads(r.text, object_pairs_hook=OrderedDict);
                                    z = json.dumps(r, ensure_ascii=False)
                                except:
                                    z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                                # dff - 20191012 增加对出参是否需base64解码的判断处理
                                if isBase64Decode:
                                    z = base64Decode(z)
                                response['res'] = z
                                response['success'] = success
                            except Exception as e:
                                response['res'] = e
                                response['success'] = False
                            response['time']=time
                            response['url'] = url_item
                            response['data'] = new_data.encode('utf-8')
                            response_list.append(response)
                    else:
                        time = 0
                        response = {}
                        try:
                            r = requests.get(new_rest, headers=headers, params=new_data)
                                    #接口运行时间
                            time = r.elapsed.microseconds/1000
                            try:
                                r = json.loads(r.text, object_pairs_hook=OrderedDict);
                                z = json.dumps(r, ensure_ascii=False)
                            except:
                                z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                            # dff - 20191012 增加对出参是否需base64解码的判断处理
                            if isBase64Decode:
                                z = base64Decode(z)
                            response['res'] = z
                            response['success'] = success
                        except Exception as e:
                            response['res'] = e
                            response['success'] = False
                        response['time']=time
                        response['url'] = new_rest
                        response['data'] = new_data.encode('utf-8')
                        response_list.append(response)
            else:  # 当未传递data
                if (headers != ''):
                    headers = eval(headers)
                if d_list != []:  # 不为空时，代表d参数有参数化，则循环请求
                    for rest_item in d_list:
                        time = 0
                        response = {}
                        try:
                            r = requests.get(rest_item, headers=headers)
                            # 接口运行时间
                            time = r.elapsed.microseconds/1000
                            try:
                                r = json.loads(r.text, object_pairs_hook=OrderedDict)
                                z = json.dumps(r, ensure_ascii=False)
                            except:
                                z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                            # dff - 20191012 增加对出参是否需base64解码的判断处理
                            if isBase64Decode:
                                z = base64Decode(z)
                            response['res'] = z
                            response['success'] = success
                        except Exception as e:
                            response['res'] = e
                            response['success'] = False
                        response['time']=time
                        response['url'] = rest_item
                        response['data'] = ''
                        response_list.append(response)

                elif rest_list != [] and d_list == []:
                    for rest_item in rest_list:
                        time = 0
                        response = {}
                        try:
                            r = requests.get(rest_item, headers=headers)
                            # 接口运行时间
                            time = r.elapsed.microseconds/1000
                            try:
                                r = json.loads(r.text, object_pairs_hook=OrderedDict)
                                z = json.dumps(r, ensure_ascii=False)
                            except:
                                z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                            # dff - 20191012 增加对出参是否需base64解码的判断处理
                            if isBase64Decode:
                                z = base64Decode(z)
                            response['res'] = z
                            response['success'] = success
                        except Exception as e:
                            response['res'] = e
                            response['success'] = False

                        response['time']=time
                        response['url'] = rest_item
                        response['data'] = ''
                        response_list.append(response)
                else:
                    time = 0
                    response = {}
                    try:
                        r = requests.get(new_rest, headers=headers)
                        # 接口运行时间
                        time = r.elapsed.microseconds/1000
                        try:
                            r = json.loads(r.text, object_pairs_hook=OrderedDict)
                            z = json.dumps(r, ensure_ascii=False)
                        except:
                            z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                            # success=True if r.status_code ==200 else False
                        # dff - 20191012 增加对出参是否需base64解码的判断处理
                        if isBase64Decode:
                            z = base64Decode(z)
                        response['res'] = z
                        response['success'] = success
                    except Exception as e:
                        response['res'] = e
                        response['success'] = False
                    response['time']=time
                    response['url'] = new_rest
                    response['data'] = ''
                    response_list.append(response)

        except Exception as e:
            print(e)
            z = '调用的get 请求方法异常'
            time=0
        #返回dict（接口返回值以及接口运行时间）
            response={}
            response['res']=z
            response['time']=time
            response['success']=False
            response_list.append(response)
        return response_list

    def postinterfaceone(self, rest, data, env, headers, dParam='', isBase64Encode=False, isBase64Decode=False):
        getparmsvalue = GetParmsValue()
        response_list = []
        # rest = getparmsvalue.get_parms_value(rest, env)
        new_rest, params_list = getparmsvalue.get_params_values_list(rest, env)   # new_rest得到第1次参数化后的请求rest
        rest_list = []
        if params_list != {}:
            rest_list = getparmsvalue.set_params_list(rest, params_list)  #得到rest参数化后的列表
            print("rest_list:", rest_list)
        success=True

        #dff: 20190704 对d参数进行处理
        param = {}
        d_list = []   #存放rest与d参数合并后的请求url列表,或d_list为[],后面请求只需根据url调接口即可，否则直接使用d_list做为url调接口（因为已将上面url合并在一起了）
        if dParam is not None and dParam != '':
            # dParam = getparmsvalue.get_parms_value(dParam, env)
            new_dParam, params_list = getparmsvalue.get_params_values_list(dParam,env)
            if params_list != {}:  # d需要参数化
                dParam_list = getparmsvalue.set_params_list(dParam,params_list)  #a获取到d参数化后的请求列表
                if rest_list != []:   #当url中也有参数化存在时，与d循环组合在一起
                    for rest_item in rest_list:
                        for d_item in dParam_list:
                            param['d'] = d_item
                            # dff: 20190701 将请求d参数编码
                            encodeParam = parse.urlencode(param)
                            # rest = rest +'&'+ encodeParam
                            d_list.append(rest_item+'&'+encodeParam)
                    print('111--dparam_list:', d_list)
                else:  # 当rest_list==[]时，url无参数化，只需针对d参数列表循环处理
                    for d_item in dParam_list:
                        param['d'] = d_item
                        encodeParam = parse.urlencode(param)
                        d_list.append(new_rest+'&'+encodeParam)
                    print('222--dparam_list:', d_list)
            else:   # d 不需要参数化
                param['d'] = new_dParam
                encodeParam = parse.urlencode(param)
                if rest_list !=[]:   # 上面的url需要参数化
                    for rest_item in rest_list:
                        d_list.append(rest_item+'&'+encodeParam)
                    print('333--dparam_list:',d_list)
                else: # 上面的url 不需要参数化
                    new_rest = new_rest + '&' + encodeParam

        try:
            if (data != '' and data != None):
                # data = getparmsvalue.get_parms_value(data, env)
                if (headers != ''):
                    if ('{{' in headers):
                        headers = getparmsvalue.get_parms_value(headers, env)
                    headers = ast.literal_eval(headers)

                new_data, params_list = getparmsvalue.get_params_values_list(data, env)
                #20190816-dff: 兼容未使用参数且需base64编码处理时，也需要对new_data处理
                if isBase64Encode:
                    new_data = base64Encode(new_data)
                if params_list != {}:  #  data 需要参数化
                    data_list = getparmsvalue.set_params_list(data, params_list)
                    print("data_list:", data_list)
                    ## 20190727 dff: 增加对入参base64编码单独处理
                    if isBase64Encode:
                        data_list_tmp = []
                        for item in data_list:
                            data_list_tmp.append(base64Encode(item))
                        data_list = data_list_tmp
                    ####----------dff 20190727 以上 -----------####
                    #循环执行参数化后的data入参
                    if d_list !=[]:
                        for url_item in d_list:
                            for data_item in data_list:
                                time = 0
                                response = {}
                                try:
                                    r = requests.post(url_item, data=data_item.encode('utf-8'), headers=headers)
                                    #接口运行时间
                                    time = r.elapsed.microseconds/1000
                                    try:
                                        r = json.loads(r.text, object_pairs_hook=OrderedDict);
                                        z = json.dumps(r, ensure_ascii=False)
                                    except:
                                        z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                                    # dff - 20191012 增加对出参是否需base64解码的判断处理
                                    if isBase64Decode:
                                        z = base64Decode(z)
                                    response['res'] = z
                                    response['success'] = success
                                except Exception as e:
                                    response['res'] = e
                                    response['success'] = False
                                response['time']=time
                                response['url'] = url_item
                                response['data'] = data_item
                                response_list.append(response)
                    elif rest_list != [] and d_list == []:
                        for url_item in rest_list:
                            for data_item in data_list:
                                time = 0
                                response = {}
                                try:
                                    r = requests.post(url_item, data=data_item.encode('utf-8'), headers=headers)
                                    #接口运行时间
                                    time = r.elapsed.microseconds/1000
                                    try:
                                        r = json.loads(r.text, object_pairs_hook=OrderedDict);
                                        z = json.dumps(r, ensure_ascii=False)
                                    except:
                                        z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                                    # dff - 20191012 增加对出参是否需base64解码的判断处理
                                    if isBase64Decode:
                                        z = base64Decode(z)
                                    response['res'] = z
                                    response['success'] = success
                                except Exception as e:
                                    response['res'] = e
                                    response['success'] = False
                                response['time']=time
                                response['url'] = url_item
                                response['data'] = data_item
                                response_list.append(response)
                    else:
                        for data_item in data_list:
                                time = 0
                                response = {}
                                try:
                                    r = requests.post(new_rest, data=data_item.encode('utf-8'), headers=headers)
                                    #接口运行时间
                                    time = r.elapsed.microseconds/1000
                                    try:
                                        r = json.loads(r.text, object_pairs_hook=OrderedDict);
                                        z = json.dumps(r, ensure_ascii=False)
                                    except:
                                        z,success= (r.status_code,False) if r.status_code !=200 else (r.text,success)
                                    # dff - 20191012 增加对出参是否需base64解码的判断处理
                                    if isBase64Decode:
                                        z = base64Decode(z)
                                    response['res'] = z
                                    response['success'] = success
                                except Exception as e:
                                    response['res'] = e
                                    response['success'] = False
                                response['time']=time
                                response['url'] = new_rest
                                response['data'] = data_item
                                response_list.append(response)

                else: #data 无需参数化
                    if d_list != []:
                        for url_item in d_list:
                            time = 0
                            response = {}
                            try:
                                r = requests.post(url_item,data = new_data.encode('utf-8'), headers=headers)
                                    #接口运行时间
                                time = r.elapsed.microseconds/1000
                                try:
                                    r = json.loads(r.text, object_pairs_hook=OrderedDict);
                                    z = json.dumps(r, ensure_ascii=False)
                                except:
                                    z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                                # dff - 20191012 增加对出参是否需base64解码的判断处理
                                if isBase64Decode:
                                    z = base64Decode(z)
                                response['res'] = z
                                response['success'] = success
                            except Exception as e:
                                response['res'] = e
                                response['success'] = False
                            response['time']=time
                            response['url'] = url_item
                            # response['data'] = new_data.encode('utf-8')
                            response['data'] = new_data
                            response_list.append(response)
                    elif rest_list != [] and d_list == []:
                        for url_item in rest_list:
                            time = 0
                            response = {}
                            try:
                                r = requests.post(url_item,data=new_data.encode('utf-8'), headers=headers)
                                    #接口运行时间
                                time = r.elapsed.microseconds/1000
                                try:
                                    r = json.loads(r.text, object_pairs_hook=OrderedDict);
                                    z = json.dumps(r, ensure_ascii=False)
                                except:
                                    z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                                # dff - 20191012 增加对出参是否需base64解码的判断处理
                                if isBase64Decode:
                                    z = base64Decode(z)
                                response['res'] = z
                                response['success'] = success
                            except Exception as e:
                                response['res'] = e
                                response['success'] = False
                            response['time']=time
                            response['url'] = url_item
                            # response['data'] = new_data.encode('utf-8')
                            response['data'] = new_data
                            response_list.append(response)
                    else:
                        time = 0
                        response = {}
                        try:
                            r = requests.post(new_rest, data=new_data.encode('utf-8'),headers=headers)
                                    #接口运行时间
                            time = r.elapsed.microseconds/1000
                            try:
                                r = json.loads(r.text, object_pairs_hook=OrderedDict);
                                z = json.dumps(r, ensure_ascii=False)
                            except:
                                z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                            # dff - 20191012 增加对出参是否需base64解码的判断处理
                            if isBase64Decode:
                                z = base64Decode(z)
                            response['res'] = z
                            response['success'] = success
                        except Exception as e:
                            response['res'] = e
                            response['success'] = False

                        response['time']=time
                        response['url'] = new_rest
                        # response['data'] = new_data.encode('utf-8')
                        response['data'] = new_data
                        response_list.append(response)
            else:  # 当未传递data  , 其实对于post 请求来说，这种情况应该不存在
                if (headers != ''):
                    headers = eval(headers)
                if d_list != []:  # 不为空时，代表d参数有参数化，则循环请求
                    for rest_item in d_list:
                        time = 0
                        response = {}
                        try:
                            r = requests.post(rest_item, headers=headers)
                            # 接口运行时间
                            time = r.elapsed.microseconds/1000
                            try:

                                r = json.loads(r.text, object_pairs_hook=OrderedDict)
                                z = json.dumps(r, ensure_ascii=False)
                            except:
                                z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                            # dff - 20191012 增加对出参是否需base64解码的判断处理
                            if isBase64Decode:
                                z = base64Decode(z)
                            response['res'] = z
                            response['success'] = success
                        except Exception as e:
                            response['res'] = e
                            response['success'] = False
                        response['time']=time
                        response['url'] = rest_item
                        response['data'] = ''
                        response_list.append(response)

                elif rest_list != [] and d_list == []:
                    for rest_item in rest_list:
                        time = 0
                        response = {}
                        try:
                            r = requests.post(rest_item, headers=headers)
                            # 接口运行时间
                            time = r.elapsed.microseconds/1000
                            try:
                                r = json.loads(r.text, object_pairs_hook=OrderedDict)
                                z = json.dumps(r, ensure_ascii=False)
                            except:
                                z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                            # dff - 20191012 增加对出参是否需base64解码的判断处理
                            if isBase64Decode:
                                z = base64Decode(z)
                            response['res'] = z
                            response['success'] = success
                        except Exception as e:
                            response['res'] = e
                            response['success'] = False

                        response['time']=time
                        response['url'] = rest_item
                        response['data'] = ''
                        response_list.append(response)
                else:
                    time = 0
                    response = {}
                    try:
                        r = requests.post(new_rest, headers=headers)
                        # 接口运行时间
                        time = r.elapsed.microseconds/1000
                        try:
                            r = json.loads(r.text, object_pairs_hook=OrderedDict)
                            z = json.dumps(r, ensure_ascii=False)
                        except:
                            z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                        # dff - 20191012 增加对出参是否需base64解码的判断处理
                        if isBase64Decode:
                            z = base64Decode(z)
                        response['res'] = z
                        response['success'] = success
                    except Exception as e:
                        response['res'] = e
                        response['success'] = False
                    response['time']=time
                    response['url'] = new_rest
                    response['data'] = ''
                    response_list.append(response)
        except Exception as e:
            print(e)
            z='调用的post 请求方法异常'
            time=0
        # 返回dict（接口返回值以及接口运行时间）
            response = {}
            response['res'] = z
            response['time'] = time
            response['success'] = False
            response_list.append(response)
        return response_list

    def putinterfaceone(self, rest, data, env, headers, dParam='', isBase64Encode=False, isBase64Decode=False):
        getparmsvalue = GetParmsValue()
        response_list = []
        # rest = getparmsvalue.get_parms_value(rest, env)
        new_rest, params_list = getparmsvalue.get_params_values_list(rest, env)   # new_rest得到第1次参数化后的请求rest
        rest_list = []
        if params_list != {}:
            rest_list = getparmsvalue.set_params_list(rest, params_list)  #得到rest参数化后的列表
            print("rest_list:", rest_list)
        success=True

        #dff: 20190704 对d参数进行处理
        param = {}
        d_list = []   #存放rest与d参数合并后的请求url列表,或d_list为[],后面请求只需根据url调接口即可，否则直接使用d_list做为url调接口（因为已将上面url合并在一起了）
        if dParam is not None and dParam != '':
            # dParam = getparmsvalue.get_parms_value(dParam, env)
            new_dParam, params_list = getparmsvalue.get_params_values_list(dParam,env)
            if params_list != {}:  # d需要参数化
                dParam_list = getparmsvalue.set_params_list(dParam,params_list)  #a获取到d参数化后的请求列表
                if rest_list != []:   #当url中也有参数化存在时，与d循环组合在一起
                    for rest_item in rest_list:
                        for d_item in dParam_list:
                            param['d'] = d_item
                            # dff: 20190701 将请求d参数编码
                            encodeParam = parse.urlencode(param)
                            # rest = rest +'&'+ encodeParam
                            d_list.append(rest_item+'&'+encodeParam)
                    print('111--dparam_list:', d_list)
                else:  # 当rest_list==[]时，url无参数化，只需针对d参数列表循环处理
                    for d_item in dParam_list:
                        param['d'] = d_item
                        encodeParam = parse.urlencode(param)
                        d_list.append(new_rest+'&'+encodeParam)
                    print('222--dparam_list:', d_list)
            else:   # d 不需要参数化
                param['d'] = new_dParam
                encodeParam = parse.urlencode(param)
                if rest_list !=[]:   # 上面的url需要参数化
                    for rest_item in rest_list:
                        d_list.append(rest_item+'&'+encodeParam)
                    print('333--dparam_list:',d_list)
                else: # 上面的url 不需要参数化
                    new_rest = new_rest + '&' + encodeParam

        try:
            if (data != '' and data != None):
                # data = getparmsvalue.get_parms_value(data, env)
                if (headers != ''):
                    if ('{{' in headers):
                        headers = getparmsvalue.get_parms_value(headers, env)
                    headers = ast.literal_eval(headers)

                new_data, params_list = getparmsvalue.get_params_values_list(data, env)
                #20190816-dff: 兼容未使用参数且需base64编码处理时，也需要对new_data处理
                if isBase64Encode:
                    new_data = base64Encode(new_data)
                if params_list != {}:  #  data 需要参数化
                    data_list = getparmsvalue.set_params_list(data, params_list)
                    print("data_list:", data_list)
                    ## 20190727 dff: 增加对入参base64编码单独处理
                    if isBase64Encode:
                        data_list_tmp = []
                        for item in data_list:
                            data_list_tmp.append(base64Encode(item))
                        data_list = data_list_tmp
                    ####----------dff 20190727 以上 -----------####
                    #循环执行参数化后的data入参
                    if d_list !=[]:
                        for url_item in d_list:
                            for data_item in data_list:
                                time = 0
                                response = {}
                                try:
                                    r = requests.put(url_item, data=data_item.encode('utf-8'), headers=headers)
                                    #接口运行时间
                                    time = r.elapsed.microseconds/1000
                                    try:
                                        r = json.loads(r.text, object_pairs_hook=OrderedDict);
                                        z = json.dumps(r, ensure_ascii=False)
                                    except:
                                        z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                                    # dff - 20191012 增加对出参是否需base64解码的判断处理
                                    if isBase64Decode:
                                        z = base64Decode(z)
                                    response['res'] = z
                                    response['success'] = success
                                except Exception as e:
                                    response['res'] = e
                                    response['success'] = False

                                response['time']=time
                                response['url'] = url_item
                                response['data'] = data_item
                                response_list.append(response)
                    elif rest_list != [] and d_list == []:
                        for url_item in rest_list:
                            for data_item in data_list:
                                time = 0
                                response = {}
                                try:
                                    r = requests.put(url_item, data=data_item.encode('utf-8'), headers=headers)
                                    #接口运行时间
                                    time = r.elapsed.microseconds/1000
                                    try:
                                        r = json.loads(r.text, object_pairs_hook=OrderedDict);
                                        z = json.dumps(r, ensure_ascii=False)
                                    except:
                                        z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                                    # dff - 20191012 增加对出参是否需base64解码的判断处理
                                    if isBase64Decode:
                                        z = base64Decode(z)
                                    response['res'] = z
                                    response['success'] = success
                                except Exception as e:
                                    response['res'] = e
                                    response['success'] = False
                                response['time']=time
                                response['url'] = url_item
                                response['data'] = data_item
                                response_list.append(response)
                    else:
                        for data_item in data_list:
                            time = 0
                            response = {}
                            try:
                                r = requests.put(new_rest, data=data_item.encode('utf-8'), headers=headers)
                                #接口运行时间
                                time = r.elapsed.microseconds/1000
                                try:
                                    r = json.loads(r.text, object_pairs_hook=OrderedDict);
                                    z = json.dumps(r, ensure_ascii=False)
                                except:
                                    z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                                # dff - 20191012 增加对出参是否需base64解码的判断处理
                                if isBase64Decode:
                                    z = base64Decode(z)
                                response['res'] = z
                                response['success'] = success
                            except Exception as e:
                                response['res'] = e
                                response['success'] = False
                            response['time']=time
                            response['url'] = new_rest
                            response['data'] = data_item
                            response_list.append(response)

                else: #data 无需参数化
                    if d_list != []:
                        for url_item in d_list:
                            time = 0
                            response = {}
                            try:
                                r = requests.put(url_item,data = new_data.encode('utf-8'), headers=headers)
                                    #接口运行时间
                                time = r.elapsed.microseconds/1000
                                try:
                                    r = json.loads(r.text, object_pairs_hook=OrderedDict);
                                    z = json.dumps(r, ensure_ascii=False)
                                except:
                                    z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                                # dff - 20191012 增加对出参是否需base64解码的判断处理
                                if isBase64Decode:
                                    z = base64Decode(z)
                                response['res'] = z
                                response['success'] = success
                            except Exception as e:
                                response['res'] = e
                                response['success'] = False
                            response['time']=time
                            response['url'] = url_item
                            # response['data'] = new_data.encode('utf-8')
                            response['data'] = new_data
                            response_list.append(response)
                    elif rest_list != [] and d_list == []:
                        for url_item in rest_list:
                            time = 0
                            response = {}
                            try:
                                r = requests.put(url_item,data=new_data.encode('utf-8'), headers=headers)
                                    #接口运行时间
                                time = r.elapsed.microseconds/1000
                                try:
                                    r = json.loads(r.text, object_pairs_hook=OrderedDict);
                                    z = json.dumps(r, ensure_ascii=False)
                                except:
                                    z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                                # dff - 20191012 增加对出参是否需base64解码的判断处理
                                if isBase64Decode:
                                    z = base64Decode(z)
                                response['res'] = z
                                response['success'] = success
                            except Exception as e:
                                response['res'] = e
                                response['success'] = False
                            response['time']=time
                            response['url'] = url_item
                            # response['data'] = new_data.encode('utf-8')
                            response['data'] = new_data
                            response_list.append(response)
                    else:
                        time = 0
                        response = {}
                        try:
                            r = requests.put(new_rest, data=new_data.encode('utf-8'),headers=headers)
                                    #接口运行时间
                            time = r.elapsed.microseconds/1000
                            try:
                                r = json.loads(r.text, object_pairs_hook=OrderedDict);
                                z = json.dumps(r, ensure_ascii=False)
                            except:
                                z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                            # dff - 20191012 增加对出参是否需base64解码的判断处理
                            if isBase64Decode:
                                z = base64Decode(z)
                            response['res'] = z
                            response['success'] = success
                        except Exception as e:
                            response['res'] = e
                            response['success'] = False
                        response['time']=time
                        response['url'] = new_rest
                        # response['data'] = new_data.encode('utf-8')
                        response['data'] = new_data
                        response_list.append(response)
            else:  # 当未传递data  , 其实对于post 请求来说，这种情况应该不存在
                if (headers != ''):
                    headers = eval(headers)
                if d_list != []:  # 不为空时，代表d参数有参数化，则循环请求
                    for rest_item in d_list:
                        time = 0
                        response = {}
                        try:
                            r = requests.put(rest_item, headers=headers)
                            # 接口运行时间
                            time = r.elapsed.microseconds/1000
                            try:
                                r = json.loads(r.text, object_pairs_hook=OrderedDict)
                                z = json.dumps(r, ensure_ascii=False)
                            except:
                                z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                            # dff - 20191012 增加对出参是否需base64解码的判断处理
                            if isBase64Decode:
                                z = base64Decode(z)
                            response['res'] = z
                            response['success'] = success
                        except Exception as e:
                            response['res'] = e
                            response['success'] = False
                        response['time']=time
                        response['url'] = rest_item
                        response['data'] = ''
                        response_list.append(response)

                elif rest_list != [] and d_list == []:
                    for rest_item in rest_list:
                        time = 0
                        response = {}
                        try:
                            r = requests.put(rest_item, headers=headers)
                            # 接口运行时间
                            time = r.elapsed.microseconds/1000
                            try:
                                r = json.loads(r.text, object_pairs_hook=OrderedDict)
                                z = json.dumps(r, ensure_ascii=False)
                            except:
                                z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                            # dff - 20191012 增加对出参是否需base64解码的判断处理
                            if isBase64Decode:
                                z = base64Decode(z)
                            response['res'] = z
                            response['success'] = success
                        except Exception as e:
                            response['res'] = e
                            response['success'] = False

                        response['time']=time
                        response['url'] = rest_item
                        response['data'] = ''
                        response_list.append(response)
                else:
                    time = 0
                    response = {}
                    try:
                        r = requests.put(new_rest, headers=headers)
                        # 接口运行时间
                        time = r.elapsed.microseconds/1000
                        try:
                            r = json.loads(r.text, object_pairs_hook=OrderedDict)
                            z = json.dumps(r, ensure_ascii=False)
                        except:
                            z,success= (r.status_code,False)  if r.status_code !=200 else (r.text,success)
                        # dff - 20191012 增加对出参是否需base64解码的判断处理
                        if isBase64Decode:
                            z = base64Decode(z)
                        response['res'] = z
                        response['success'] = success
                    except Exception as e:
                        response['res'] = e
                        response['success'] = False
                    response['time']=time
                    response['url'] = new_rest
                    response['data'] = ''
                    response_list.append(response)
        except Exception as e:
            print(e)
            z='调用的put 请求方法异常'
            time=0
        # 返回dict（接口返回值以及接口运行时间）
            response = {}
            response['res'] = z
            response['time'] = time
            response['success'] = False
            response_list.append(response)
        return response_list
#
if __name__ == '__main__':
    i=Parameter_Interface()


    # ****---以下是get接口----****
    url = 'https://api.tuniu.com/portal/home/data/indexWithLocation?c={"cc":3415,"ct":10,"p":14588,"ov":20,"dt":0,"v":{{Version}}}'
    dParam = '{"height":1334,"location":{"lng":118.8822476222722,"lat":32.08730600292966},"width":750,\
    "uniqueKey":"c6777549d3dca9d907271ee6ac3d189df00fdb49","localCityCode":1602,"abroadCityCode":{{cityCode}},"clientModel":"iPhone 6s","bookCityName":{{cityName}}}'
    data = ''

    url ='''https://api.tuniu.com/portal/home/data/indexWithLocation?c={"cc":3415,"ct":10,"p":14588,"ov":20,"dt":0,"v":{{Version}}}&d={"height":1334,"location":{"lng":118.8822476222722,"lat":32.08730600292966},"width":750,"uniqueKey":"c6777549d3dca9d907271ee6ac3d189df00fdb49","localCityCode":1602,"abroadCityCode":{{cityCode}},"clientModel":"iPhone 6s","bookCityName":{{cityName}}}'''

    response = i.getinterfaceone(url,'','prd','','')
    for i in response:
        print(type(i),i)


    #以下是post接口
    # url = 'https://api.tuniu.com/batch/search/list?c={"cc":1602,"ct":20,"dt":1,"ov":20,"p":19326,"v":{{Version}}}'
    # data = '''{
    # "catId": 0,
    # "customMode": 0,
    # "displayType": 0,
    # "height": 0,
    # "isDirectSearch": true,
    # "isShowDot": false,
    # "keyword": {{cityName}},
    # "lastKey": "",
    # "lat": "32.085189",
    # "limit": 15,
    # "lng": "118.887424",
    # "locateCityCode": 1602,
    # "maxHour": 0,
    # "maxPrice": -1,
    # "minHour": 0,
    # "minPrice": 0,
    # "originalKeyword": {{cityName}},
    # "page": 1,
    # "poiId": 0,
    # "productType": 0,
    # "recommendPlan": "通用",
    # "searchKey": [],
    # "searchType": 1,
    # "tabId": 0,
    # "tact": "354782065438272",
    # "tagName": "",
    # "title": "",
    # "useSpecialType": 0,
    # "width": 0}'''
    # response = i.postinterfaceone(url,data,'prd','','')
    # print(response,'\n', len(response), '\n',type(response))
    # for i in response:
    #     print(type(i),i)