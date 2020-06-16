# -*- coding: utf-8 -*-
# TIME:         上午10:29
# Author:       xutaolin

from app.models.models import *
from flask import Blueprint, request, make_response
from flask import jsonify
from sqlalchemy import and_, or_, distinct, text
from app.actions.interfaceAuto.apirequest import Interface
from app.actions.interfaceAuto.check import CheckOut
from app.actions.interfaceAuto.batchcheck import BatchCheck
from app.actions.interfaceAuto.batchRequest import batchRequest
from app.actions.interfaceAuto.query import query,newlist
from app.actions.interfaceAuto.GetParmsValue import GetParmsValue
import json,ast,logging
import dateutil.parser
import pytz
from datetime import datetime
from sqlalchemy import func
import time
from app import db,cache

from app import app
from app.actions.interfaceAuto.query import queryallpid,querychilddict

##dff add
from app.actions.interfaceAuto.interface_parameter import Parameter_Interface
import base64
from app.actions.interfaceAuto.interface_tsp import *
import time
from app.actions.interfaceAuto.checkResponseField import CheckResult_by_reExpression, re_CheckResult, re_newCheck, re_string2list
from concurrent.futures import ThreadPoolExecutor
executor =ThreadPoolExecutor(1)

from app.actions.interfaceAuto.interface_pepple import *



global null
null = None

# 设置蓝图
interface = Blueprint('interface', __name__, url_prefix="")
# 解决跨域问题
def cors_response(res):
    response = json.dumps(res,ensure_ascii=False)
    response = make_response(response)
    # response.addHeader("Access-Control-Max-Age", "2592000")
    response.headers["Access-Control-Max-Age"]= "2592000"
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,POST,GET,DELETE,OPTIONS'
    # response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, t'
    # response.headers['Access-Control-Allow-Headers'] = 'Referer,Accept,Origin,User-Agent'
    response.headers['Access-Control-Allow-Credentials'] = True
    return response

# 运行用例接口(不做任何入库操作也并不做任何校验，只是单纯的调用接口)
@interface.route('/runCase', methods=['GET', 'POST'])
def runinterface():
    interface = Interface()
    # 获取入参
    env = request.get_json().get('env')
    headers = request.get_json().get('header')

    #获取当前运行人
    user=request.get_json().get('user') #取不到值的时候为None

    #20190718 dff；增加接口类型处理（rest, tsp)
    requestType = request.get_json().get('requestType')
    #如果是tsp类型，则通过界面输入的服务名tsp接口查询ip,path、method信息
    if requestType == 'tsp':
        tsp_name = request.get_json().get('url')
        tsp_interface = TspSearch(tsp_name,env)
        tsp_interface = tsp_interface.tsp2interface()
        print(tsp_interface)
        if tsp_interface is None:
            response = {"success": False, "data": "未查询到tsp服务所对应的接口！"}
            return cors_response(response)
        else:
            tsp_interface=json.loads(tsp_interface)
            print(tsp_interface["ip"], type(tsp_interface["ip"]))
            print(tsp_interface["path"], type(tsp_interface["path"]))
            url = "http://" + str(tsp_interface["ip"]) + tsp_interface["path"]
            requestmethod = tsp_interface["method"]
            print(requestmethod)
    elif requestType == 'rest':
        requestmethod = request.get_json().get('requestmethod')
        url = request.get_json().get('url').strip()
        if( url.startswith('http://') ==False and  url.startswith('https://') == False):
            url='http://'+url
    #20191225 dff增加对pepple接口的处理
    elif requestType == 'pepple':
        requestmethod = 'pepple'
        url = request.get_json().get('url').strip()  #指pepple的serviceName
        queryMethod = request.get_json().get('queryMethod')  # pepple的queryMethod

    print(url)

    #dff-20190727: 新增入参base64编码功能
    isBase64Encode = request.get_json().get('isBase64Encode')
    isBase64Decode = request.get_json().get('isBase64Decode')   # dff-20191009: 增加出参是否需直接base64解码判断
    inputparam = request.get_json().get('inputparam')
    dParam = request.get_json().get('dParam')

    # 处理请求头
    flag = True
    dict = {}
    for i in range(len(headers)):
        if (headers[i]['key'] != '' or headers[i]['value'] != ''):
            flag_assert = True
            break
        else:
            flag = False
    if (flag == True):
        for i in range(len(headers)):
            k = headers[i]['key']
            v = headers[i]['value']
            dict[k] = v
        headers = str(dict)
    else:
        headers = ''
    print('the requestType is : ',requestType)
    print('the requestMethod is :',requestmethod)
    try:
        if (requestmethod in( 'get','GET')):
            response = interface.getinterfaceone(url, inputparam, env, headers, dParam, isBase64Encode, isBase64Decode)
            #如果是tsp请求，则对响应信息做base64解码处理再返回
            if requestType == 'tsp':
                response = base64Decode(response)
            # response转成字典
            try:
                response = json.loads(response)
                response={"success": True, "data":response}
            except:
                response = {"success": True, "data": response}

        elif (requestmethod in( 'post','POST')):
            response = interface.postinterfaceone(url, inputparam, env, headers, dParam, isBase64Encode, isBase64Decode)
            # print("tsp response: ", response, '\n', type(response))

            #如果是tsp请求，则对响应信息做base64解码处理再返回
            if requestType == 'tsp':
                response = base64Decode(response)
            # response转成字典
            try:
                response = json.loads(response)
                response = {"success": True, "data": response}
            except:
                response = {"success":True, "data": response}

        elif (requestmethod in( 'put','PUT')):
            response = interface.putinterfaceone(url, inputparam, env, headers, dParam, isBase64Encode, isBase64Decode)
            # print("tsp response: ", response, '\n', type(response))

            #如果是tsp请求，则对响应信息做base64解码处理再返回
            if requestType == 'tsp':
                response = base64Decode(response)
            # response转成字典
            try:
                response = json.loads(response)
                response = {"success": True, "data": response}
            except:
                response = {"success":True, "data": response}

        #增加pepple的处理
        elif (requestmethod in ('pepple','PEPPLE')):
            response = InterfacePepple(env,url,queryMethod,inputparam).peppleRun()
        else:
            response = {"success":False, "data": "请求方式不正确"}
    except Exception as e:
        print(e)
        response = {"success": False, "data": "方法异常"}
    return cors_response(response)

# 校验接口(其中入库操作只做全局变量的)
@interface.route('/check', methods=['GET', 'POST'])
def check():
    # 获取入参
    env = request.get_json().get('env')
    # 出参---刚开始取到的值为dict形式
    outparam = request.get_json().get('outparam')
    #转换成json格式并且 中文正常输出
    outparam=json.dumps(outparam, ensure_ascii=False)
    # 全局变量信息
    globalvar = request.get_json().get('globalvar')
    #校验字段信息
    assertInfo =request.get_json().get('assertInfo')
    #获取当前运行人
    user=request.get_json().get('user')
    # assertInfo不为空数组的时候处理校验信息 格式 route;route       expected_response;expected_response
    if(len(assertInfo) !=0):
        # 路径
        route = []
        # 期望值
        expeted_field = []
        types=[]
        flag_assert = True
        for i in range(len(assertInfo)):
            if (assertInfo[i]['key'] != '' or assertInfo[i]['value'] != ''):
                flag_assert = True
                break
            else:
                flag_assert = False
        if (flag_assert == True):
            for i in range(len(assertInfo)):
                k = assertInfo[i]['key']
                v = assertInfo[i]['value']
                check_type=assertInfo[i]['checkType']
                if(k !='' or v!=''):
                    route.append(k)
                    expeted_field.append(v)
                    types.append(check_type)
            route = ';'.join(route)
            expeted_field = ';'.join(expeted_field)
            types=';'.join(types)
        else:
            route = ''
            expeted_field = ''
            types = ''
    else:
        route =''
        expeted_field = ''
        types=''

    # 获取块信息
    expectedcontent = request.get_json().get('expectedcontent')

    # 当globalvar不为空的时候处理全局变量  name;name    route;route  格式
    # 2.全局变量信息不为空
    # 2.1全局变量都为空
    if(len(globalvar)!=0):
        # 路径
        globalname = []
        # 期望值
        globalroute = []

        flag_global = True
        for i in range(len(globalvar)):
            if (globalvar[i]['key'] != '' or globalvar[i]['value'] != ''):
                flag_global = True
                break
            else:
                flag_global = False
        if (flag_global == True):
            for i in range(len(globalvar)):
                k = globalvar[i]['key']
                v = globalvar[i]['value']
                if(k!='' or  v!=''):
                    globalname.append(k)
                    globalroute.append(v)
            globalname = ';'.join(globalname)
            globalroute = ';'.join(globalroute)
    else:
        globalname = ''
        globalroute = ''

    # 进行校验
    # 1.出参不为空
    # 1.1校验值信息 && 块信息不全为空
    # 1.2校验信息,全局变量和块信息都为空----前端已处理，该种情况不会调用校验方法
    print(env, outparam, globalname, globalroute, route, expeted_field, expectedcontent,types)

    checkOut = CheckOut(env, outparam, globalname, globalroute, route, expeted_field,types, expectedcontent,user)
    if (outparam != ''):
        response=checkOut.checkout()

    ## 20190831 dff; 增加 批量字段正则校验功能
    reCheck = request.get_json().get('regex_checklist')
    print('reCheck:',reCheck)
    if outparam != '':
        if (len(reCheck)>0 and reCheck != [{'key': '', 'value': ''}]):
            can_reCheck_list = []
            check_error_list = []
            checkflag = True
            # 获取校验字段值及正则表达式值都不为空的信息
            for i in range(len(reCheck)):
                if reCheck[i]['key']  in ('',None) or reCheck[i]['value']  in ('',None):
                    result = {'success': False,'msg':'存在正则校验字段或表达式值为空，无法进行校验，请检查！'}
                    checkflag = False
                    break
                else:
                    can_reCheck_list.append(reCheck[i])
                    checkflag = True
            if checkflag and  len(can_reCheck_list) > 0:
                outparam = json.loads(outparam,encoding='utf-8')
                for i in can_reCheck_list:
                    checklist = re_string2list(i['key'])
                    if checklist == []:
                        tmp_dict = {}
                        tmp_dict[i['key']] = '输入的正则校验字段格式有误'
                        check_error_list.append(tmp_dict)
                    else:

                        print('响应信息：',outparam,type(outparam))
                        print('正则检查字段：',checklist)
                        print('正则表达式',i['value'])
                        result,result_msg = re_newCheck(checklist,outparam,i['value'])
                        if result is False or result_msg != []:
                            tmp_dict = {}
                            tmp_dict[i['key']] = result_msg  or '返回值正则校验失败'
                            check_error_list.append(tmp_dict)

                if check_error_list == []:
                    result = {'success': True, 'msg': '批量字段正则校验成功'}
                else:
                    result = {'success': False, 'msg': str(check_error_list)}
            else:
                result = {'success': True,'msg':''}

            # 将上述的response 与 result 结果组合：
            if response['success'] == True and result['success'] == True:
                response = {'success': True, 'msg':'预期结果校验成功'}
            elif response['success'] == True and result['success'] == False:
                response = {'success': False, 'msg': result['msg']}
            elif response['success'] == False and result['success'] == True:
                response = {'success': False, 'msg': response['msg']}
            else:
                response = {'success': False, 'msg':str(response['msg'])+ str(result['msg'])}

    return cors_response((response))

