from flask import Blueprint, request
from sqlalchemy import func, and_, desc
import unittest
import os,json,requests
from views.interfaceAuto.interface import cors_response
from app.models.models import *
from app.actions.AppUrlCheck_collect.interface_conf import Common_params
from concurrent.futures import ThreadPoolExecutor
executor =ThreadPoolExecutor(1)

case_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/app/actions/AppUrlCheck_collect'
# print(case_path)

ios_ui_case_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/app/actions/AppUITest_ios'

# 设置蓝图
appurlcheck = Blueprint('appurlcheck', __name__)

@appurlcheck.route('/execUrlCheck', methods=['GET','POST'])
def sync_execUrlCheck():
    file_name = request.args.get('file_name') or "testCase_portal.py"
    case_name = request.args.get('case_name') or "url检查接口（自定义）"
    version = request.args.get('version') or '10.19.0'
    env = request.args.get('env') or 'pre'
    print('version:',version, "env:",env)
    error_webhook = request.args.get('webhook') or "https://oapi.dingtalk.com/robot/send?access_token=ebb3a70ad93edff6d8a025fe85902d615dca48bbc537c18cb8ece746fc37b010"
    print(file_name,case_name,'\n',version,env, '\n')
    Common_params.version = version
    Common_params.env = env
    executor.submit(execUrlCheck,file_name,case_name,error_webhook,env)
    response = {"success": "true", "msg": "url批量检查中，请稍后[自动化报告列表]界面查看~~"}
    return cors_response(response)

def execUrlCheck(file_name, case_name,error_webhook,env):
    print('begin start......')
    discover = unittest.defaultTestLoader.discover(case_path,pattern=file_name)
    suite = unittest.TestSuite()
    suite.addTest(discover)
    test_result = unittest.TextTestRunner().run(suite)
    case_success = int(test_result.testsRun) - len(test_result.failures)-len(test_result.errors)
    if len(test_result.failures)>0 or len(test_result.errors)>0:
        response = {'success': False, 'case_totalnum': test_result.testsRun, 'case_success': case_success,'case_failures': test_result.failures, 'case_errors': test_result.errors}
    else:
        response = {'success': True,'case_totalnum': test_result.testsRun, 'case_success': case_success,'case_failures': 0, 'case_errors': 0}
    print(response)
    # 获取用例本身的信息，以便下面记录report表
    case_info = Interface_Mall.query.filter(Interface_Mall.name == case_name).first()
    if case_info is not None:
        #从report表获取该用例记录的信息，后续每个用例利用case_id,count
        report_case_info = Report.query.filter(Report.case_id == case_info.tree_id).order_by(Report.id.desc()).first()
        if report_case_info is not None:
            case_id = report_case_info.case_id
            count = report_case_info.count
        #若报告中未获取到该用例信息，则重新计算最大count全新记录
        else:
            case_id = case_info.tree_id
            report_count = Report.query.filter_by().order_by(Report.count.desc()).first()
            if report_count is not None:
                count = report_count.count + 1
            else:
                count = 1
        if len(test_result.failures) >0:
            try:
                for case,reason in test_result.failures:
                    report_info = Report(
                                case_id=case_id,
                                rest = str(case.id()),
                                result=0,
                                outparams = '测试失败',
                                checkout=str(reason),
                                count=count
                            )
                    db.session.add(report_info)
            except Exception as e:
                print(e)
            else:
                db.session.commit()

        if len(test_result.errors) >0:
            try:
                for case,reason in test_result.errors:
                    report_info = Report(
                                case_id=case_id,
                                rest = str(case.id()),
                                result=0,
                                outparams = '脚本执行有误',
                                checkout=str(reason),
                                count=count
                            )
                    db.session.add(report_info)
            except Exception as e:
                print(e)
            else:
                db.session.commit()
        if len(test_result.errors) == 0 and len(test_result.failures) == 0:
            try:
                report_info = Report(
                    case_id = case_id,
                    result = 1,
                    outparams = '共执行用例【%d】个，全部测试通过~~~'%int(test_result.testsRun),
                    count = count,
                )
                db.session.add(report_info)
            except Exception as e:
                print(e)
            else:
                db.session.commit()

        #计算总体成功率，发送钉钉提醒信息 (暂不使用，采用pandora jenkins触发统一报告dingding提醒
        # Success=round(int(case_success)/int(test_result.testsRun),2) *100
        # #测试模块
        # test_module = file_name[9:-3]
        # # 这里是传送的消息
        # header = {"Content-Type": "application/json", "charset": "utf-8"}
        # data = {"msgtype": "link", "link": {
        #     "text": ">>成功率:" + str(Success) + "% ,用例总数:" + str(test_result.testsRun) + "\n" + ">>成功数:" + str(case_success)+ ",失败数:" + str(len(test_result.errors)+len(test_result.failures)) + "\n" + ">>查看更多...",
        #     "title": "APP聚合接口url巡检报告(mob_"+test_module+"_"+env+")\n",
        #     "picUrl": "http://m.tuniucdn.com/fb2/t1/G5/M00/A1/8B/Cii-slq7dASIL3m5AAB17eM2eHsAAE2fgPygjoAAHYF06_w400_h300_c1_t0.jpeg",
        #     "messageUrl": "http://pandora.tuniu.org/automation/report/"+str(count)}}
        # message_json = json.dumps(data)
        # if len(test_result.errors) == 0 and len(test_result.failures) == 0:
        #     webhook = "https://oapi.dingtalk.com/robot/send?access_token=9d28e85a48392be9cc2fb1579c7e213f6db1d0810d1efe0c7bf13d4456763acf"
        # else:
        #     #volvo bug_小秘书机器人
        #     # webhook="https://oapi.dingtalk.com/robot/send?access_token=ebb3a70ad93edff6d8a025fe85902d615dca48bbc537c18cb8ece746fc37b010"
        #     webhook = error_webhook
        # # 发送钉钉信息
        # msg = requests.post(url=webhook, data=message_json, headers=header)
        # # 打印返回值
        # print(msg.text)


