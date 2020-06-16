# coding:utf-8
from __future__ import unicode_literals
from robot.libraries.BuiltIn import _Verify
import HttpLibrary
from app.actions.interfaceAuto.GetParmsValue import GetParmsValue
import  re



class CheckOut():
    def __init__(self, env, outparam, globalname, globalroute, route, expeted_field,types, expectedcontent,user):

        self.env = env
        self.actual_response = outparam
        self.global_name = globalname
        self.global_route = globalroute
        self.route = route
        self.expected_field = expeted_field
        self.expected_response = expectedcontent
        self.types=types
        self.user=user

    def getmyvalue(self, response, route):
        try:
            data = HttpLibrary.HTTP()
            value = data.get_json_value(response, route)
        except Exception as e:
            print(e)
        return value

    def checkout(self):
        glabalvalue = GetParmsValue()
        verify = _Verify()

        # 全局变量校验并入库（如果校验的时候不进行入库，那么在保存的时候有要去重新查一下全局路径对应的全局字段值）
        if (len(self.global_route) != 0):
            print(self.global_route)
            res = glabalvalue.get_parms_value_from_key(self.global_route, self.global_name, self.env,
                                                       self.actual_response,self.user)
            if (res['success'] == False):
                return res
        # else:
        #     print('未设置全局变量')

        # 校验值路径是否存在
        if (self.route not in ('', None)):
            self.actual_field_list = []
            route_list = self.route.split(';')
            for r in route_list:
                # 替换参数
                if ('{{' in r):
                    getparmsvalue = GetParmsValue()
                    r = getparmsvalue.get_parms_value(self.route, self.env)

                try:
                    self.actual_field_list.append(self.getmyvalue(self.actual_response, r))
                except:
                    return ({"success": False, "msg": "无法获取" + str(r) + "对应的value"})
        # else:
        #     print("该接口没有设置校验值路径")

        # 校验
        if ((self.route in ('', None)) and (self.expected_response not in ('', None))):

            # 校验块内容字段
            try:
                # 替换参数
                if ('{{' in self.expected_response):
                    getparmsvalue = GetParmsValue()
                    self.expected_response = getparmsvalue.get_parms_value(self.expected_response, self.env)
                verify.should_contain(''.join(self.actual_response.split()), ''.join(self.expected_response.split()))
                print('返回结果中' + self.actual_response + '字段中包含预期返回值 ' + self.expected_response + "全部字段")
            except  Exception as e:
                print(e)
                return {"success": False, "msg": "返回结果中不包含预期返回值全部字段,请检查!"}
            return {"success": True, "msg": "OK"}
        elif ((self.route not in ('', None)) and (self.expected_response in ('', None))):
            expected_field_list = self.expected_field.split(';')
            print('')
            i = 0
            for route, actual_field,check_type in zip(self.route.split(';'), self.actual_field_list,self.types.split(';')):
                i += 1
                # 替换参数
                try:
                    if ('{{' in expected_field_list[i - 1]):
                        getparmsvalue = GetParmsValue()
                        expected_field_list[i - 1] = getparmsvalue.get_parms_value(expected_field_list[i - 1], self.env)

                    if(check_type=='equal'  or  check_type == ''):
                        if (actual_field == expected_field_list[i - 1]):
                            print('接口返回数据中' + str(route) + '校验路径字段值匹配成功为' + actual_field)
                        else:
                            return {"success": False, "msg": '接口返回数据中' + str(route) + '校验路径字段值应该为' + expected_field_list[
                                i - 1] + ',而不是' + actual_field}
                    elif(check_type=='regex'):
                        actual_field = actual_field.strip('"')
                        if('\\\\'in  expected_field_list[i - 1]):
                            # expected_field_new=eval(expected_field_list[i - 1])
                            expected_field_new=expected_field_list[i - 1].replace('\\\\','\\')
                            regex_result=re.search(expected_field_new,actual_field,re.I|re.M|re.S)
                        else:
                            # A=expected_field_list[i - 1]
                            regex_result=re.search(expected_field_list[i - 1],actual_field,re.I|re.M|re.S)
                        if(regex_result):
                            print('接口返回数据中' + str(route) + '校验路径字段值正则匹配成功为' + actual_field)
                        else:
                            return {"success": False, "msg": '接口返回数据中' + str(route) + '路径的字段值' + actual_field + '匹配正则'+expected_field_list[
                            i - 1]+'失败'}
                    else:
                        return {"success": False, "msg": "校验类型无法匹配"}
                except:
                    return {"success": False, "msg": "请检查使用的全局变量"}

            return {"success": True, "msg": "OK"}

        elif ((self.route not in ('', None)) and (self.expected_response not in ('', None))):
            # 校验某些字段
            try:
                # 替换参数
                if ('{{' in self.expected_response):
                    getparmsvalue = GetParmsValue()
                    self.expected_response = getparmsvalue.get_parms_value(self.expected_response, self.env)

                verify.should_contain(''.join(self.actual_response.split()), ''.join(self.expected_response.split()))
                print('返回结果中' + self.actual_response + '字段中包含预期返回值 ' + self.expected_response + "全部字段")
            except:

                return {"success": False, "msg": '返回结果中不包含预期返回值全部字段,' + "请检查!"}

            expected_field_list = self.expected_field.split(';')
            i = 0
            for route, actual_field,check_type in zip(self.route.split(';'), self.actual_field_list,self.types.split(';')):
                print("route=" + route)
                print("actual_field=" + actual_field)
                i += 1
                # 替换参数
                try:
                    if ('{{' in expected_field_list[i - 1]):
                        getparmsvalue = GetParmsValue()
                        expected_field_list[i - 1] = getparmsvalue.get_parms_value(expected_field_list[i - 1], self.env)
                    if (check_type == 'equal'  or  check_type == ''):
                        if (actual_field == expected_field_list[i - 1]):
                            # print('接口返回数据中' + '第' + str(i) + '校验路径字段值匹配成功为' + actual_field)
                            print('接口返回数据中' + str(route) + '校验路径字段值匹配成功为' + actual_field)

                        else:
                            return {"success": False, "msg": '接口返回数据中' + str(route) + '校验路径字段值应该为' + expected_field_list[
                                i - 1] + ',而不是' + actual_field}
                    elif (check_type == 'regex'):
                        actual_field = actual_field.strip('"')
                        if ('\\\\' in expected_field_list[i - 1]):
                            # expected_field_new=eval(expected_field_list[i - 1])
                            expected_field_new = expected_field_list[i - 1].replace('\\\\', '\\')
                            # regex_result = re.match(expected_field_new, actual_field)
                            regex_result=re.search(expected_field_new,actual_field,re.I|re.M|re.S)
                        else:
                            # regex_result = re.match(expected_field_list[i - 1], actual_field)
                            regex_result=re.search(expected_field_list[i - 1],actual_field,re.I|re.M|re.S)

                        if (regex_result):
                            print('接口返回数据中' + str(route) + '校验路径字段值正则匹配成功为' + actual_field)
                        else:
                            return {"success": False,
                                    "msg": '接口返回数据中' + str(route) + '路径的字段值' + actual_field + '匹配正则'+expected_field_list[
                            i - 1]+'失败'}
                    else:
                        return {"success": False, "msg": "校验类型无法匹配"}
                except:
                    return {"success": False, "msg": "请检查使用的全局变量"}
        return {"success": True, "msg": "OK"}

# m = CheckOut('get_request', '17')