#查询用例信息
@interface.route('/queryCaseInfo',methods=['GET'])
def querycase():
    try:
        # treeid = request.get_json().get('treeid')
        treeid=request.args['treeid']
        env=request.args['env']
        if (treeid == '' or treeid == None):
            return cors_response({"success": False, "msg": "参数必传"})

        # 通过tree_id查询是否存在用例信息
        res = {}
        tmp_data = {}
        count = Interface_Mall.query.filter(and_(Interface_Mall.tree_id==treeid,Interface_Mall.env==env)).count()
        print("count:",count)

        if (count != 0):  # 查询信息
            caseinfo = Interface_Mall.query.filter(and_(Interface_Mall.tree_id==treeid,Interface_Mall.env==env)).first()
            # 查询的时候需要返回用例id，便于保存的时候是更新还是新增
            res['success'] = True
            res['msg'] = 'OK'
            tmp_data['id']=caseinfo.id
            tmp_data['env'] = env
            tmp_data['requestmethod'] = caseinfo.request
            tmp_data['header'] = caseinfo.headers
            tmp_data['url'] = caseinfo.rest
            tmp_data['inputparam'] = caseinfo.data  # 数据库中存储的应该存非json格式化的，这样查出来的才会没有空格
            tmp_data['globalvar'] = caseinfo.global_var
            tmp_data['assertInfo'] = caseinfo.assert_info
            tmp_data['expectedcontent'] = caseinfo.expected_response
            tmp_data['name']=caseinfo.name
            tmp_data['treeid']=treeid
            #dff：20190625 获取新增的c, d参数信息
            tmp_data['dParam'] = caseinfo.dParam
            # res['selectedtag']=json.loads(caseinfo.tag)
            if(count ==1):
                if(caseinfo.tag !='' and caseinfo.tag!=None ):
                    tmp_data['selectedtag']=caseinfo.tag
                else:
                    tmp_data['selectedtag'] = []
            else:
                caseinfo_all= Interface_Mall.query.filter(and_(Interface_Mall.tree_id==treeid,Interface_Mall.env==env)).all()
                tmp_data['selectedtag'] = []
                for caseinfo_one in caseinfo_all:
                    tmp_data['selectedtag'].append(caseinfo_one.tag)
                print(tmp_data['selectedtag'])


            #20190722-dff: 增加接口类型字段的处理
            tmp_data['requestType'] = caseinfo.request_type
            tmp_data['isBase64Encode'] = caseinfo.isBase64Encode
            #20190902-dff: 新增批量正则校验字段列表
            tmp_data['regex_checklist'] = caseinfo.regex_checklist
            #dff-20191010 add
            tmp_data['isBase64Decode'] = caseinfo.isBase64Decode
            #dff - 20191226 add
            tmp_data['queryMethod'] = caseinfo.queryMethod
            res['data']=tmp_data
            response = res
        elif (count == 0):
            caseinfo = Interface_Mall.query.filter(Interface_Mall.tree_id == treeid).first()
            # response = {"id":None,"env":env,"requestmethod":None,"header":None,"url":None,"inputparam":None,"globalvar":None,"assertInfo":None
            #             ,"expectedcontent":None,"name":None,"selectedtag":None,"treeid":treeid,"dParam":'',"resquestType":"rest","isBase64Encode":False}
            response = {"success": True, "msg": "未查询到用例", "data": {"id":None,"env":env,"requestmethod":None,"header":None,"url":None,"inputparam":None,"globalvar":None,"assertInfo":None
                        ,"expectedcontent":None,"name":caseinfo.name,"selectedtag":None,"treeid":treeid,"dParam":'',"requestType":"rest","isBase64Encode":False,
                                                                   "regex_checklist":None, "isBase64Decode":False}}
        else:
            response = {"success": False, "msg": "查询失败，请检查用例数据~"}
    except Exception as e:
        print(e)
        response = {"success": False, "msg": "请检查参数"}

    return cors_response(response)