@appurlcheck.route('/iosuitest', methods=['GET','POST'])
def sync_iosuitest():
    case_name = request.args.get('case_name') or "ios界面自动化"
    executor.submit(iosUItest,case_name)
    response = {"success": "true", "msg": "ios界面自动化脚本后台运行中，请稍后[自动化报告列表]界面查看~~"}
    return cors_response(response)

def iosUItest(case_name):
    print('begin start......')
    discover = unittest.defaultTestLoader.discover(ios_ui_case_path,pattern="Test*.py")
    suite = unittest.TestSuite()
    suite.addTest(discover)
    test_result = unittest.TextTestRunner().run(suite)
    case_success = int(test_result.testsRun) - len(test_result.failures)-len(test_result.errors)
    if len(test_result.failures)>0 or len(test_result.errors)>0:
        response = {'success': False, 'case_totalnum': test_result.testsRun, 'case_success': case_success,'case_failures': test_result.failures, 'case_errors': test_result.errors}
    else:
        response = {'success': True,'case_totalnum': test_result.testsRun, 'case_success': case_success,'case_failures': 0, 'case_errors': 0}
    print(response)
    # 获取用例本身的信息，以便下面记录report表
    case_info = Interface_Mall.query.filter(Interface_Mall.name == case_name).first()
    if case_info is not None:
        #从report表获取该用例记录的信息，后续每个用例利用case_id,count
        report_case_info = Report.query.filter(Report.case_id == case_info.tree_id).order_by(Report.id.desc()).first()
        if report_case_info is not None:
            case_id = report_case_info.case_id
            count = report_case_info.count
        #若报告中未获取到该用例信息，则重新计算最大count全新记录
        else:
            case_id = case_info.tree_id
            report_count = Report.query.filter_by().order_by(Report.count.desc()).first()
            if report_count is not None:
                count = report_count.count + 1
            else:
                count = 1
        if len(test_result.failures) >0:
            try:
                for case,reason in test_result.failures:
                    report_info = Report(
                                case_id=case_id,
                                rest = str(case.id()),
                                result=0,
                                outparams = '测试失败',
                                checkout=str(reason),
                                count=count
                            )
                    db.session.add(report_info)
            except Exception as e:
                print(e)
            else:
                db.session.commit()

        if len(test_result.errors) >0:
            try:
                for case,reason in test_result.errors:
                    report_info = Report(
                                case_id=case_id,
                                rest = str(case.id()),
                                result=0,
                                outparams = '脚本执行有误',
                                checkout=str(reason),
                                count=count
                            )
                    db.session.add(report_info)
            except Exception as e:
                print(e)
            else:
                db.session.commit()
        if len(test_result.errors) == 0 and len(test_result.failures) == 0:
            try:
                report_info = Report(
                    case_id = case_id,
                    result = 1,
                    outparams = '共执行用例【%d】个，全部测试通过~~~'%int(test_result.testsRun),
                    count = count,
                )
                db.session.add(report_info)
            except Exception as e:
                print(e)
            else:
                db.session.commit()

        #计算总体成功率，发送钉钉提醒信息 (暂不使用，采用pandora jenkins触发统一报告dingding提醒
        # Success=round(int(case_success)/int(test_result.testsRun),2) *100
        # #测试模块
        # test_module = file_name[9:-3]
        # # 这里是传送的消息
        # header = {"Content-Type": "application/json", "charset": "utf-8"}
        # data = {"msgtype": "link", "link": {
        #     "text": ">>成功率:" + str(Success) + "% ,用例总数:" + str(test_result.testsRun) + "\n" + ">>成功数:" + str(case_success)+ ",失败数:" + str(len(test_result.errors)+len(test_result.failures)) + "\n" + ">>查看更多...",
        #     "title": "APP聚合接口url巡检报告(mob_"+test_module+"_"+env+")\n",
        #     "picUrl": "http://m.tuniucdn.com/fb2/t1/G5/M00/A1/8B/Cii-slq7dASIL3m5AAB17eM2eHsAAE2fgPygjoAAHYF06_w400_h300_c1_t0.jpeg",
        #     "messageUrl": "http://pandora.tuniu.org/automation/report/"+str(count)}}
        # message_json = json.dumps(data)
        # if len(test_result.errors) == 0 and len(test_result.failures) == 0:
        #     webhook = "https://oapi.dingtalk.com/robot/send?access_token=9d28e85a48392be9cc2fb1579c7e213f6db1d0810d1efe0c7bf13d4456763acf"
        # else:
        #     #volvo bug_小秘书机器人
        #     # webhook="https://oapi.dingtalk.com/robot/send?access_token=ebb3a70ad93edff6d8a025fe85902d615dca48bbc537c18cb8ece746fc37b010"
        #     webhook = error_webhook
        # # 发送钉钉信息
        # msg = requests.post(url=webhook, data=message_json, headers=header)
        # # 打印返回值
        # print(msg.text)



# if __name__ == '__main__':
    # runner = unittest.TextTestRunner()
    # runner.run(get_allcase())
    # test_result = unittest.TextTestRunner().run(get_allcase())
    # # unittest.TextTestRunner(verbosity=2).run(test_suite)
    # print("total testcases num: ", test_result.testsRun)
    # print("failes: ", test_result.failures)
    # print("errors: ", test_result.errors)
    # for case, reason in test_result.failures:
    #     print(case.id())
    #     print(reason)
    # for case, reason in test_result.errors:
    #     print(case.id())
    #     print(reason)
    # report = exec_case()
    # print(report)

