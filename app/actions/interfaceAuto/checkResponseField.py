# encoding:utf-8
import logging
import re

user_define_log_level=logging.DEBUG

logging.basicConfig(
    level=user_define_log_level,  # 定义输出到文件的log级别，
    format='[%(asctime)s][%(filename)s]-[%(funcName)s]-[%(lineno)d] [%(levelname)s] %(message)s',  # 定义输出log的格式
    datefmt='%Y-%m-%d %H:%M:%S',  # 时间
    )

class CheckIfResultIsNone:
    def __init__(self):
        self.nullList=[]
        self.not_nullList=[]
        self._temp = []
        self.reErrorList = []
        self.reSuccessList = []

    def check(self,dict, *args):
        """
         判断key是否正确，先判断是否存在，然后判断key的值value
        :param key:
        :return:
        """
        if self.isKey(dict,*args):
            if self.isValue(dict,*args):
                return True
            else:
                return False
        else:
            return False

    def isKey(self, dict , *args):
        """
        检查key是否存在
        :param key:
        :return:
        """
        tmp = []
        for key in args:
            if key not in dict:
                tmp.append(key)
        if len(tmp)>0:
            return False
        else:
            return True

    def isValue(self, dict, *args):
        """
        检查value的值是否为None或空字符串，支持多key查询
        :return:True对应value非空；False对应value有空
        """
        tmp = []
        for i in args:

            if dict[i] is None or len(str(dict[i])) <= 0:
                tmp.append(i)
        if len(tmp) > 0:
            return False
        else:
            return True


# 显示所有的空字段及其层级
    def checkcCertainParm(self,response,level=0):
        if type(response).__name__ == 'dict':
            if len(list(response.keys()))>0:
                # print('response.key():',response.keys())
                count=level+1
                for i in list(response.keys()):
                    result = self.check(response,i)
                    # self.temp=SuccessJudge(self.temp,result).judge()
                    if not result:
                        self.nullList.append({i:count})
                    else:
                        self.not_nullList.append({i:count})
                        self.checkcCertainParm(response[i],level=count)

        if type(response).__name__ == 'list':
            if len(response)>0:
                count = level + 1
                for i in range(len(response)):
                    self.checkcCertainParm(response[i],level=count)
        return self.nullList,self.not_nullList


class CheckResult:

    def __init__(self,checkList,nullList,not_nullList):
        self.temp=True
        self.checkList=checkList
        self.nullList=nullList
        self.not_nullList=not_nullList
        self.null_str=[]
        self.not_exist_key = []

    def checkResult(self):
        for i in self.checkList:
            if i in self.nullList:
                self.temp=False
                self.null_str.append(str(i))
            elif i not in self.not_nullList:
                self.temp=False
                self.not_exist_key.append(str(i))

        for i in set(self.null_str):
            # print("\033[0;33m{parm1}\033[0m\033[0;33m{information}\033[0m\033[0;33m{parm2}\033[0m".format(parm1="ERROR:字段",information=str(i),parm2="对应的值为空"))
            logging.error('%s对应的值为空', i)
        for j in set(self.not_exist_key):
            logging.error('%s对应的key不存在',j)
        return self.temp

def newCheck(checkList,response):
        nullList,not_nullList = CheckIfResultIsNone().checkcCertainParm(response)
        # print(nullList)
        # print(not_nullList)
        return CheckResult(checkList, nullList,not_nullList).checkResult()


##************* 20190830 dff: 根据正则表达式校验预期结果字段值 *************
class CheckResult_by_reExpression:
    def __init__(self):
        self.nullValueList=[]
        self._temp = []
        self.reErrorList = []
        self.reSuccessList = []

    #按正则表达式校验字段值
    def re_check(self,dict, re_expression, check_key):
        """
         判断key是否正确，先判断是否存在，然后按正侧表达式判断key的值value
        :param key:
        :return:
        """
        if self.re_valueCheck(dict, re_expression, check_key):
            return True
        else:
            return False

    def re_valueCheck(self, dict, re_expression, check_key):
        tmp_err = []
        try:
            regex = re.compile(re_expression, re.I|re.M|re.S)
        except Exception as e:
            logging.error('正则表达式提供有误，请检查!')
            logging.error('正则表达式异常信息：%s'%e)
            return False
        try:
            re_result = regex.findall(str(dict[check_key]))
            # print('key-->:',check_key,'; key-value-->:',dict[check_key],';result-->: ',re_result)
            if re_result == []:
                # logging.error('%s字段值正则校验不通过，请检查接口返回信息'%check_key)
                tmp_err.append(check_key)
        except Exception as e:
            print('异常key:',check_key,'; 对应的value: ',dict[check_key])
            tmp_err.append(check_key)
            # logging.error('%s字段值正则校验不通过或程序异常，请检查接口返回信息'%check_key)
            logging.error('程序异常信息：%s'%e)
        if len(tmp_err)>0:
            return False
        else:
            return True