#保存接口用例信息(全部入库，不做校验)
@interface.route('/saveCase',methods=['POST'])
def savecase():
    #获取表单所有参数
    requestType = request.get_json().get('requestType')
    print("接口类型：",requestType)
    env = request.get_json().get('env')
    queryMethod = ''  # 该字段仅pepple需要用，先初始化为空字符串,若是pepple接口会通过下方重新获取
    #如果是tsp类型，则通过界面输入的服务名tsp接口查询ip,path、method信息
    if requestType == 'tsp':
        url = request.get_json().get('url')
        tsp_interface = TspSearch(url,env)
        tsp_interface = tsp_interface.path_search()
        print(tsp_interface)
        if tsp_interface is None:
            response = {"success": False, "data": "未查询到tsp服务所对应的接口！"}
            return cors_response(response)
        else:
            # tsp_interface=json.loads(tsp_interface)
            requestmethod = tsp_interface["method"]
            print(requestmethod)
    elif requestType == 'rest':  # 普通接口直接通过界面获取请求方式（get, post)
        requestmethod = request.get_json().get('requestmethod')
        url = request.get_json().get('url')
    #20191226 dff 新增pepple接口实现
    elif requestType == 'pepple':
        requestmethod = 'pepple'
        url = request.get_json().get('url')
        queryMethod = request.get_json().get('queryMethod')

    if(url not in ('',None)):
        url=url.strip()
    headers = request.get_json().get('header')
    headers=json.dumps(headers)

    print("method: ",requestmethod)

    #dff-20190727: 新增入参base64编码功能
    isBase64Encode = request.get_json().get('isBase64Encode')
    isBase64Decode = request.get_json().get('isBase64Decode') #dff-20191009: 增加出参是否base64解码标志，记录到表
    inputparam = request.get_json().get('inputparam')

    # 注意保存之后的是单引号还是双引号
    globalvar=request.get_json().get('globalvar')
    #把单引号转成双引号
    globalvar=json.dumps(globalvar)

    assertinfo=request.get_json().get('assertInfo')
    assertinfo=json.dumps(assertinfo)
    expectedcontent=request.get_json().get('expectedcontent')
    #用来判断用例是新增还是更新
    id=request.get_json().get('id')
    #tag---jenkins运行用例时所需参数,生成用例的条数也根据该字段判断
    #此时从前端获取的是个list
    tag=request.get_json().get('selectedtag')
    module_tag = tag # 先将所选择和tag记录下来，供关联模块数据时使用
    print('module_tag:',tag)
    #tree_id表示用例和树的关系----保存的时候tree_id,name--用例名为必传
    tree_id=request.get_json().get('treeid')
    name = request.get_json().get('name')

    #dff: 20190625 增加新的参数c、d的处理，保存到数据库
    dParam = request.get_json().get('dParam')

    #20190902-dff: 新增批量正则校验字段列表
    regex_checklist = request.get_json().get('regex_checklist')
    # if regex_checklist in ('',[]):
    #     regex_checklist = None
    regex_checklist = json.dumps(regex_checklist)

    #如果选择的标签存在和环境不匹配的情况,则根据标签 来匹配环境

    #该env,该tree_id下面有几条数据
    # count_env_id=Interface_Mall.query.filter(and_(Interface_Mall.tree_id==tree_id,Interface_Mall.env==env)).count()
    # all_env_id=Interface_Mall.query.filter(and_(Interface_Mall.tree_id==tree_id,Interface_Mall.env==env)).all()

    if(tree_id not  in ('',None) and name not in ('',None)):
        #保存用例信息到数据库中
        #若参数中不存在id或者id为空，则直接新增数据到库中 ,否则更新

        #1.先判断tag是否为空
        #2.若为空或者长度为1，则直接更新数据库已有的一条--1条数据，env还是页面填写的env,不需要通过tag来进行解析
        #3.若长度大于1，每个tag生成一条数据，env 通过解析tag生成
        try:
            if(tag == None or len(tag) in (0,1)):
                if (id != '' and id !=None):
                    if(len(tag)==1):
                        # 如果选择的标签存在和环境不匹配的情况,则根据标签 来匹配环境
                        if('sit' in tag[0].lower()):
                            env='sit'
                        elif('pre' in tag[0].lower()):
                            env= 'pre'
                        elif('prd' in tag[0].lower()):
                            env='prd'
                        else:
                             env = ''
                        # 该env,该tree_id下面有几条数据
                        count_env_id = Interface_Mall.query.filter(
                            and_(Interface_Mall.tree_id == tree_id, Interface_Mall.env == env)).count()
                        all_env_id = Interface_Mall.query.filter(
                            and_(Interface_Mall.tree_id == tree_id, Interface_Mall.env == env)).all()

                        #判断是删除还是更新还是新增
                        #1 表中同样环境和tree_id的用例如果是1条
                        #1.1 该条数据的tag和此次传入的tag一致 或者 不一致，则直接更新已有的这条数据
                        #2 表中同样环境和tree_id的用例如果是多条
                        #2.1 传入的tag在表中存在 则直接更新,其余的数据删除
                        #2.2 传入的tag在表中不存在 则取第一条数据  更新成该tag,其余的tag的数据则删除
                        #3 表中同样环境和tree_id的用例如果是0条
                        #3.1 新增数据
                        tag = tag[0]
                        if(count_env_id==1):
                                # 加锁
                                Interface_Mall.query.filter(
                                    and_(Interface_Mall.tree_id == tree_id, Interface_Mall.env == env)).with_lockmode('update')
                                # 更新
                                Interface_Mall.query.filter(
                                    and_(Interface_Mall.tree_id == tree_id, Interface_Mall.env == env)).update({
                                    'name': name,
                                    'env': env,
                                    'request': requestmethod,
                                    'rest': url,
                                    'data': inputparam,
                                    'expected_response': expectedcontent,
                                    'assert_info': assertinfo,
                                    'global_var': globalvar,
                                    'tree_id': tree_id,
                                    'headers': headers,
                                    'tag': tag,
                                    'dParam': dParam,  # 增加新增的c\d参数信息
                                    'request_type': requestType,  # 20190719dff: 增加接口类型的记录（rest, tsp)
                                    'isBase64Encode': isBase64Encode,  # 20190727-dff: 增加入参是否需要base64编码标识
                                    'regex_checklist': regex_checklist, #20190902-dff: 新增批量正则校验字段列表
                                    'isBase64Decode': isBase64Decode, # dff-20191009 增加
                                    'queryMethod': queryMethod, #dff-20191226 新增pepple查询方法字段
                                })
                        elif(count_env_id ==0):
                            #数据库新增
                            caseInfo = Interface_Mall(
                                name=name,
                                request=requestmethod,
                                rest=url,
                                data=inputparam,
                                headers=headers,
                                expected_response=expectedcontent,
                                env=env,
                                global_var=globalvar,
                                assert_info=assertinfo,
                                tree_id=tree_id,
                                tag=tag,
                                dParam=dParam,
                                request_type=requestType,
                                isBase64Encode=isBase64Encode,
                                regex_checklist=regex_checklist, #20190902-dff: 新增批量正则校验字段列表
                                isBase64Decode=isBase64Decode, # dff-20191009 增加
                                queryMethod=queryMethod, #dff-20191226 新增pepple查询方法字段
                            )

                            db.session.add(caseInfo)
                            # db.session.flush()  # 主要是这里，写入数据库，但是不提交
                            db.session.commit()
                        else:
                            flag=0
                            for one_env_id in all_env_id:
                                flag=1
                            if(flag==1):
                                #则筛选出该条进行更新
                                # 加锁
                                Interface_Mall.query.filter(and_(Interface_Mall.tree_id==tree_id,Interface_Mall.env==env,Interface_Mall.tag ==tag)).with_lockmode('update')
                                # 更新
                                Interface_Mall.query.filter(and_(Interface_Mall.tree_id==tree_id,Interface_Mall.env==env,Interface_Mall.tag ==tag)).update({
                                    'name': name,
                                    'env': env,
                                    'request': requestmethod,
                                    'rest': url,
                                    'data': inputparam,
                                    'expected_response': expectedcontent,
                                    'assert_info': assertinfo,
                                    'global_var': globalvar,
                                    'tree_id': tree_id,
                                    'headers': headers,
                                    'tag': tag,
                                    'dParam': dParam,  # 增加新增的c\d参数信息
                                    'request_type': requestType,  # 20190719dff: 增加接口类型的记录（rest, tsp)
                                    'isBase64Encode': isBase64Encode,  # 20190727-dff: 增加入参是否需要base64编码标识
                                    'regex_checklist': regex_checklist, #20190902-dff: 新增批量正则校验字段列表
                                    'isBase64Decode': isBase64Decode, # dff-20191009 增加
                                    'queryMethod': queryMethod, #dff-20191226 新增pepple查询方法字段
                                })
                            elif(flag ==0):
                                # 2.2 传入的tag在表中不存在 则取其中一条数据  更新成该tag,其余的tag的数据则删除
                                # 加锁
                                Interface_Mall.query.filter(and_(Interface_Mall.tree_id==tree_id,Interface_Mall.env==env)).with_lockmode('update')
                                # 更新
                                Interface_Mall.query.filter(and_(Interface_Mall.tree_id==tree_id,Interface_Mall.env==env)).update({
                                    'name': name,
                                    'env': env,
                                    'request': requestmethod,
                                    'rest': url,
                                    'data': inputparam,
                                    'expected_response': expectedcontent,
                                    'assert_info': assertinfo,
                                    'global_var': globalvar,
                                    'tree_id': tree_id,
                                    'headers': headers,
                                    'tag': tag,
                                    'dParam': dParam,  # 增加新增的c\d参数信息
                                    'request_type': requestType,  # 20190719dff: 增加接口类型的记录（rest, tsp)
                                    'isBase64Encode': isBase64Encode,  # 20190727-dff: 增加入参是否需要base64编码标识
                                    'regex_checklist': regex_checklist, #20190902-dff: 新增批量正则校验字段列表,
                                    'isBase64Decode': isBase64Decode, # dff-20191009 增加
                                    'queryMethod': queryMethod, #dff-20191226 新增pepple查询方法字段
                                })

                                db.session.commit()
                                response = {"success": True, "msg": "保存成功"}
                                print(response)
                            #查询需要删除其余的tag的数据
                            d_all_ntag = Interface_Mall.query.filter(and_(Interface_Mall.tree_id==tree_id,Interface_Mall.env==env,Interface_Mall.tag != tag)).delete()
                            db.session.commit()

                    else:
                        tag=None
                        # 若tag为空，则新增一条tag为空的数据，并且删除同环境下同tree_id下其他带有tag的数据
                        # 加锁
                        Interface_Mall.query.filter_by(id=id).with_lockmode('update')
                        # 更新
                        Interface_Mall.query.filter_by(id=id).update({
                            'name': name,
                            'env': env,
                            'request': requestmethod,
                            'rest': url,
                            'data': inputparam,
                            'expected_response': expectedcontent,
                            'assert_info': assertinfo,
                            'global_var': globalvar,
                            'tree_id': tree_id,
                            'headers': headers,
                            'tag': tag,
                            'dParam': dParam,  #增加新增的c\d参数信息
                            'request_type': requestType,  # 20190719dff: 增加接口类型的记录（rest, tsp)
                            'isBase64Encode': isBase64Encode, #20190727-dff: 增加入参是否需要base64编码标识
                            'regex_checklist': regex_checklist, #20190902-dff: 新增批量正则校验字段列表
                            'isBase64Decode': isBase64Decode, # dff-20191009 增加
                            'queryMethod': queryMethod, #dff-20191226 新增pepple查询方法字段
                        })
                        # 查询需要删除其余的tag的数据
                        d_all_ntag = Interface_Mall.query.filter(
                            and_(Interface_Mall.tree_id == tree_id, Interface_Mall.env == env,
                                 Interface_Mall.tag != tag)).delete()
                        db.session.commit()

                    # db.session.delete()
                    response = {"success": True, "msg": "保存成功"}


                else:
                    #无id时新增数据
                    #新增树节点的时候会在interface_mall表里新增一条用例数据，故无tag或者只有一个tag的时候应该都是更新，没有新增---废弃
                    #新增树节点只有一个sit环境的数据，pre和prd环境没有任何数据，故保存的时候需要重新生成数据并保存
                    if(tag ==None):
                        env = env
                    elif('sit' in tag[0].lower()):
                        env = 'sit'
                    elif ('pre' in tag[0].lower()):
                        env = 'pre'
                    elif ('prd' in tag[0].lower()):
                        env = 'prd'
                    else:
                        env = ''
                    caseInfo = Interface_Mall(
                        name=name,
                        request=requestmethod,
                        rest=url,
                        data=inputparam,
                        headers=headers,
                        expected_response=expectedcontent,
                        env=env,
                        global_var=globalvar,
                        assert_info=assertinfo,
                        tree_id=tree_id,
                        tag=tag,
                        dParam=dParam,
                        request_type=requestType,
                        isBase64Encode=isBase64Encode,
                        regex_checklist=regex_checklist,
                        isBase64Decode=isBase64Decode, # dff-20191009 增加
                        queryMethod=queryMethod, #dff-20191226 新增pepple查询方法字段
                    )

                    db.session.add(caseInfo)
                    # db.session.flush()  # 主要是这里，写入数据库，但是不提交
                    db.session.commit()
                    response = {"success": True, "msg": "保存成功"}

            else:
                # if (id != '' and id != None):
                    # for i in range(len(tag)):
                for i in tag:  # dff 修改
                    #tag对应的标签名
                    tag_str = db.session.query(TAG.tag).filter(and_(TAG.tag == i, TAG.del_flag == 0)).first()
                    if('sit' in (tag_str[0]).lower()):
                        env='sit'
                    elif('pre' in (tag_str[0]).lower()):
                        env='pre'
                    elif('prd' in (tag_str[0]).lower()):
                        env='prd'
                    else:
                        env=''
                    tag_case_count_excep_tag=Interface_Mall.query.filter(and_(Interface_Mall.tree_id==tree_id,Interface_Mall.env==env,Interface_Mall.tag ==None)).count()
                    tag_case_count=Interface_Mall.query.filter(and_(Interface_Mall.tree_id==tree_id,Interface_Mall.env==env,Interface_Mall.tag ==i)).count()

                    # 根据tree_id、env、tag为空查出的用例为1条数据,再根据tag查出0条数据
                    if (tag_case_count_excep_tag ==1 and tag_case_count == 0):
                        # 加锁
                        Interface_Mall.query.filter(
                            and_(Interface_Mall.tree_id == tree_id, Interface_Mall.env == env)).with_lockmode('update')
                        # 更新
                        Interface_Mall.query.filter(
                            and_(Interface_Mall.tree_id == tree_id, Interface_Mall.env == env)).update({
                            'name': name,
                            'env': env,
                            'request': requestmethod,
                            'rest': url,
                            'data': inputparam,
                            'expected_response': expectedcontent,
                            'assert_info': assertinfo,
                            'global_var': globalvar,
                            'tree_id': tree_id,
                            'headers': headers,
                            'tag': i,
                            'dParam': dParam,  # 增加新增的c\d参数信息
                            'request_type': requestType,  # 20190719dff: 增加接口类型的记录（rest, tsp)
                            'isBase64Encode': isBase64Encode,  # 20190727-dff: 增加入参是否需要base64编码标识
                            'regex_checklist': regex_checklist, #20190902-dff: 新增批量正则校验字段列表
                            'isBase64Decode': isBase64Decode, # dff-20191009 增加
                            'queryMethod': queryMethod, #dff-20191226 新增pepple查询方法字段
                        })
                        db.session.commit()
                        response = {"success": True, "msg": "保存成功"}
                    #根据标签和tree_id、tag查出的用例为1条数据
                    elif(tag_case_count==1):
                        # 加锁
                        Interface_Mall.query.filter(
                            and_(Interface_Mall.tree_id == tree_id,Interface_Mall.env==env,Interface_Mall.tag==i)).with_lockmode('update')
                        # 更新
                        Interface_Mall.query.filter(
                            and_(Interface_Mall.tree_id == tree_id,Interface_Mall.env==env,Interface_Mall.tag==i)).update({
                            'name': name,
                            'env': env,
                            'request': requestmethod,
                            'rest': url,
                            'data': inputparam,
                            'expected_response': expectedcontent,
                            'assert_info': assertinfo,
                            'global_var': globalvar,
                            'tree_id': tree_id,
                            'headers': headers,
                            'tag': i,
                            'dParam': dParam, #增加新增的c\d参数信息
                            'request_type': requestType,  # 20190719dff: 增加接口类型的记录（rest, tsp)
                            'isBase64Encode': isBase64Encode, #20190727-dff: 增加入参是否需要base64编码标识
                            'regex_checklist': regex_checklist, #20190902-dff: 新增批量正则校验字段列表
                            'isBase64Decode': isBase64Decode, # dff-20191009 增加
                            'queryMethod': queryMethod, #dff-20191226 新增pepple查询方法字段
                        })
                        db.session.commit()
                        response = {"success": True, "msg": "保存成功"}

                    # 根据标签和tree_id查出的用例为0条数据
                    elif(tag_case_count==0):
                        caseInfo = Interface_Mall(
                            name=name,
                            request=requestmethod,
                            rest=url,
                            data=inputparam,
                            headers=headers,
                            expected_response=expectedcontent,
                            env=env,
                            global_var=globalvar,
                            assert_info=assertinfo,
                            tree_id=tree_id,
                            # tag=int(tag[i]),
                            tag = i,  # dff: tag直接记录名TAG表中的tag字段，不再记录为id
                            dParam=dParam,
                            request_type=requestType,  # 20190719dff: 增加接口类型的记录（rest, tsp)
                            isBase64Encode=isBase64Encode, #20190727-dff: 增加入参是否需要base64编码标识
                            regex_checklist=regex_checklist, #20190902-dff: 新增批量正则校验字段列表
                            isBase64Decode=isBase64Decode, # dff-20191009 增加
                            queryMethod=queryMethod, #dff-20191226 新增pepple查询方法字段
                        )

                        db.session.add(caseInfo)
                        # db.session.flush()  # 主要是这里，写入数据库，但是不提交
                        db.session.commit()
                        response = {"success": True, "msg": "保存成功"}
                    # 根据标签和用例id查出的用例为多条数据
                    else:
                        response = {"success": False, "msg":str(tag)+"已经存在多条数据，请检查后新增"}
            # else:
            #     response = {"success": False, "msg": "用例id必须存在"}
        except Exception as  e:
            print(e)
            logging.error(e)
            db.session.rollback()
            response = {"success": False, "msg": "数据库操作失败"}
    else:
        response={"success":False,"msg":"用例文件必须存在"}
    #dff: 20190628 下面是针对 moudle_interface_list 表进行关联数据处理，方便处理覆盖率

    if response == {"success": True, "msg": "保存成功"} and url not in(None,'') and module_tag not in([],None,''):
        index = url.find('?')
        if index == -1:
            path = url
        else:
            path = url[:url.find('?')]

        print('path:',path)

        module_list = Modules_interface_list.query.from_statement(text("SELECT * FROM modules_interface_list WHERE INSTR(right('"+str(path)+"',length(interface_path)),interface_path)>0")).first()

        print("module_list:",module_list)
        print("模块tag:",module_tag,"module_tag[0]：",module_tag[0][:module_tag[0].rfind('-')].replace('-','_'))
        if module_list is not None:
            #更新接口覆盖率表
            try:
                module_list.is_auto = True
                module_list.module_name = module_tag[0][:module_tag[0].rfind('-')].replace('-','_')  # 同步更新module_name,防止有时选错tag后重新修改的情况
                db.session.add(module_list)
                db.session.commit()
                response = {"success": True, "msg": "接口用例保存成功，关联模块数据更新成功"}
            except Exception as e:
                print("异常:",e)
                logging.error(e)
                db.session.rollback()
                response = {"success": True, "msg": "接口用例保存成功，关联模块数据更新失败"}
        elif module_list is None:
            # 新增接口覆盖率表
            try:
                module_interface_info = Modules_interface_list(module_name=module_tag[0][:module_tag[0].rfind('-')].replace('-','_'), interface_path=path,is_auto=True)
                # print("sql:",module_interface_info)
                db.session.add(module_interface_info)
                db.session.commit()
                response = {"success": True, "msg": "接口用例保存成功，关联模块数据新增成功"}
            except Exception as e:
                db.session.rollback()
                print("异常:",e)
                logging.error(e)
                response = {"success": True, "msg": "接口用例保存成功，关联模块数据新增失败"}

    return cors_response(response)


