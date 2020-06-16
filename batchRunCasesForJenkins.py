# -*- coding: utf-8 -*-
# TIME:         2:20 PM
# Author:       xutaolin

import sys
import time
from app.actions.interfaceAuto.GetParmsValue import GetParmsValue
from app.models.models import *
from app.actions.interfaceAuto.batchcheck import BatchCheck
from app.actions.interfaceAuto.interface_parameter import Parameter_Interface
from app.actions.interfaceAuto.interface_tsp import *
from sqlalchemy import and_
from app.actions.interfaceAuto.interface_pepple import *


tag=sys.argv[1]
if(len(sys.argv)>2):
    ding_url=sys.argv[2]
# tag="mall-booking-sit"
print(tag)



def batchRunCaseForJenkins(tag):
    err_list = []
    case_total = 0
    case_failed = 0
    user="系统"
    getparmsvalue = GetParmsValue()

    #联表查询,查询出所有需要运行的用例,并按照用例树结构顺序排序
    # all_run_cases=db.session.query(Interface_Mall.name,Interface_Mall.request,Interface_Mall.rest,Interface_Mall.request_type,
    #                                Interface_Mall.data,Interface_Mall.headers,Interface_Mall.expected_response,Interface_Mall.assert_info,
    #                                Interface_Mall.global_var,Interface_Mall.tree_id,Interface_Mall.env,Interface_Mall.dParam,Interface_Mall.isBase64Encode)\
    #                       .outerjoin(Tree_Task,Tree_Task.tree_id==Interface_Mall.tree_id).filter(Interface_Mall.tag==tag).order_by(Tree_Task.parent_id,Tree_Task.tree_order).all()

    all_run_cases = db.session.query(Interface_Mall).outerjoin(Tree_Task, Tree_Task.tree_id == Interface_Mall.tree_id).filter(Interface_Mall.tag == tag).order_by(
        Tree_Task.parent_id, Tree_Task.tree_order).all()
    print(all_run_cases)

    #根据标签设置env
    if ('sit' in tag[0].lower()):
        env = 'sit'
    elif ('pre' in tag[0].lower()):
        env = 'pre'
    elif ('prd' in tag[0].lower()):
        env = 'prd'
    else:
        env = ''
    #报告 (入库count)
    report_count = Report.query.filter_by().count()
    if (report_count != 0):
        report_one = Report.query.filter_by().order_by(Report.count.desc()).first()
        run_count = report_one.count + 1
    else:
        run_count = 1

    #run_count 入表，占位（防止因为未及时入表被抢用）
    report_count_pre = Report(case_id=0,count=run_count)
    db.session.add(report_count_pre)
    db.session.flush()

    #循环执行用例

    #开始时间
    start_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    for case_info in all_run_cases:
        interface = Parameter_Interface()  # 使用参数化后方式处理

        # 获取入参
        env = case_info.env
        requestmethod = case_info.request
        id=case_info.tree_id

        queryMethod = case_info.queryMethod

        # string转成list
        headers = json.loads(case_info.headers)

        # 增加对接口类型rest\tsp分别处理
        requestType = case_info.request_type
        if requestType == 'tsp':
            tsp_name = case_info.rest
            tsp_interface = TspSearch(tsp_name, env)
            tsp_interface = tsp_interface.tsp2interface()
            print(tsp_interface)
            if tsp_interface is None:
                url = tsp_name  # 如果未查询到tsp服务接口，则url直接获取为表中存储的tsp服务名，后续接口会执行失败处理
            else:
                tsp_interface = json.loads(tsp_interface)
                print(tsp_interface["ip"], type(tsp_interface["ip"]))
                print(tsp_interface["path"], type(tsp_interface["path"]))
                url = "http://" + str(tsp_interface["ip"]) + tsp_interface["path"]
        else:
            url = case_info.rest

        url = url.strip()
        inputparam = case_info.data

        # 增加入参是否需要base64编码处理逻辑
        isBase64Encode = case_info.isBase64Encode
        #dff 20191017:增加出参是否需要base64解码处理
        isBase64Decode = case_info.isBase64Decode
        # 全局变量信息
        globalvar = json.loads(case_info.global_var)

        # 校验字段信息
        assertInfo = json.loads(case_info.assert_info)

        # 获取块信息
        expectedcontent = case_info.expected_response

        #获取d参数
        dParam = case_info.dParam

        # 处理请求头
        flag = True
        dict = {}
        for i in range(len(headers)):
            if (headers[i]['key'] != '' or headers[i]['value'] != ''):
                # flag_assert = True
                flag = True  # dff : 20190705 增加此行，将上面一行屏蔽
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
            types = []

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

        try:
            if (url not in ('', None) and url.startswith('http://') == False and url.startswith(
                    'https://') == False and requestType != 'pepple'):
                url = 'http://' + url

            if (requestmethod in ('get', 'GET')):
                response = interface.getinterfaceone(url, inputparam, env, headers, dParam, isBase64Encode, isBase64Decode)
                print(response)
            elif (requestmethod in ('post', 'POST')):
                response = interface.postinterfaceone(url, inputparam, env, headers, dParam, isBase64Encode, isBase64Decode)
                print(response)
            elif (requestmethod in ('put', 'PUT')):
                response = interface.putinterfaceone(url, inputparam, env, headers, dParam, isBase64Encode, isBase64Decode)
                print(response)
            elif (requestmethod == 'pepple'):
                response = InterfacePepple(env,url,queryMethod,inputparam).peppleBatchRun()
                print(response)
            if(requestmethod in ('get', 'GET','post', 'POST','put', 'PUT', 'pepple')):
                for response_item in response:
                    # 记录执行用例总数
                    case_total += 1
                    # 接口响应数据
                    if requestType == 'tsp':  # 20190722-dff: tsp类型接口，对响应数据进行base64转码处理
                        # response = base64Decode(response)
                        res = base64Decode(response_item['res'])
                    else:
                        res = response_item['res']
                    # 运行时间
                    run_time = response_item['time']
                    # get/post运行结果
                    success = response_item['success']
                    url = response_item['url']
                    data = response_item['data']

                    if ( globalname == [] and globalroute == [] and route == [] and expeted_field == [] and expectedcontent == ''):
                        print('无需校验')
                        bacth_checkout = ''  # 20190705 dff新增，如果无校验信息，此字段默认为空
                    else:
                        checkOut = BatchCheck(env, res, globalname, globalroute, route, expeted_field, types,expectedcontent,
                                              user)
                        result = checkOut.checkout()
                        if (result['success'] == False):
                            err_list.append(id)  # 记录失败用例id
                        if (len(result['msg']) != 0):
                            bacth_checkout = (';\n').join(result['msg'][0:])
                        else:
                            bacth_checkout = ''
                    if (success == False or result['success'] == False):
                        success = False
                        case_failed += 1  # 记录失败用例数
                        print("到此失败个数为："+str(case_failed))
                        # 入参
                    if (headers != ''):
                        inparams = headers + ';' + str(data)
                    else:
                        inparams = data
                    # 最终校验结论整合

                    report_info = Report(
                        case_id=id,
                        runtime=run_time,
                        result=success,
                        rest=url,
                        inparams=inparams,
                        outparams=str(res),
                        checkout=bacth_checkout,
                        count=run_count,
                        tag=tag,
                    )
                    db.session.add(report_info)
                    db.session.commit()
            else:
                print('请求方式不正确')

        except Exception as e:
            print('ERROR:'+ str(e))

        if (err_list):
            print("运行用例共：%d个；成功：%d；失败：%d" % (case_total, case_total - case_failed, case_failed))
        else:
            print("运行完成,共执行了用例：%d个。" % case_total)
    #结束时间
    end_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    #成功率
    Success=round((case_total - case_failed)/case_total,2) *100
    # 删除占位记录
    report_pre_delete = Report.query.filter(
        and_(Report.count == run_count, Report.case_id == 0, )).first()
    db.session.delete(report_pre_delete)
    # 这里是传送的消息
    header = {"Content-Type": "application/json", "charset": "utf-8"}
    data = {"msgtype": "link", "link": {
        "text": ">>成功率:" + str(Success) + "% ,用例总数:" + str(case_total) + "\n" + ">>成功数:" + str(case_total - case_failed )+ ",失败数:" + str(case_failed) + "\n" + ">>查看更多...",
        "title": "Automatic(" + tag + ")\n",
        "picUrl": "http://m.tuniucdn.com/fb2/t1/G5/M00/A1/8B/Cii-slq7dASIL3m5AAB17eM2eHsAAE2fgPygjoAAHYF06_w400_h300_c1_t0.jpeg",
        "messageUrl": "http://pandora.tuniu.org/automation/report/"+str(run_count)}}
    message_json = json.dumps(data)
    if(case_failed ==0):
        build_result=1
        webhook = "https://oapi.dingtalk.com/robot/send?access_token=9d28e85a48392be9cc2fb1579c7e213f6db1d0810d1efe0c7bf13d4456763acf"
    else:
        build_result = 0
        webhook=ding_url
    # 发送钉钉信息
    msg = requests.post(url=webhook, data=message_json, headers=header)
    # 打印返回值
    print(msg.text)
    try:
        module_name=tag[:tag.rfind('-')].replace('-','_')
        group_info = db.session.query(Modules_list.systemChinese).filter(Modules_list.module_name == module_name).first()
        # 组name：例如 订单
        group_name=group_info[0]
        #第几周
        week_for_year=datetime.datetime.now().isocalendar()
        week=week_for_year[1]-44
        #数据入jenkins_case_build 表
        build_case_info=Jenkins_Case_Build(
            group_name=group_name,
            report_num=run_count,
            tag=tag,
            env=env,
            build_result=build_result,
            success_case_count=case_total - case_failed,
            fail_case_count=case_failed,
            start_time=start_time,
            end_time=end_time,
            week=week
        )
        db.session.add(build_case_info)
        db.session.commit()
        print("恭喜你,入jenkins_case_build表成功~~")
    except Exception as e:
        print(e)
        print("呜呜呜,入jenkins_case_build表失败！！")



if __name__ == '__main__':
    batchRunCaseForJenkins(tag)
    # batchRunCaseForJenkins("mob-tour-prd")
    # batchRunCaseForJenkins("tks-fuhsi-sit")

