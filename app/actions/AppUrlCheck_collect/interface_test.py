import re, logging,requests
import json,sys,getopt
from .interface_conf import interface_conf

user_define_log_level=logging.DEBUG

logging.basicConfig(
    level=user_define_log_level,  # 定义输出到文件的log级别，
    format='[%(asctime)s][%(filename)s]-[%(funcName)s]-[%(lineno)d] [%(levelname)s] %(message)s',  # 定义输出log的格式
    datefmt='%Y-%m-%d %H:%M:%S',  # 时间
    )

def re_valueCheck(check_value, re_expression):
    tmp_err = []
    try:
        regex = re.compile(re_expression, re.I|re.M|re.S)
    except Exception as e:
        logging.error('正则表达式提供有误，请检查!')
        logging.error('正则表达式异常信息：%s'%e)
        return False
    try:
        re_result = regex.findall(str(check_value))
        if re_result == []:
            # logging.error('%s字段值正则校验不通过，请检查接口返回信息'%check_key)
            tmp_err.append((check_value,'不应该为空值或不是有效的url或imgUrl，请检查'))
    except Exception as e:
        logging.error('程序异常信息：%s'%e)
    return tmp_err

def url_request_test(url):
    url_request_err = []
    response = requests.get(url)
    if response.status_code != 200:
        url_request_err.append((url,"未能成功访问，当前返回状态码为%s"%response.status_code))
    return url_request_err


def common_params_get(varargs=sys.argv):
    common_params = {
        'env': 'prd',
        'Version': '10.19.0'
    }
    opts, args = getopt.getopt(varargs[1:], "e:v:", ["env=", "vParam="])
    print("opts:",opts)
    print("args:",args)
    for k,v in opts:
        if k in ("-e","--env"):
            common_params['env']=v
            logging.info("测试环境为：{}".format(common_params['env']))

        if k in ("-v","--vParam"):
            common_params['Version']=v
            logging.info("测试版本号为：{}".format(common_params['Version']))
    return common_params

def interface_test(interface_name,data,env='pre'):
    method = interface_conf[interface_name]['method']
    # data = interface_conf[interface_name]['data']
    path = interface_conf[interface_name]['path']
    # print('data: ',data, type(data))
    domain = interface_conf[interface_name]['domain'][env]
    # print(domain)
    url = 'https://'+ domain + path
    if method in ('get','GET'):
        response =requests.get(url,params=data)
    elif method in ('post','POST'):
        response = requests.post(url=url, data=data)
    if response.status_code == 200:
        response = json.loads(response.text)
    else:
        response = {'success': False, 'msg': '接口请求失败，响应状态码为%s'%response.status_code, 'data':None}
    return response