#查询标签
@interface.route('/getTag',methods=['GET'])
def gettag():
    #查询所有标签
    allInfo=TAG.query.filter(TAG.del_flag ==0).all()
    tags=[]
    for i in range(len(allInfo)):
        # id=allInfo[i].id
        tag=allInfo[i].tag
        tags.append({'value':tag,'label':tag})   # dff: 20190628 保存用例时，tag字段直接记录该表的tag信息，不再记录id，方便自动构建触发自动化时系统模块映射

    return cors_response(tags)


@interface.route('/getTreeid', methods=['GET', 'POST'])
def getTreeid():
    if request.method == 'GET':
        # record = request.form.get('record', '')
        treeid = request.args['tree_id']
        interface_one = Interface_Mall.query.filter_by(
            tree_id=treeid).first()
        select_record = {
            "id": interface_one.id,
            "name": interface_one.name,
            "request": interface_one.request,
            "headers": interface_one.headers,
            "rest": interface_one.rest,
            "data": interface_one.data,
            "expected_response": interface_one.expected_response,
            "route": interface_one.route,
            "actual_response": interface_one.actual_response,
            "expected_field": interface_one.expected_field,
            "global_name": interface_one.global_name,
            "global_route": interface_one.global_route,
            "tag": interface_one.tag,
            "env": interface_one.env,
        }
        return jsonify(select_record)


# 通过treeID数组获取ID数组
@interface.route('/getId', methods=['GET', 'POST'])
def getId():
    if request.method == 'GET':
        id_forms = []
        ids = []
        treeid = request.args['tree_id']
        arrId = treeid.split(",")
        interface_ids = []
        for i in range(len(arrId)):
            interface_id = Interface_Mall.query.filter_by(tree_id=arrId[i]).first()
            interface_ids.append(interface_id)

        for i in range(len(interface_ids)):
            ids.append(interface_ids[i].id)
        return jsonify({"data": ids})


@interface.route('/addTree', methods=['POST'])
def add_tree():
    if not request.get_json() or 'name' not in request.get_json():
        response = ({"success": False, "msg": "没有name", "errorCode": 720002})
        return cors_response(response)
    else:
        name = request.get_json().get('name')
        pid = request.get_json().get('pId')
        tree_type = request.get_json().get('dropInner')
        # neworder=request.form['order']
        # print tree_type
        if tree_type == True or tree_type == True:
            tree_type = 1
        else:
            tree_type = 0
        tree_one = Tree_Task.query.filter_by().order_by(Tree_Task.tree_order.desc()).first()
        try:

            tree_tasks = Tree_Task(tree_name=name,
                                   parent_id=pid,
                                   tree_type=tree_type,
                                   tree_order=tree_one.tree_order + 1)
            db.session.add(tree_tasks)
            db.session.flush()  # 主要是这里，写入数据库，但是不提交
            id = tree_tasks.tree_id  # 这样就可以获得自增id了
            tree_order = tree_tasks.tree_order
            tree_two = Tree_Task.query.filter_by().order_by(Tree_Task.tree_order.desc()).first()
            if (tree_two.tree_order == tree_tasks.tree_order):
                # 往用例表里插入一条记录
                if tree_type == 0:
                    Interface_Mall.query.filter_by(tree_id=id).first()
                    add_interface = Interface_Mall(name=name,
                                                   tree_id=id, request="get",env='sit')
                    db.session.add(add_interface)
                db.session.commit()
                response = (
                    {"success": True, "msg": "ok", "errorCode": 720001, "data": {"id": id, "order": tree_order}})

                #层级表新增数据
                pids = queryallpid(id)
                add_case_level = Case_Level(case_id=id,
                                            levels=str(pids))
                db.session.add(add_case_level)
                db.session.commit()

            else:
                db.session.rollback()
                response = ({"success": False, "msg": "tree_order不能重复", "errorCode": 720005})

        except:
            db.session.rollback()
            raise
            response = {"success": False, "msg": "数据库操作失败", "errorCode": 720003, }
        return cors_response(response)


@interface.route('/queryTree', methods=['GET'])
def query_tree():
    if not request.args or 'id' not in request.args:
        response = ({"success": False, "msg": "没有指定id", "errorCode": 720002})
        return cors_response(response)
    else:
        id = request.args['id']
        treetask_all = Tree_Task.query.filter_by(parent_id=id).order_by(Tree_Task.tree_order).all()
        treetask_forms = []
        if(treetask_all):
            for i in range(len(treetask_all)):
                treetask_form = {
                    "id": treetask_all[i].tree_id,
                    "name": treetask_all[i].tree_name,
                    "pId": treetask_all[i].parent_id,
                    "dropInner": treetask_all[i].tree_type,
                    "treeOrder": treetask_all[i].tree_order,
                }
                treetask_forms.append(treetask_form)
                if treetask_forms:
                    response = ({"success": True, "msg": "OK", "errorCode": 720001, "data": treetask_forms})
                    response = cors_response(response)
                else:
                    response = ({"success": True, "msg": "该目录下无用例", "errorCode": 720002, "data": treetask_forms})
                    response = cors_response(response)
        else:
            response = cors_response(
                ({"success": True, "msg": "该目录下无用例", "errorCode": 720001, "data": treetask_forms}))
        # db.session.remove()
        return response


@interface.route('/dragTree', methods=['POST'])
def drag_tree():
    # 获取入参
    # 拖拽节点Id ---tree_id
    dragid = request.get_json().get('dragId')
    # 释放位置节点id
    dropid = request.get_json().get('dropId')
    # 放置位置
    position = request.get_json().get('position')

    try:

        if (dragid in ('',null) or dropid in ('',null) or position in ('',null)):
                return cors_response({"success": False, "msg": "参数必填", "errorCode": 720002})
        else:
            # 放入里面---即成为该节点的子节点
            if (position == 1 or position == '1'):
                #如果dropid是个用例--即tree_type 为0,则返回提示"用例不能成为父目录"
                # 查询释放位置节点的tree_type
                drop_info = Tree_Task.query.filter_by(tree_id=dropid).first()
                drop_type = drop_info.tree_type
                if(drop_type==0 or drop_type=='0'):
                    return cors_response({"success":False,"msg":"用例不能成为父目录"})
                # 查到释放位置节点下的tree_order最大的节点
                drag_order = db.session.query(Tree_Task.tree_order).filter_by(
                    parent_id=dropid).order_by(Tree_Task.tree_order.desc()).first()

                # ordermax = Tree_Task.query.filter_by(parent_id = dropid).order_by(Tree_Task.tree_order.desc()).first().tree_order
                if(drag_order == None or len(drag_order)==0):
                    ordermax=0
                else:
                    ordermax=drag_order[0]
                # 新增节点的tree_order在treeorder上加1
                treeorder = ordermax + 1
                # 更改拖拽节点信息
                # 1.tree_order 取treeorder
                # 2.parent_id更改为dropid
                #加锁
                Tree_Task.query.filter_by(tree_id = dragid).with_lockmode('update')
                #更新
                Tree_Task.query.filter_by(tree_id = dragid).update({'tree_order': treeorder, 'parent_id': dropid})


                #发现问题：
                #用例拖到用例的下面，没有下拉点击按钮，只有把用例改成文件夹才可以点击查询

            # 放入下面
            elif (position == 2 or position == '2'):

                # 查询释放位置节点的父节点 && tree_order
                drop_info = Tree_Task.query.filter_by(tree_id=dropid).first()
                parentid = drop_info.parent_id
                drop_treeorder = drop_info.tree_order

                # 查询释放位置节点下的其他节点的tree_id,tree_order---是个list
                treeorders = db.session.query(Tree_Task.tree_id, Tree_Task.tree_order).filter(
                    and_(Tree_Task.parent_id == parentid, Tree_Task.tree_order > drop_treeorder)).all()
                tree_order_list = [(row.tree_id, row.tree_order) for row in treeorders]

                for i in tree_order_list:
                    #锁表
                    Tree_Task.query.filter_by(tree_id = i[0]).with_lockmode('update')
                    # 根据当前的tree_id查询出来，然后更新当前节点的tree_order+1
                    Tree_Task.query.filter_by(tree_id = i[0]).update({'tree_order': i[1] + 1})
                #更新拖拽节点的tree_order
                #锁表
                Tree_Task.query.filter_by(tree_id = dragid).with_lockmode('update')
                #更新
                Tree_Task.query.filter_by(tree_id =dragid).update({'tree_order':  drop_treeorder+ 1,'parent_id': parentid})

            # 放入上面
            elif(position == 0 or position == '0'):
                # 查询释放位置节点的父节点 && tree_order
                drop_info=Tree_Task.query.filter_by(tree_id=dropid).first()
                parentid = drop_info.parent_id
                drop_treeorder =drop_info.tree_order

                # 查询释放位置节点下的其他节点的tree_id,tree_order---是个list
                treeorders = db.session.query(Tree_Task.tree_id, Tree_Task.tree_order).filter(
                    and_(Tree_Task.parent_id == parentid, Tree_Task.tree_order >= drop_treeorder)).all()
                tree_order_list = [(row.tree_id, row.tree_order) for row in treeorders]

                for i in tree_order_list:
                    # 锁表
                    Tree_Task.query.filter_by(tree_id=i[0]).with_lockmode('update')
                    # 根据当前的tree_id查询出来，然后更新当前节点的tree_order+1
                    Tree_Task.query.filter_by(tree_id=i[0]).update({'tree_order': i[1] + 1})
                # 更新拖拽节点的tree_order
                # 锁表
                Tree_Task.query.filter_by(tree_id=dragid).with_lockmode('update')
                # 更新
                Tree_Task.query.filter_by(tree_id=dragid).update(
                    {'tree_order': drop_treeorder, 'parent_id': parentid})
    except  Exception as e:
        print(e)
        response = {"success": False, "msg": "方法异常", "errorCode": 720001 }
        return cors_response(response)

    try:
        db.session.commit()
        response = cors_response({"success": True, "msg": "OK", "errorCode": 720000})

        # 层级表修改数据
        pids = queryallpid(dragid)
        Case_Level.query.filter_by(case_id =dragid).update({'levels':str(pids)})
        db.session.commit()

    except:
        db.session.rollback()
        response = {"success": False, "msg": "数据库操作失败", "errorCode": 720002, }
        response = cors_response(response)

    return response



@interface.route('/deleteTree', methods=['POST'])
def delete_tree():
    if not request.get_json() or 'id' not in request.get_json():
        response = ({"success": False, "msg": "未指定id", "errorCode": 720002})
        return cors_response(response)
    else:
        list = []
        # id = request.form['id']
        id = request.get_json().get('id')
        try:
            # Tree_Task.query.filter_by(tree_id=id ).delete()
            # Tree_Task.query.filter_by(parent_id=id).delete()
            count = Tree_Task.query.filter(or_(Tree_Task.parent_id == id, Tree_Task.tree_id == id)).count()
            if count > 0:
                # Tree_Task.query.filter(or_(Tree_Task.parent_id == id, Tree_Task.tree_id == id)).delete()
                "需要同步删除用例表中，对应的treeid,treeid 获取来自 tree_task表中，parentid=id的所有treeid "
                # test1 = db.session.query(Tree_Task.tree_id).filter(or_(Tree_Task.parent_id == id, Tree_Task.tree_id == id)).all()

                treeid_all = Tree_Task.query.filter(
                    or_(Tree_Task.parent_id == id, Tree_Task.tree_id == id)).all()
                for i in range(len(treeid_all)):
                    list.append(treeid_all[i].tree_id)

                Tree_Task.query.filter(or_(Tree_Task.parent_id == id, Tree_Task.tree_id == id)).delete()
                Interface_Mall.query.filter(Interface_Mall.tree_id.in_(list)).delete(synchronize_session='fetch')

                #删除层级表中对应数据
                Case_Level.query.filter(Case_Level.case_id.in_(list)).delete(synchronize_session='fetch')

                db.session.commit()
                response = ({"success": True, "msg": "ok", "errorCode": 720001, "data": count})
            else:
                response = ({"success": False, "msg": "无删除的指定id", "errorCode": 720001, "data": count})
        except:
            db.session.rollback()
            raise
            response = {"success": False, "msg": "数据库操作失败", "errorCode": 720003, }
            # response = cors_response(response)
        return cors_response(response)