# 显示所有正则校验通过、不通过的字段及其层级
    def re_checkcCertainParm(self,response,re_expression, level=0):
        if type(response).__name__ == 'dict':
            if len(list(response.keys()))>0:
                # print('response.key():',response.keys())
                # count=level+1
                for i in list(response.keys()):
                    count=level+1
                    if type(response[i]).__name__  in('str','int','float'):  #如果该字段对应的值是str,则进行正则校验
                        result = self.re_check(response,re_expression,i)
                    # self.temp=SuccessJudge(self.temp,result).judge()
                        if not result:
                            self.reErrorList.append({i:count})
                        else:
                            self.reSuccessList.append({i:count})
                    elif type(response[i]).__name__ == 'dict': #如果字段值是dict，则继续下一层处理
                        self.re_checkcCertainParm(response[i],re_expression,level=count)
                    elif response[i] in (None,'',[]):  # 如果字段值为空，则记录空字段列表中
                        self.nullValueList.append({i:count})
                    elif type(response[i]).__name__  == 'list':
                        if len(response[i])>0 and type(response[i][0]).__name__ == 'dict':
                            count = count + 1
                            for j in range(len(response[i])):
                                self.re_checkcCertainParm(response[i][j],re_expression,level=count)
                        else:
                            self.reSuccessList.append({i:count})


        if type(response).__name__ == 'list' and type(response[0]).__name__ == 'dict':
            if len(response)>0:
                count = level + 1
                for i in range(len(response)):
                    self.re_checkcCertainParm(response[i],re_expression,level=count)
        return self.reErrorList,self.reSuccessList,self.nullValueList


class re_CheckResult:

    def __init__(self,checkList,reErrorList,reSuccessList,nullValueList):
        self.temp=True
        self.checkList=checkList
        self.reErrorList=reErrorList
        self.reSuccessList=reSuccessList
        self.nullValueList=nullValueList
        self.err_str=[]
        self.null_value_list = []
        self.not_exist_key_list = []
        self.result_msg_list =[]

    def re_checkResult(self):
        for i in self.checkList:
            if i in self.nullValueList:
                self.null_value_list.append(str(i))
                logging.error('%s字段对应的值为空'%i)
                self.result_msg_list.append('%s字段对应的值为空'%i)
                self.temp = False
            elif i in self.reErrorList:
                self.err_str.append(str(i))
                logging.error('%s对应的值正则校验不通过'% i)
                self.result_msg_list.append('%s对应的值正则校验不通过'%i)
                self.temp = False
            elif i not in self.reSuccessList:
                self.not_exist_key_list.append(str(i))
                logging.error('%s对应的key不存在'%i)
                self.result_msg_list.append('%s对应的key不存在'%i)
                self.temp = False
        return self.temp,self.result_msg_list


def re_newCheck(checkList,response,re_expression):
        reErrorList,reSuccessList,nullValueList = CheckResult_by_reExpression().re_checkcCertainParm(response,re_expression)
        print('reErrorList:',reErrorList)
        print('reSuccessList:', reSuccessList)
        print('nullValueList:', nullValueList)
        return re_CheckResult(checkList, reErrorList,reSuccessList,nullValueList).re_checkResult()

def re_string2list(str1):
    try:
        str2list = str1.split(',')
        tmp_list = []
        for i in str2list:
            tmp_list.append(eval(i))
        #校验处理后的字段列表样式是否符合{'key':n}格式要求
        for j in tmp_list:
            if type(j).__name__ != 'dict':
                logging.error("输入的正则校验字段列表格式有误，请检查！参考样式：{'key1':n},{'key2':n}....")
                tmp_list = []
                break
    except Exception as e:
        logging.error("输入的正则字段列表格式有误，导致程序异常：%s"%e)
        tmp_list = []
    return tmp_list


if __name__ == '__main__':
    checkList1 = [{'sessionId': 2},{'offlineService':2}]
    checklist2 = [{'key': 5}, {'rankDesc': 5}]
    # re_expression1 = '^https.*?\.png$'   #匹配以https开头，且以.png结尾的值
    # re_expression1 = '^https|^tuniuapp'
    re_expression1 = '.*'
    response={"success": True, "errorCode": 710000, "msg": "OK", "data": {"pin": 0, "offlineInfo": {"title": "鼓楼新街口金轮店", "url": "https://m.tuniu.com/travel/retail/list/1602?needLocation=1"}, "offlineService": None, "adviser": {"content": None, "recommend": {"icon": "https://m4.tuniucdn.com/fb2/t1/G5/M00/B9/66/Cii-slznmUKIL9S5AAB36zX-nQgAAWEawNFHPYAAHgD223_w180_h180_c1_t0.png", "title": None, "subTitle": None, "url": "tuniuapp://page?iosPageName=TNUserConsultantViewController&androidPageName=com.tuniu.usercenter.activity.ConsultantWelcomeActivity&parameters={}", "totalNumber": 494}}, "store": {"title": "九霄梦天地店", "subTitle": "附近27家，最近距您约3.3公里", "icon": "https://m1.tuniucdn.com/fb2/t1/G5/M00/B9/66/Cii-slznmUKIQ5vkAABvoomFtJ0AAWEawNFlPkAAG-6154_w180_h180_c1_t0.png", "status": 0, "url": "https://m.tuniu.com/travel/retail/list/1602?needLocation=1"}}}
    response1 = {"success": True, "errorCode": 710000, "msg": "OK", "data": {"sessionId": "a74fff90ebd0af25dd8f2ea92616e1e9_", "isLogin": 0}}
    response2 = {'success': True, 'errorCode': 710000, 'msg': 'OK', 'data': {'keyword': {'duration': 5, 'items': [{'key': '澳门', 'redirectUrl': None, 'rankDesc': '城市观光出游TOP3'}, {'key': '广州', 'redirectUrl': None, 'rankDesc': '主题乐园出游TOP2'}, {'key': '日本', 'redirectUrl': None, 'rankDesc': '滑雪出游TOP1'}]}}}
    result,result_msg = re_newCheck(checklist2,response2,re_expression1)
    print(result)
    print(result_msg)

    # str1 = "{'sessionId': 2}"
    # str1 = str1.split(',')
    # print(str1,type(str1))
    # tmp_list =[]
    # for i in str1:
    #     tmp_list.append(eval(i))
    # print(tmp_list)
    # print(type(tmp_list[0]))
    # aa = re_string2list(str1)
    # print('aa',aa)


