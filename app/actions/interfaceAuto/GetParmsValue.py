# coding:utf-8
from app.models.models import Parms_Enviroment
from sqlalchemy import and_, or_
import HttpLibrary
from app import db
import logging
from app.actions.interfaceAuto.sysParamsDefine import *

global true
true = 'true'
global false
false = 'false'
global null
null = 'null'


class GetParmsValue:

    def get_parms_value(self, parmstring, env):
        leftcount = parmstring.count('{{')
        rightcount = parmstring.count('}}')
        # print("parmstring:",parmstring,'\nleftcount:',leftcount,'\nrightcount:',rightcount)
        if leftcount > 0 and rightcount > 0:
            for i in range(0, leftcount):
                start = parmstring.find('{{')
                end = parmstring.find('}}',start)
                if (start == -1 and end == -1):
                    break
                parms_key = parmstring[start + 2:end]
                parms = Parms_Enviroment.query.filter(
                    and_(Parms_Enviroment.parms_key == parms_key, Parms_Enviroment.parms_env == env)).order_by(Parms_Enviroment.create_time.desc()).first()
                # parms_value = parms.parms_value
                try:
                    # 2019-11-27 dff；以下 增加变量类型param_type判断，进行分别处理
                    if parms.parms_type == 'user':
                        parms_value = parms.parms_value.split(',')[0]  # 20190708dff:兼容参数值是多个的情况，则直接取第一个替换
                    elif parms.parms_type == 'sys':
                        tmp_parms_value = parms.parms_value.split(';')
                        print("系统变量值为：",tmp_parms_value)
                        try:  # 对系统变量中自定义的加减数字进行str->int转换
                            num = int(tmp_parms_value[2])
                        except:
                            num = 0
                        if tmp_parms_value[0] == 'curr_date':
                            parms_value = SysParams().curr_date(tmp_parms_value[1],tmp_parms_value[3],num)
                        elif tmp_parms_value[0] == 'curr_time':
                            parms_value = SysParams().curr_time(tmp_parms_value[1],tmp_parms_value[3],num)
                        elif tmp_parms_value[0] == 'curr_month':
                            parms_value = SysParams().curr_month(tmp_parms_value[1],tmp_parms_value[3],num)
                        print("处理后的系统变量为：",parms_value)
                    parmstring = parmstring.replace("{{" + parms_key + "}}",parms_value)

                except:
                    logging.info("替换参数异常")
                    parmstring=parmstring
        return parmstring

    def get_parms_value_from_key(self, route, name, env, response,user):
        route_data = route.split(";")
        name_data = name.split(";")
        # 轮询数据参数并格式化处理
        i = 0
        for route_item in route_data:
            # 调用HttpLibrary模块的get_json_value方法
            data = HttpLibrary.HTTP()
            # eval去掉返回的sessionId的左右两边的引号
            try:
                value = eval(data.get_json_value(response, route_item))
                key = name_data[i]
                i = i + 1
                count = Parms_Enviroment.query.filter(
                    and_(Parms_Enviroment.parms_key == key, Parms_Enviroment.parms_env == env)).count()
                if (count != 0):
                    parms_one = Parms_Enviroment.query.filter(
                        and_(Parms_Enviroment.parms_key == key, Parms_Enviroment.parms_env == env)).order_by(Parms_Enviroment.create_time.desc()).first()
                    if (str(parms_one.parms_value) == str(value)):
                        print("全局变量值无任何变化,不做数据库更新")
                    else:
                        parms_one.parms_value = value
                        parms_one.create_user =user
                        db.session.add(parms_one)
                        db.session.commit()
                        print('全局变量' + str(key) + ':' + str(value) + '更新成功')
                else:
                    param_add = Parms_Enviroment(
                        id=0,
                        parms_key=key,
                        parms_value=value,
                        parms_env=env,
                        create_user=user,
                    )
                    db.session.add(param_add)
                    db.session.commit()
                    print('全局变量' + str(key) + ':' + str(value) + '新增成功')
            except Exception as e:
                print(e)
                print("校验失败,请检查输入的全局字段路径或名称")
                return {"success": False, "msg": "校验失败,请检查输入的全局字段路径或名称"}
        return  {"success": True, "msg": "全局变量校验OK"}

    # dff 20190708 : 获取变量对应多个值的情况，将多个值按逗号',’分隔，形成list
    def get_params_values_list(self, paramstring, env):
        '''
        根据入参中 变量名分别获取变量值 列表信息
        :param paramstring:   用来接收请求参数字符串
        :param env: 使用变量所属环境
        :return: paramstring（原始请求参数，或 参数化后的参数串）， params -- 获取到的由“变量:变量值"（params_key:params_value)组成的字典，变量值为多个时，得到是list类型
        '''
        leftcount = paramstring.count('{{')
        rightcount = paramstring.count('}}')
        # print("parmstring:",parmstring,'\nleftcount:',leftcount,'\nrightcount:',rightcount)
        if leftcount > 0 and rightcount > 0:
            params = {}
            for i in range(0, leftcount):
                start = paramstring.find('{{')
                end = paramstring.find('}}',start)
                if (start == -1 and end == -1):
                    break
                params_key = paramstring[start + 2:end]
                params_record = Parms_Enviroment.query.filter(
                    and_(Parms_Enviroment.parms_key == params_key, Parms_Enviroment.parms_env == env)).order_by(Parms_Enviroment.create_time.desc()).first()
                if params_record is not None:
                    # 20191127 dff：增加变量类型的判断，user,sys类型分别处理
                    if params_record.parms_type == 'user':  #如果是user类型，则走原有逻辑处理
                        params_value = params_record.parms_value
                        if len(params_value.split(',')) == 1:
                            paramstring = paramstring.replace("{{" + params_key + "}}",params_value)
                            params[params_key] = params_value.split(',')
                        elif len(params_value.split(',')) > 1:
                            paramstring = paramstring.replace("{{" + params_key + "}}",params_value.split(',')[0])  #如果获取到的变量值是多个（即"南京,北京,上海"类似格式），则先取第一值先参数化
                            params[params_key] = params_value.split(',') # 并且把取到的变量key 与变量value形成字典先记录下来
                    #如果是sys系统变量，则按下述逻辑处理
                    elif params_record.parms_type == 'sys':
                        tmp_parms_value = params_record.parms_value.split(';')
                        print("初始系统变量值为：",tmp_parms_value)
                        try:  # 对系统变量中自定义的加减数字进行str->int转换
                            num = int(tmp_parms_value[2])
                        except:
                            num = 0
                        if tmp_parms_value[0] == 'curr_date':
                            params_value = SysParams().curr_date(tmp_parms_value[1],tmp_parms_value[3],num)
                        elif tmp_parms_value[0] == 'curr_time':
                            params_value = SysParams().curr_time(tmp_parms_value[1],tmp_parms_value[3],num)
                        elif tmp_parms_value[0] == 'curr_month':
                            params_value = SysParams().curr_month(tmp_parms_value[1],tmp_parms_value[3],num)
                        print("处理后的系统变量值为：",params_value)
                        paramstring = paramstring.replace("{{" + params_key + "}}",params_value)
                        params[params_key] = params_value.split(',')

                else:  #未从库里取到变量值，则退出循环，直接返回parmstring本身
                    print("未取到要参数化的变量值，请检查表数据")
                    # params=parmstring
                    break
            return paramstring, params
        else:
            # print("s未使用变量值，无需参数化")
            params = {}

            return paramstring, params

    def set_params_list(self,origin_param, params_list):
        '''
        将获取到的变量值一一替换到入参中，形成可具体发起请求的实际入参
        :param origin_param:  接收原始未参数化前的入参字符串
        :param params_list:  接收由get_params_values_list()方法处理后的参数值列表信息
        :return:
        '''
        print(params_list)
        params_len = [len(x) for x in (params_list.values())]
        for_times = max(params_len)
        # print(params_len, '\n', paramstring, '\n', for_times)
        rest_params_list =[]
        for i in range(for_times):
            tem_string = origin_param
            for key in params_list:
                # print("key:",key)
                # print('before:',tem_string)
                if len(params_list[key]) <= i:
                    tem_string = tem_string.replace('{{'+key+'}}',params_list[key][len(params_list[key])-1])
                else:
                    tem_string = tem_string.replace('{{'+key+'}}',params_list[key][i])
                # print('after:',tem_string)
            # print(i,tem_string)
            rest_params_list.append(tem_string)
        return  rest_params_list

if __name__ == '__main__':
    rest_param = '"citycode":{{cityCode}},"cityname":{{cityName}},"success":true,"msg":"ok","version":{{Version}}'
    param = GetParmsValue()
    paramstring,params_list = param.get_params_values_list(rest_param,'prd')
    print("1:",paramstring)
    if params_list != {}:
        request_list = param.set_params_list(rest_param,params_list)
        for item_reques in request_list:
            print(item_reques, type(item_reques))