@interface.route('/modifyTree', methods=['POST'])
def modify_tree():
    if not request.get_json() or 'id' not in request.get_json():
        response = {"success": False, "msg": "未指定id", "errorCode": 720002}
        return cors_response(response)
    else:
        id = request.get_json().get('id')
        name = request.get_json().get('name')
        try:
            Tree_Task.query.filter(Tree_Task.tree_id == id).update({Tree_Task.tree_name: name})
            # 同步修改用例表名称
            Interface_Mall.query.filter(Interface_Mall.tree_id == id).update({Interface_Mall.name: name})
            db.session.commit()
            response = {"success": True, "msg": "ok", "errorCode": 720001, "data": 1}
        except:
            db.session.rollback()
            raise
            response = {"success": False, "msg": "数据库操作失败", "errorCode": 720003}
        return cors_response(response)

#查出节点下的所有父节点
@interface.route('/queryPid',methods=['GET'])
def querypid():
    id = request.args['id']
    try:
        if(id==''):
            response = {"success": False, "msg": "节点id不能为空", "errorCode": 720003}
        else:
            r_list=[]
            pids = db.session.query(Tree_Task.tree_id).filter(
                and_(Tree_Task.parent_id == id, Tree_Task.tree_type == 1)).all()
            pid_list = [(row.tree_id) for row in pids]
            #查询勾选节点下所有的父节点
            pid=query(pid_list,r_list)
            id=int(id)
            all_pid=[id]+pid_list+pid
            #两层list嵌套取出
            new_all_pid=list(newlist(all_pid))
            response = {"success": True,"data":new_all_pid}
    except:
        response = {"success": False, "msg": "查询失败", "errorCode": 720003}

    return cors_response(response)


#批量运行（已废弃）
@interface.route('/batchRunCases',methods=['POST'])
def batchruncases():
    err_list=[]
    getparmsvalue = GetParmsValue()
    if not request.get_json() or 'caseids' not in request.get_json():
        response = {"success": False, "msg": "请检查参数", "errorCode": 720002}
        return cors_response(response)
    else:
        caseids=request.get_json().get('caseids')
        env=request.get_json().get('env')
        #运行标记
        report_count=  Report.query.filter_by().count()
        if(report_count !=0):
            report_one = Report.query.filter_by().order_by(Report.count.desc()).first()
            run_count=report_one.count+1
        else:
            run_count=1
        if(caseids==[]):
            response = {"success": False, "msg": "用例必选", "errorCode": 720002}
        elif(env==''):
            response={"success": False, "msg": "环境必选", "errorCode": 720002}
        else:
            response = {"success": True, "msg": env+"环境下无可运行用例信息", "data": err_list}
            for id in caseids:
                count=Interface_Mall.query.filter(and_(Interface_Mall.tree_id == id, Interface_Mall.env == env,Interface_Mall.rest !=None)).count()
                print('count:',count)
                if(count !=0):
                    case_info = Interface_Mall.query.filter(
                        and_(Interface_Mall.tree_id == id, Interface_Mall.env == env)).first()

                    interface = batchRequest()
                    # 获取入参
                    env = case_info.env
                    requestmethod = case_info.request

                    #string转成list

                    headers=json.loads(case_info.headers)


                    url = case_info.rest
                    inputparam = case_info.data
                    # 全局变量信息
                    globalvar=json.loads(case_info.global_var)

                    # 校验字段信息
                    assertInfo=json.loads(case_info.assert_info)

                    # 获取块信息
                    expectedcontent = case_info.expected_response

                    ##dff: 20190625 获取d参数
                    dParam = case_info.dParam

                    # 处理请求头
                    flag = True
                    dict = {}
                    for i in range(len(headers)):
                        if (headers[i]['key'] != '' or headers[i]['value'] != ''):
                            flag_assert = True
                            break
                        else:
                            flag = False
                    if (flag == True):
                        for i in range(len(headers)):
                            k = headers[i]['key']
                            v = headers[i]['value']
                            dict[k] = v
                        headers = str(dict)
                    else:
                        headers = ''

                    # assertInfo不为空数组的时候处理校验信息 格式 route;route       expected_response;expected_response
                    if (len(assertInfo) != 0):
                        # 路径
                        route = []
                        # 期望值
                        expeted_field = []

                        flag_assert = True
                        for i in range(len(assertInfo)):
                            if (assertInfo[i]['key'] != '' or assertInfo[i]['value'] != ''):
                                flag_assert = True
                                break
                            else:
                                flag_assert = False
                        if (flag_assert == True):
                            for i in range(len(assertInfo)):
                                k = assertInfo[i]['key']
                                v = assertInfo[i]['value']
                                if (k != '' or v != ''):
                                    route.append(k)
                                    expeted_field.append(v)
                            route = ';'.join(route)
                            expeted_field = ';'.join(expeted_field)
                        else:
                            route = ''
                            expeted_field = ''

                    # 当globalvar不为空的时候处理全局变量  name;name    route;route  格式
                    # 2.全局变量信息不为空
                    # 2.1全局变量都为空
                    if (len(globalvar) != 0):
                        # 路径
                        globalname = []
                        # 期望值
                        globalroute = []

                        flag_global = True
                        for i in range(len(globalvar)):
                            if (globalvar[i]['key'] != '' or globalvar[i]['value'] != ''):
                                flag_global = True
                                break
                            else:
                                flag_global = False
                        if (flag_global == True):
                            for i in range(len(globalvar)):
                                k = globalvar[i]['key']
                                v = globalvar[i]['value']
                                if (k != '' or v != ''):
                                    globalname.append(k)
                                    globalroute.append(v)
                            globalname = ';'.join(globalname)
                            globalroute = ';'.join(globalroute)
                        else:
                            globalname = ''
                            globalroute = ''


                    try:
                        if (requestmethod == 'get'):
                            # res = interface.getinterfaceone(url, inputparam, env, headers, dParam)
                            # response转成字典
                            # response = json.loads(response)
                            if (url not in ('', None) and url.startswith('http://') == False and url.startswith('https://') == False):
                                url = 'http://' + url
                            print(url)
                            response = interface.getinterfaceone(url, inputparam, env, headers, dParam)
                            # print(res)
                            #出参
                            res=response['res']
                            #运行时间
                            time=response['time']
                            #get/post运行结果
                            success=response['success']

                            if(globalname==[]  and globalroute==[]  and route==[]  and expeted_field==[]  and expectedcontent=='' ):
                                print('无需校验')

                            else:
                                checkOut = BatchCheck(env, res, globalname, globalroute, route, expeted_field,
                                                    expectedcontent)
                                result = checkOut.checkout()
                                if(result['success'] == False):
                                    err_list.append(id)

                        elif (requestmethod == 'post'):
                            # res = interface.postinterfaceone(url, inputparam, env, headers, dParam)
                            if ( url not in ('',None) and url.startswith('http://') == False and url.startswith('https://') == False):
                                url = 'http://' + url
                            print(url)
                            response = interface.postinterfaceone(url, inputparam, env, headers, dParam)
                            #出参
                            res=response['res']
                            #运行时间
                            time=response['time']
                            #get/post运行结果
                            success=response['success']

                            if (globalname  and globalroute==[]  and route==[]  and expeted_field==[]  and expectedcontent==''):
                                print('无需校验')

                            else:
                                checkOut = BatchCheck(env, res, globalname, globalroute, route, expeted_field, expectedcontent)
                                result = checkOut.checkout()
                                if (result['success'] == False):
                                    err_list.append(id)

                        else:
                            print('请求方式不正确')
                        #用例运行信息入库
                        # #运行和校验有一个失败就失败

                        if(success==False or result['success'] == False):
                            success=False
                        #入参
                        if(headers !=''):
                            if('{{' in headers):
                                headers = getparmsvalue.get_parms_value(headers, env)
                            if('{{' in inputparam):
                                inputparam=getparmsvalue.get_parms_value(inputparam, env)
                            inparams= headers +';'+inputparam
                        else:
                            if (inputparam !=None and '{{' in inputparam):
                                inputparam = getparmsvalue.get_parms_value(inputparam, env)
                            inparams = inputparam
                        # 最终校验结论整合
                        if(len(result['msg']) !=0):
                            if('{{' in result['msg'] ):
                                result['msg'] = getparmsvalue.get_parms_value(result['msg'], env)
                            bacth_checkout= (';\n').join(result['msg'][0:])
                        else:
                            bacth_checkout=''

                        #把参数中的参数化转换成真实数据再入库
                        if ('{{' in url ):
                            rest = getparmsvalue.get_parms_value(url, env)

                        report_info=Report(
                            case_id=id,
                            runtime=time,
                            result= success,
                            rest=url,
                            inparams=  inparams,
                            outparams=  res,
                            checkout= bacth_checkout,
                            count= run_count,
                        )
                        db.session.add(report_info)
                        db.session.commit()  
                        if (err_list):
                            response = {"success": True, "msg": "运行完成且标红为失败用例", "data": err_list}
                        else:
                            response = {"success": True, "msg": "运行完成","data":err_list}


                    except Exception as e:
                        print(e)
                        response = {"success": False, "msg": "方法异常"}
    return cors_response(response)

#报告列表
@interface.route('/queryReportList',methods=['POST'])
def  queryReportList():
    time=request.get_json().get('time')
    startTime_ = time[0]
    endTime_ = time[1]
    tag=request.get_json().get('tag')
    page=request.get_json().get('page')
    pageSize=request.get_json().get('pageSize')
    if(page in (None,'') or  pageSize in ('',None)):
        return jsonify({"success":False,"msg": "参数必传"})
    else:
        param = []
        dataList = []
        if(startTime_ not in ('',None)):
            startTime_beijing = dateutil.parser.parse(startTime_).astimezone(
                pytz.timezone('Asia/Shanghai'))  # 解析string 并转换为北京时区
            startTime = datetime.strftime(startTime_beijing, '%Y-%m-%d %H:%M:%S')  # 将datetime转换为string
            param.append(Jenkins_Case_Build.start_time >= startTime )
        if(endTime_ not in ('',None)):
            endTime_beijing = dateutil.parser.parse(endTime_).astimezone(
                pytz.timezone('Asia/Shanghai'))  # 解析string 并转换为北京时区
            endTime = datetime.strftime(endTime_beijing, '%Y-%m-%d %H:%M:%S')  # 将datetime转换为string
            param.append(Jenkins_Case_Build.end_time <= endTime)
        if(tag  not in ('',None)):
            param.append(Jenkins_Case_Build.tag.like("%" + tag + "%"))
        try:
            if(len(param)!=0):
                # report_counts = Jenkins_Case_Build.query.with_entities(Report.count).filter(*param).order_by(Report.count.desc()).group_by(Report.count).paginate(page=page, per_page=pageSize)
                report_counts = Jenkins_Case_Build.query.with_entities(Jenkins_Case_Build.report_num).filter(*param).order_by(Jenkins_Case_Build.id.desc()).paginate(page=page, per_page=pageSize)
            else:
                # report_counts = Report.query.with_entities(Report.count).order_by(Report.count.desc()).group_by(Report.count).paginate(page=page, per_page=pageSize)
                report_counts = Report.query.with_entities(Jenkins_Case_Build.report_num).order_by(Jenkins_Case_Build.id.desc()).paginate(page=page, per_page=pageSize)

            for  report_count in report_counts.items:
                report_info=Jenkins_Case_Build.query.filter(Jenkins_Case_Build.report_num==report_count.report_num).first()
                startTime=str(report_info.start_time)
                tag=report_info.tag
                if(tag ==None):
                    tag=report_info.env
                endTime=str(report_info.end_time)
                if(report_info.build_result==1):
                    result='成功'
                else:
                    result='失败'
                dataList.append({
                    "id":report_info.report_num,
                    "tag":tag,
                    'result':result,
                    "startTime":startTime,
                    "endTime":endTime
                })
            print(dataList)

        except Exception as e:
            print(e)
    return jsonify({"success":True,"msg":"OK","data":{"dataList":dataList,"page":page,"pageSize":pageSize,"count":report_counts.total,"totalPage":report_counts.pages}})

#查看报告信息
@interface.route('/getReportInfo',methods=['GET'])
@cache.cached(query_string=True,timeout=7200000000000000)
def getreportinfo():
    #获取批次id
    count_id=request.args['id']
    report_count = db.session.query(func.count(Report.count)).filter(Report.count == count_id).scalar()
    # report_count = db.session.query(Report.count).filter(Report.count == count_id).count()
    if(report_count ==0):
        response={'success':True,'data':None}
    else:
        # max_count_query=Report.query.filter_by().order_by(Report.count.desc()).first()
        # report_info=Report.query.filter_by(count=max_count_query.count).all()
        # report_info = Report.query.filter_by(count=count_id).all()
        # report_info_first=Report.query.filter_by(count=count_id).first()
        # report_info_end=Report.query.filter_by(count=count_id).order_by(Report.id.desc()).first()

        # 获取case_id
        report_info = db.session.query(distinct(Report.case_id)).filter(Report.count==count_id).all()
        #获取创建时间
        report_info_first=db.session.query(Report.create_time).filter(Report.count==count_id).first()
        report_info_end=db.session.query(Report.create_time).filter(Report.count==count_id).order_by(Report.id.desc()).first()
        # report_info = db.session.query(Report.case_id,Tree_Task.tree_name,Report.runtime,Report.result,Report.rest,Report.inparams,
        #                                Report.outparams,Report.checkout).outerjoin(Tree_Task,Tree_Task.tree_id == Report.case_id)\
        #                                 .filter(Report.count == 12).order_by(Report.count.desc()).all()
        all_pid=[]
        p_list=[]
        #所有运行节点及其所有父节点list

        print(report_info)
        for i in range(len(report_info)):
            all_pid = db.session.query(Case_Level.levels).filter(Case_Level.case_id==report_info[i][0])
            print(all_pid,report_info[i][0])
            all_pid_list=eval(all_pid[0][0])
            all_pid_list.append(report_info[i][0])
            p_list += all_pid_list

        # for i in range(len(report_info)):
        #     all_pid = queryallpid(report_info[i][0])
        #     all_pid.append(report_info[i][0])
        #     p_list += all_pid

        p_list=list(set(p_list))   #p_list = [0,1,2,8,11]
        out_json=[]
        #获取顶层id
        # head_tree_id=Tree_Task.query.filter_by(parent_id=0).first()
        head_tree_id=db.session.query(Tree_Task.tree_id,Tree_Task.tree_name).filter(Tree_Task.parent_id==0).first()
        #根据获取的展示出真实的信息
        out_info=db.session.query(Tree_Task.tree_id,Tree_Task.tree_name,Tree_Task.tree_type).filter(Tree_Task.parent_id==head_tree_id[0]).order_by(Tree_Task.tree_order).all()
        for id in ([(row.tree_id,int(row.tree_type),row.tree_name) for row in out_info]):
            if(id[0] in p_list):
                # tree_type 为目录
                if(id[1]==1):
                    sec_json={'type':'suite','id':id[0],'name':id[2],'child':[],'runtime':None,'result':None,'rest':'',"num":None}
                    three_json=querychilddict(id[0],p_list,count_id)
                    sec_json['child']=three_json
                    out_json.append(sec_json)
                elif (id[1]==0):
                    # sec_info = Report.query.filter(and_(Report.case_id==id[0],Report.count==max_count_query.count)).first()
                    # 20190708-dff: 修改为查询该用例及运行count批次下所有的执行记录（参数化后一个用例可能被执行了多次）
                    sec_info = db.session.query(Report.result,Report.runtime,Report.rest,Report.id).filter(and_(Report.case_id==id[0],Report.count==id)).all()
                    # case_run_count = Report.query.filter(and_(Report.case_id==id[0],Report.count==id)).count()   #获取用例执行记录条数
                    case_run_count = db.session.query(func.count(Report.case_id)).filter(and_(Report.case_id==id[0],Report.count==id)).scalar()   #获取用例执行记录条数

                    if case_run_count > 1:   # dff： 只有当同一用例执行多次时才需要循环处理
                        case_count = 1 #dff 20190708
                        for sec_info_item in sec_info:
                            #result 1---成功，0---失败
                            if(sec_info_item[0] ==1):
                                result='success'
                            elif(sec_info_item[0] ==0):
                                result='fail'
                            sec_json = {'type': 'test', 'id': id[0], 'name': id[2]+'_'+str(case_count), 'child': [],"num":sec_info_item[3],
                                            'runtime': sec_info_item[1],
                                            'result': result, 'rest':sec_info_item[2]
                                           }
                            out_json.append(sec_json)
                    else:  # dff；同一用例无多条执行记录时，直接处理
                        if(sec_info[0][0] ==1):
                                result='success'
                        elif(sec_info[0][0] ==0):
                            result='fail'
                        sec_json = {'type': 'test', 'id': id[0], 'name': id[2], 'child': [],
                                            'runtime': sec_info[0][1],
                                            'result': result, 'rest':sec_info[0][2]
                                             }
                        out_json.append(sec_json)
        all_dict={'type':'suite','id':head_tree_id[0],'name':head_tree_id[1],"num":None,'child':out_json,'runtime':None,'result':None,'rest':''}
        starttime=str(report_info_first.create_time)
        endtime=str(report_info_end.create_time)
        response={'success':True,'starttime':starttime,'endtime':endtime,'data':all_dict}
    print('======================')
    print(response)
    return jsonify(response)

#查看报告的出入参以及校验
@interface.route('/queryParams',methods = ['GET'])
def  queryParams():
    #获取批次id
    count_id=request.args['id']
    #获取入参啊，出参，校验信息
    try:
        params=db.session.query(Report.case_id,Report.inparams,Report.outparams,Report.checkout).filter(Report.id==count_id).first()
        logging.info(params)
    except Exception as e:
        logging.error(e)
    return jsonify({"success":True,"msg":"OK","data":{"inparams":params[1],"outparams":params[2],"checkout":params[3]}})

# #查看报告的出入参以及校验
# @interface.route('/queryTest',methods = ['GET'])
# def  queryTest():
#     #获取批次id
#     count_id=request.args['id']
#     #获取入参啊，出参，校验信息
#     params=db.session.query(Report.case_id,Report.inparams,Report.outparams,Report.checkout).filter(Report.id==count_id).first()
#     return jsonify({"success":True,"msg":"OK","data":{"inparams":params[1],"outparams":params[2],"checkout":params[3]}})


@interface.route('/searchModules',methods = ['GET'])    #用来获取module_list表中模块列表信息的，暂时未用到
def searchModules():
    modules = db.session.query(Modules_list.module_name).distinct(Modules_list.module_name).all()
    # modules = Modules_list.query.from_statement(text("SELECT DISTINCT(module_name) FROM modules_list")).all()
    print(modules)
    modules_list = []
    if len(modules)>0:
        for module in modules:
            tmp_module = {}
            tmp_module['value'] = module[0]
            tmp_module['label'] = module[0]
            modules_list.append(tmp_module)
        response = {"success":True, "msg":"OK", "data": modules_list}
    else:
        response = {"success":False, "msg":"未查询到modules信息，请检查数据库配置", "data":null}
    print(modules_list)
    return cors_response(response)

# 根据modules_list表生成 tag数据
@interface.route('/insertTags', methods=['GET'])
def insert_tags():
    modules = db.session.query(Modules_list.module_name).distinct(Modules_list.module_name).all()
    print(modules)
    if len(modules)>0:
        count=0
        for module in modules:
            tags = [module[0].replace('_','-')+'-sit',module[0].replace('_','-')+'-pre',module[0].replace('_','-')+'-prd']
            for tag in tags:
                old_tag = TAG.query.filter(TAG.tag==tag).first()
                if old_tag is None:
                    new_tag = TAG(tag=tag,del_flag=0)
                    db.session.add(new_tag)
                    db.session.commit()
                    count+=1
                else:
                    print("%s 已经存在了！"%(tag))
        result = {'success':True,"msg":"tags入库成功，共入库%d条"%(count)}
    else:
        result = {'success':False,'msg':"未查询到modules，无需导入tag!"}
    return cors_response(result)


#批量参数化运行接口
@interface.route('/batchRunByParameter',methods=['GET','POST'])
def sync_BatchRun():
    # data = request.get_json('data')
    # print(data)
    if not request.get_json() or 'caseids' not in request.get_json():
        response = {"success": False, "msg": "请检查参数", "errorCode": 720002}
        # return cors_response(response)
    else:
        caseids=request.get_json().get('caseids')
        env=request.get_json().get('env')
        user=request.get_json().get('user')
        if(caseids==[]):
            response = {"success": False, "msg": "用例必选", "errorCode": 720002}
        elif(env==''):
            response={"success": False, "msg": "环境必选", "errorCode": 720002}
        else:
            executor.submit(batchRunByParameter,caseids,env,user)
            response = {"success": "true", "msg": "批量执行中，请稍后[自动化报告列表]界面查看~~","data":[]}
    # print("aa")
    # print(response)
    return cors_response(response)

def batchRunByParameter(caseids, env, user):
    logging.info('[start] 批量执行开始.....')
    err_list=[]
    case_total = 0
    case_failed = 0
    getparmsvalue = GetParmsValue()
    # if not request.get_json() or 'caseids' not in request.get_json():
    #     response = {"success": False, "msg": "请检查参数", "errorCode": 720002}
    #     return cors_response(response)
    # else:
    #     caseids=request.get_json().get('caseids')
    #     env=request.get_json().get('env')
    #     user=request.get_json().get('user')

        # #运行标记
    report_count=  Report.query.filter_by().count()
    if(report_count !=0):
        report_one = Report.query.filter_by().order_by(Report.count.desc()).first()
        run_count=report_one.count+1
    else:
        run_count=1
    if(caseids==[]):
        response = {"success": False, "msg": "用例必选", "errorCode": 720002}
    elif(env==''):
        response={"success": False, "msg": "环境必选", "errorCode": 720002}
    else:
        response = {"success": True, "msg": env+"环境下无可运行用例信息", "data": err_list}
        # 开始时间
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        for id in caseids:
            print('caseid:',id)
            count=Interface_Mall.query.filter(and_(Interface_Mall.tree_id == id, Interface_Mall.env == env,Interface_Mall.rest !=None)).count()
            if(count !=0):
                case_info = Interface_Mall.query.filter(
                    and_(Interface_Mall.tree_id == id, Interface_Mall.env == env)).first()

                # interface = batchRequest()
                interface = Parameter_Interface()  #使用参数化后方式处理
                # 获取入参
                env = case_info.env
                requestmethod = case_info.request

                #string转成list
                headers=json.loads(case_info.headers)

                #20190722-dff: 增加对接口类型rest\tsp分别处理
                requestType = case_info.request_type
                if requestType == 'tsp':
                    tsp_name = case_info.rest
                    tsp_interface = TspSearch(tsp_name,env)
                    tsp_interface = tsp_interface.tsp2interface()
                    print(tsp_interface)
                    if tsp_interface is None:
                        # err_list.append(id)   # 记录失败用例
                        url = tsp_name  # 如果未查询到tsp服务接口，则url直接获取为表中存储的tsp服务名，后续接口会执行失败处理
                    else:
                        tsp_interface=json.loads(tsp_interface)
                        print(tsp_interface["ip"], type(tsp_interface["ip"]))
                        print(tsp_interface["path"], type(tsp_interface["path"]))
                        url = "http://" + str(tsp_interface["ip"]) + tsp_interface["path"]
                else:
                    url = case_info.rest
                print("hhaaa:url, ",url)

                # dff-20191226 新增pepple的查询方法queryMethod获取
                queryMethod = case_info.queryMethod
                inputparam = case_info.data
                print('the inputparams  --- : ',inputparam)
                #20190727-dff: 增加入参是否需要base64编码处理逻辑
                isBase64Encode = case_info.isBase64Encode
                #dff-20191012 add:
                isBase64Decode = case_info.isBase64Decode
                # 全局变量信息
                globalvar=json.loads(case_info.global_var)

                # 校验字段信息
                assertInfo=json.loads(case_info.assert_info)

                # 获取块信息
                expectedcontent = case_info.expected_response

                ##dff: 20190625 获取d参数
                dParam = case_info.dParam

                #20190903dff: 获取预期正则校验信息,并将查询出的str转换成list
                if case_info.regex_checklist is None:
                    regex_checklist = [{"key": "", "value": ""}]
                else:
                    regex_checklist = json.loads(case_info.regex_checklist)
                # print('regex_checklist:',regex_checklist, type(regex_checklist))

                # 处理请求头
                flag = True
                dict = {}
                for i in range(len(headers)):
                    if (headers[i]['key'] != '' or headers[i]['value'] != ''):
                        # flag_assert = True
                        flag = True    #dff : 20190705 增加此行，将上面一行屏蔽
                        break
                    else:
                        flag = False
                if (flag == True):
                    for i in range(len(headers)):
                        k = headers[i]['key']
                        v = headers[i]['value']
                        dict[k] = v
                    headers = str(dict)
                else:
                    headers = ''

                # assertInfo不为空数组的时候处理校验信息 格式 route;route       expected_response;expected_response
                if (len(assertInfo) != 0):
                    # 路径
                    route = []
                    # 期望值
                    expeted_field = []
                    types=[]
                    flag_assert = True
                    for i in range(len(assertInfo)):
                        if (assertInfo[i]['key'] != '' or assertInfo[i]['value'] != ''):
                            flag_assert = True
                            break
                        else:
                            flag_assert = False
                    if (flag_assert == True):
                        for i in range(len(assertInfo)):
                            k = assertInfo[i]['key']
                            v = assertInfo[i]['value']
                            check_type = assertInfo[i]['checkType']
                            if (k != '' or v != ''):
                                route.append(k)
                                expeted_field.append(v)
                                types.append(check_type)

                        route = ';'.join(route)
                        expeted_field = ';'.join(expeted_field)
                        types = ';'.join(types)
                    else:
                        route = ''
                        expeted_field = ''
                        types = ''
                else:
                    route = ''
                    expeted_field = ''
                    types = ''


                # 当globalvar不为空的时候处理全局变量  name;name    route;route  格式
                # 2.全局变量信息不为空
                # 2.1全局变量都为空
                if (len(globalvar) != 0):
                    # 路径
                    globalname = []
                    # 期望值
                    globalroute = []

                    flag_global = True
                    for i in range(len(globalvar)):
                        if (globalvar[i]['key'] != '' or globalvar[i]['value'] != ''):
                            flag_global = True
                            break
                        else:
                            flag_global = False
                    if (flag_global == True):
                        for i in range(len(globalvar)):
                            k = globalvar[i]['key']
                            v = globalvar[i]['value']
                            if (k != '' or v != ''):
                                globalname.append(k)
                                globalroute.append(v)
                        globalname = ';'.join(globalname)
                        globalroute = ';'.join(globalroute)
                    else:
                        globalname = ''
                        globalroute = ''

                ## ******--------  20190904 dff: 处理regex_checklist信息 --*************
                if regex_checklist not in ('',None,[]) and regex_checklist != [{"key": "", "value": ""}]:
                    flag_regex = True
                    can_reCheck_list = []
                    # 获取校验字段值及正则表达式值都不为空的信息
                    for i in range(len(regex_checklist)):
                        if regex_checklist[i]['key']  in ('',None) or regex_checklist[i]['value']  in ('',None):
                            result = {'success': False,'msg':'存在正则校验字段或表达式值为空，无法进行校验，请检查！'}
                            flag_regex = False
                            break
                        else:
                            can_reCheck_list.append(regex_checklist[i])
                            flag_regex = True
                else:
                    flag_regex = False
                    can_reCheck_list = []
                # print('flag_regex:',flag_regex)
                # print('can_reCheck_list: ', can_reCheck_list)

                try:
                    if (url not in ('', None) and url.startswith('http://') == False and url.startswith(
                            'https://') == False and requestType != 'pepple'):
                        url = 'http://' + url
                    if (requestmethod in('get','GET') ):
                        response = interface.getinterfaceone(url, inputparam, env, headers, dParam, isBase64Encode, isBase64Decode)
                    elif (requestmethod in ('post', 'POST')):
                        response = interface.postinterfaceone(url, inputparam, env, headers, dParam, isBase64Encode,isBase64Decode)
                    elif (requestmethod in ('put','PUT')):
                        response = interface.putinterfaceone(url, inputparam, env, headers, dParam, isBase64Encode,isBase64Decode)
                    elif requestmethod == 'pepple':
                        response = InterfacePepple(env=env,serviceName=url,queryMethod=queryMethod,body=inputparam).peppleBatchRun()
                    else:
                        print('请求方式不正确')
                        reponse='请求方式不正确'
                    for response_item in response:
                        #记录执行用例总数
                        case_total+=1
                        #接口响应数据
                        if requestType == 'tsp':   #20190722-dff: tsp类型接口，对响应数据进行base64转码处理
                            # response = base64Decode(response)
                            res=base64Decode(response_item['res'])
                        else:
                            res = response_item['res']
                        #运行时间
                        run_time=response_item['time']
                        #get/post运行结果
                        success=response_item['success']
                        url = response_item['url']
                        data = response_item['data']

                        re_result = {'success':True, 'msg':''} # 先初始化批量正则校验结果
                        if(globalname==[]  and globalroute==[]  and route==[]  and expeted_field==[]  and expectedcontent=='' and flag_regex is False ):
                            print('无需校验')
                            bacth_checkout= ''   #20190705 dff新增，如果无校验信息，此字段默认为空
                        else:
                            bacth_checkout = '' # 20190904 dff: 先初始化批量处理结果信息
                            checkOut = BatchCheck(env, res, globalname, globalroute, route, expeted_field,types,expectedcontent,user)
                            result = checkOut.checkout()
                            ## 20190904 dff : 如果需要批量正则校验，则进行如下处理
                            if flag_regex and  len(can_reCheck_list) > 0:
                                check_error_list = []
                                check_succes_list =[]
                                # outparam = json.loads(outparam,encoding='utf-8')
                                for i in can_reCheck_list:
                                    checklist = re_string2list(i['key'])
                                    if checklist == []:
                                        tmp_dict = {}
                                        tmp_dict[i['key']] = '输入的正则校验字段格式有误'
                                        check_error_list.append(tmp_dict)
                                    else:
                                        # print('响应信息：',json.loads(res,encoding='utf-8'),type(json.loads(res,encoding='utf-8')))
                                        # print('正则检查字段：',checklist)
                                        # print('正则表达式',i['value'])
                                        re_result,result_msg = re_newCheck(checklist,json.loads(res,encoding='utf-8'),i['value'])
                                        if re_result is False or result_msg != []:
                                            tmp_dict = {}
                                            tmp_dict[i['key']] = result_msg  or '返回值正则校验失败'
                                            check_error_list.append(tmp_dict)
                                        else:
                                            tmp_dict = {}
                                            tmp_dict[i['key']] = '匹配正则[ %s ]校验成功~'%i['value']
                                            check_succes_list.append(tmp_dict)

                                if check_error_list == []:
                                    re_result = {'success': True, 'msg': '校验OK~~,'+ str(check_succes_list)}
                                elif check_succes_list != []:
                                    re_result = {'success': False, 'msg':  '校验OK~~,' + str(check_succes_list) + '\n校验失败~~, '+ str(check_error_list)}
                                else:
                                    re_result = {'success': False, 'msg':'校验失败~~, '+ str(check_error_list)}
                                bacth_checkout = bacth_checkout + re_result['msg']
                            # 将前3个校验结果与批量正则校验结果合并处理
                            if(result['success'] == False or re_result['success'] == False):
                                err_list.append(id)   # 记录失败用例id
                            if(len(result['msg']) !=0):
                                bacth_checkout= (';\n').join(result['msg'][0:]) + '\n' + bacth_checkout

                            # else:
                            #     bacth_checkout=''
                        if(success==False or result['success'] == False or re_result['success'] == False):
                            success=False
                            case_failed+=1  #记录失败用例数
                            #入参
                        if(headers !=''):
                            inparams= str(headers) +';'+str(data)
                        else:
                            inparams=data
                        # 最终校验结论整合

                        report_info=Report(
                            case_id=id,
                            runtime=run_time,
                            result= success,
                            rest=url,
                            inparams=  inparams,
                            outparams= res,
                            checkout= bacth_checkout,
                            count= run_count,
                        )
                        db.session.add(report_info)
                        db.session.commit()


                    # if (err_list):
                    #     response = {"success": True, "msg": "运行用例共：%d个；成功：%d；失败：%d, 标红为失败用例"%(case_total,case_total-case_failed,case_failed), "data": err_list}
                    # else:
                    #     response = {"success": True, "msg": "运行完成,共执行用例：%d个，全部成功！。"%case_total,"data":err_list}

                except Exception as e:
                    logging.error("方法异常: ",e)
                    response = {"success": False, "msg": "方法异常"}
            else:   # 未查询到对应环境下的用例信息时
                report_info=Report(
                            case_id=id,
                            runtime=0,
                            result= 0,
                            # rest=url,
                            # inparams=  inparams,
                            # outparams= res,
                            checkout= str(env) +"对应环境下无要运行的用例",
                            count= run_count,
                        )
                db.session.add(report_info)
                db.session.commit()
                err_list.append(id)
                case_total+=1
                case_failed+=1
            #汇总结果
            if (err_list):
                response = {"success": True, "msg": "运行用例共：%d个；成功：%d；失败：%d, 标红为失败用例"%(case_total,case_total-case_failed,case_failed), "data": err_list}
            else:
                response = {"success": True, "msg": "运行完成,共执行用例：%d个，全部成功！。"%case_total,"data":err_list}
        # 结束时间
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    logging.info('[end] 批量执行完成.....')
    try:
        if (case_failed==0):
            build_result=1
        else:
            build_result=0
        # 数据入jenkins_case_build 表
        build_case_info = Jenkins_Case_Build(
            report_num=run_count,
            env=env,
            build_result=build_result,
            success_case_count=case_total - case_failed,
            fail_case_count=case_failed,
            start_time=start_time,
            end_time=end_time
        )
        db.session.add(build_case_info)
        db.session.commit()
        print("恭喜你,入jenkins_case_build表成功~~")
    except Exception as e:
        print(e)
        print("呜呜呜,入jenkins_case_build表失败！！")

    return cors_response(response)


#查询全局变量列表
@interface.route('/queryGlobalParamsList',methods=['POST'])
def queryGlobalParamsList():
    env=request.get_json().get('env')
    key=request.get_json().get('key')
    value=request.get_json().get('value')
    page=request.get_json().get('page')
    pageSize=request.get_json().get('pageSize')
    user=request.get_json().get('user')
    if(page in (None,'') or  pageSize in ('',None)):
        return jsonify({"success":False,"msg": "参数必传"})
    else:
        # 拼接查询条件,支持模糊查询
        param = []
        if(env not in ('',None)):
            param.append(Parms_Enviroment.parms_env.like("%" + env + "%"))
        if(key not in ('',None)):
            param.append(Parms_Enviroment.parms_key.like("%" + key + "%"))
        if(value  not in ('',None)):
            param.append(Parms_Enviroment.parms_value.like("%" + value + "%"))
        if(user not in ('',None)):
            param.append(Parms_Enviroment.create_user.like("%" + user + "%"))
        try:
            if(len(param)!=0):
                params_list = Parms_Enviroment.query.filter(*param).order_by(Parms_Enviroment.create_time.desc()).paginate(page=page, per_page=pageSize)
            else:
                params_list = Parms_Enviroment.query.order_by(Parms_Enviroment.create_time.desc()).paginate(page=page, per_page=pageSize)
        except Exception as e:
            print(e)
            return jsonify({"success": False, "msg": "接口异常"})

        dataList=[]
        for globalparam in params_list.items:
            dataList.append({
                "id":globalparam.id,
                "key":globalparam.parms_key,
                "value":globalparam.parms_value,
                "createTime":str(globalparam.create_time),
                "user":globalparam.create_user,
                "env":globalparam.parms_env,
                "type":globalparam.parms_type
            })

        if(params_list.total ==0):
            page=0
        return jsonify({"success":True,"data":{"dataList":dataList,"count":params_list.total,"page":page,"pageSize":pageSize,"totalPage":params_list.pages}})

#新增、编辑保存全局变量信息
@interface.route('/saveGlobalParams',methods=['POST'])
def saveParams():
    paramKey = request.get_json().get('paramKey')
    paramValue = request.get_json().get('paramValue')
    paramEnvs = request.get_json().get('checkAllGroup')
    paramType = request.get_json().get('paramType') # 20191126新增变量类型字段
    print("环境信息：",paramEnvs,type(paramEnvs))
    user = request.get_json().get('user')
    addOrUpdate = request.get_json().get('addOrUpdate') # 获取新增或编辑标识，true:编辑；false: 新增
    err_env = ''
    succ_env = ''
    if len(paramEnvs) <=0:
        return cors_response({'success':False, 'msg': '请至少选择一个环境信息！'})
    else:
        if addOrUpdate is True: # 即界面进行的是编辑操作
            for paramEnv in paramEnvs:
                paramInfo = Parms_Enviroment.query.filter(and_(Parms_Enviroment.parms_key==paramKey,Parms_Enviroment.parms_env==paramEnv)).first()
                if paramInfo is not None:   # 对应环境记录在库里已存在，则 update 操作
                    try:
                        Parms_Enviroment.query.filter(and_(Parms_Enviroment.parms_key==paramKey,Parms_Enviroment.parms_env==paramEnv)).update(
                                {
                                    'parms_key': paramKey,
                                    'parms_value': paramValue,
                                    'parms_env': paramEnv,
                                    'create_user': user,
                                    'parms_type': paramType
                                }
                        )
                    except Exception as e:
                        logging.error(e)
                        err_env = err_env + paramEnv + ','
                        # result = False
                        # response = {'success': False, 'msg': '全局变量信息【更新】失败'}
                    else:
                        db.session.commit()
                        succ_env = succ_env + paramEnv + ','
                        # response = {'success': True, 'msg': '全局变量信息【更新】成功'}
                else:  # 对应环境记录在库里不存在，则 insert 操作
                    try:
                        new_param = Parms_Enviroment(parms_key=paramKey, parms_value=paramValue, parms_env=paramEnv,create_user=user,parms_type=paramType)
                        db.session.add(new_param)
                    except Exception as e:
                        logging.error(e)
                        err_env = err_env + paramEnv + ','
                    else:
                        db.session.commit()
                        succ_env = succ_env + paramEnv + ','
            if len(err_env)>1:
                response = {'success': False, 'msg':err_env + '环境下变量信息【更新】失败'}
            else:
                response = {'success': True, 'msg': succ_env + '环境下变量信息【更新】成功'}
        else:  # 界面进行的是新增逻辑
            can_insert = True
            exist_env = ''
            for paramEnv in paramEnvs:
                paramInfo = Parms_Enviroment.query.filter(and_(Parms_Enviroment.parms_key==paramKey,Parms_Enviroment.parms_env==paramEnv)).first()
                if paramInfo is not None:
                    can_insert = False
                    exist_env = exist_env + paramEnv +','
            if not can_insert: # 判断选择的环境下是否存在变量名,已存在则不再新增
                    return cors_response({'success': False, 'msg': '所选环境 [%s] 下已存在重复的变量名，请修改后提交!'%exist_env})
            else:
                for paramEnv in paramEnvs:
                    try:
                        params = Parms_Enviroment(parms_key=paramKey, parms_value=paramValue, parms_env=paramEnv,create_user=user,parms_type=paramType)
                        db.session.add(params)
                    except Exception as e:
                        logging.error(e)
                        err_env= err_env + paramEnv + ','
                    else:
                        db.session.commit()
                        succ_env = succ_env + paramEnv + ','
                if len(err_env)>1:
                    response = {'success': False, 'msg':err_env + '环境下变量信息【新增】失败'}
                else:
                    response = {'success': True, 'msg': succ_env + '环境下变量信息【新增】成功'}
    return  cors_response(response)


@interface.route('/base64Decode', methods=['GET', 'POST'])
def outparam_base64decode():
    origin_str = request.get_json().get('outparam')
    decode_str = base64Decode(origin_str)
    return cors_response({"success": True, "msg": "OK", "data": decode_str})

@interface.route('/deleteParam', methods=['POST'])
def delete_param():
    paramKey = request.get_json().get('paramKey')
    paramEnv = request.get_json().get('paramEnv')
    paramValue = request.get_json().get('paramValue')
    param_info = Parms_Enviroment.query.filter(and_(Parms_Enviroment.parms_key==paramKey,Parms_Enviroment.parms_env==paramEnv,Parms_Enviroment.parms_value==paramValue)).first()
    if param_info is None:
        response = {"success": False, "msg": "未查询到要删除的记录！"}
    else:
        try:
            db.session.delete(param_info)
        except Exception as e:
            logging.error(e)
            response = {'success': False, 'msg': '删除失败'}
        else:
            db.session.commit()
            response = {'success': True, 'msg': '删除成功'}
    return cors_response(response)



#新增校验类型，刷数据
@interface.route('/updateAssertInfo',methods=['GET'])
def update_assert_info():
    #查询用例表，过滤出assertInfo字段，进行解析，新增checType字段
    all_info = Interface_Mall.query.filter(Interface_Mall.assert_info !=None).all()
    for info in all_info:
        assert_info_new=json.loads(info.assert_info)
        for one in assert_info_new:
            print(one)
            if(not  "checkType" in one):
                one['checkType']='equal'
                # 更新
        print(info.id,'*******',assert_info_new)
        Interface_Mall.query.filter(Interface_Mall.id ==info.id).update({
            'assert_info': json.dumps(assert_info_new),
        })
        db.session.commit()
    return jsonify({"success":True})

@interface.route('/getTspIP', methods=['GET'])
def getTspIP():
    name = request.args.get('name')
    env = request.args.get('env')
    tsp = TspSearch(name,env)
    result = tsp.tsp2interface()
    print(result, '\n', type(result))
    return result

@interface.route('/queryRunDetail',methods=['GET'])
def query_run_detail():
    # 获取查询组名
    if("groupName" in request.args):
        group_name = request.args['groupName'].strip('"')
        try:
            if(group_name =="全部"):
                run_detail_info=db.session.query(Jenkins_Case_Build.week,Jenkins_Case_Build.env,func.count(Jenkins_Case_Build.build_result),func.sum(Jenkins_Case_Build.build_result),func.sum(Jenkins_Case_Build.success_case_count),func.sum(Jenkins_Case_Build.fail_case_count))\
                    .filter(Jenkins_Case_Build.week !='')\
                    .group_by(Jenkins_Case_Build.week,Jenkins_Case_Build.env).order_by(Jenkins_Case_Build.week,Jenkins_Case_Build.env.desc()).all()
            else:
                run_detail_info=db.session.query(Jenkins_Case_Build.week,Jenkins_Case_Build.env,func.count(Jenkins_Case_Build.build_result),func.sum(Jenkins_Case_Build.build_result),func.sum(Jenkins_Case_Build.success_case_count),func.sum(Jenkins_Case_Build.fail_case_count))\
                    .filter(and_(Jenkins_Case_Build.group_name==group_name,Jenkins_Case_Build.week !=''))\
                    .group_by(Jenkins_Case_Build.week,Jenkins_Case_Build.env).order_by(Jenkins_Case_Build.week,Jenkins_Case_Build.env.desc()).all()
            data={}
            if(len(run_detail_info)!=0):
                for detail in run_detail_info:
                    if(detail[0] not in data.keys() ):
                        data[detail[0]]={"week":detail[0],"list":[]}
                    data[detail[0]]['list'].append({"env":detail[1],"successBuildCount":detail[3],"failBuildCount":int(detail[2]-detail[3]),"successCaseCount":detail[4],"failCaseCount":detail[5]})
                return jsonify({"success":True,"msg":"OK","groupName":group_name,"data":data})
            else:
                 return jsonify({"success":True,"msg":"OK","groupName":group_name,"data":data})
        except:
            return  jsonify({"success":False,"msg":"查询失败","groupName":group_name,"data":{}})
    else:
          return  jsonify({"success":False,"msg":"参数必传","data":{}})


@interface.route("/getSysParamsList", methods = ['GET'])
def getSysParamsList():
    sysparamslist = []
    count = SysParams.query.filter(SysParams.sys_paramstatus == True).count()
    if count > 0:
        getSysParamsList = SysParams.query.filter(SysParams.sys_paramstatus == True).all()
        for i in getSysParamsList:
            print("系统变量列表：",i.sys_paramname)
            sysparamslist.append({'value':i.sys_paramname,'label': i.sys_paramname})
        response = {'success': True, 'msg': 'OK', 'data': sysparamslist}
    else:
        response = {'success': False, 'msg': '未查询到可用的系统变量', 'data':[]}
    return cors_response(response)

@interface.route("/queryMethods", methods = ['GET'])
def queryMethods():
    #获取get请求url中参数值，使用request.args.get()
    serviceName = request.args.get("serviceName")
    # serviceName = "com.tuniu.fab.spi.service.CustSerachService"
    pepple = InterfacePepple(serviceName=serviceName)
    data = pepple.getPeppleMethod()
    methodList = []
    if data != None:
        if len(data["list"]) > 0:
            for i in data["list"]:
                methodList.append({"name":i["name"],"desc":i["desc"]})
            response = {"success":True,"msg": "方法获取成功", "data":methodList}
        else:
            response = {"success":False,"msg": "未获取到可查询的方法", "data":[]}
    else:
        response = {"success":False,"msg": "获取查询方法失败", "data":[]}
    return cors_response(response)

@interface.route("/queryPeppleParams", methods = ['GET'])
def queryPeppleParams():
    queryMethod = request.args.get("queryMethod")
    # serviceName = "com.tuniu.fab.spi.service.CustSerachService"
    # queryMethod = "queryCustByIdBatch"
    serviceName = request.args.get("serviceName")
    pepple = InterfacePepple(serviceName=serviceName)
    data = pepple.getPeppleParams(queryMethod)
    if data != None:
        if "requestVO" in data.keys():
            if data["requestVO"] not in ('',null):
                response = {"success":True,"msg": "请求入参获取成功", "data":data}
            else:
                response = {"success":False,"msg": "请求入参获取为空，请自行填写", "data":''}
        else:
            response = {"success":False,"msg": "请求入参获取为空，请自行填写", "data":''}
    else:
        response = {"success":False,"msg": "请求入参获取失败，请自行填写", "data":''}
    return cors_response(response)

