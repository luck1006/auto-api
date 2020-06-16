import sys,os
import unittest

# print(sys.path)
# current_dir = os.path.dirname(os.path.abspath(__file__))
# print(current_dir)
# config_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\TestConf'
# print(config_dir)
# sys.path.append(current_dir)
# sys.path.append(config_dir)
# print(sys.path)

from ddt import ddt,data
from app.actions.AppUrlCheck_collect.interface_test import re_valueCheck,url_request_test
from app.actions.AppUrlCheck_collect.interface_test import common_params_get,interface_test
from app.actions.AppUrlCheck_collect.interface_conf import Common_params



version = Common_params.version
env = Common_params.env
print("当前测试版本号：",version)
print("当前测试环境：",env)

cityCode = [(1602,"南京"),(200,"北京"),(2500,"上海"),(3402,"杭州"),(1615,"苏州"),\
            (3000,"天津"),(619,"深圳"),(1619,"无锡"),(2802,"成都"),(300,"重庆"),\
            (1402,"武汉"),(1902,"沈阳"),(602,"广州"),(3415,"宁波"),(2702,"西安"),\
            (1202,"郑州")]
# cityCode = [(2802,"成都")]
page = [(1602,1),(1602,2),(1602,3),(1602,4),(1602,5),(200,1),(200,2),(200,3),(200,4),(200,5),(2500,1),(2500,2),(2500,3),(2500,4),(2500,5)]
# page = [(1602,1)]

@ddt
class mob_portal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.value_err = []
        cls.img_url = []
        # cls.common_params = common_params_get()
        # cls.env = cls.common_params['env']
        # cls.Version = cls.common_params['Version']
        cls.version = Common_params.version
        cls.env = Common_params.env

    @data(*cityCode)
    def test_旅游频道页(self,cityCode):
        value_err = []
        regex_expression = "(http|https)://((m|m\d)\.tuniucdn.com|m.tuniucdn.com|s.tuniu.net|img3.tuniucdn.com)/\S+.(jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF|(/w/\d+/h/\d+))$"
        params = 'c={"cc":'+str(cityCode[0])+',"ct":10,"p":14588,"ov":20,"dt":0,"v":"'+version+'"}&d={"productPageId":2698,"channelType":7,"pageId":3559,"width":750,"bookCityName":"'+cityCode[1]+'","tact":"9EA881B7-E104-412A-BD96-5B57413B75B3","lat":"32.092636","token":"bi","height":750,"uniqueKey":"c6777549d3dca9d907271ee6ac3d189df00fdb49","lng":"118.883316","locateCityCode":"1602"}}'

        response = interface_test('portal_app_channel_index_旅游', params,env)
        print("response:",response)
        if response['success'] is True and response['data'] is not None:
            #1,品类入口区块检查
            if len(response['data']['categoryAndThemes']['contents']) > 0:
                for i in response['data']['categoryAndThemes']['contents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2
            # 2，爆款特价区块检查
            if len(response['data']['flashSales']['saleContents']) > 0:
                for i in response['data']['flashSales']['saleContents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

            #3,热门推荐 放心之选区块
            if len(response['data']['theme']['services']) > 0:
                for i in response['data']['theme']['services']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2
        elif response['success'] is True and response['data'] is None:
            value_err.append(('portal_app_channel_index_旅游','接口返回data数据为null'))
        else:
            value_err.append(('portal_app_channel_index_旅游',response['msg']))

        if len(value_err)>0:
            print(sys._getframe().f_code.co_name,'校验 False','失败详情如下：\n')
            for err in value_err:
                print(err)
            print('~~~ The End ~~~~~')
        else:
            print(sys._getframe().f_code.co_name,'校验：Success')

        self.assertEqual(value_err,[],msg = '存在校验失败结果')

    @data(*cityCode)
    def test_出境游频道页(self,cityCode):
        value_err = []
        regex_expression = "(http|https)://((m|m\d)\.tuniucdn.com|m.tuniucdn.com|s.tuniu.net|img3.tuniucdn.com)/\S+.(jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF|(/w/\d+/h/\d+))$"
        params = 'c={"cc":'+str(cityCode[0])+',"ct":10,"p":14588,"ov":20,"dt":0,"v":"'+version +'"}&d={"productPageId":2059,"channelType":1,"pageId":3492,"width":750,"bookCityName":"'+cityCode[1]+'","tact":"9EA881B7-E104-412A-BD96-5B57413B75B3","lat":"32.087257","token":"bi","height":750,"uniqueKey":"c6777549d3dca9d907271ee6ac3d189df00fdb49","lng":"118.882233","locateCityCode":"1602"}'

        response = interface_test('portal_app_channel_index_出境游', params,env)
        print(" response：",response)
        if response['success'] is True and response['data'] is not None:
            #1,轮播区块检查
            if len(response['data']['slider']['contents']) > 0:
                for i in response['data']['slider']['contents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2
            # 2，爆款特价区块检查
            if len(response['data']['flashSales']['saleContents']) > 0:
                for i in response['data']['flashSales']['saleContents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

            #3,热门主题区块
            if len(response['data']['choices']['contents']) > 0:
                for i in response['data']['choices']['contents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

            #4,出境超市区块
            if len(response['data']['markets']['contents']) > 0:
                for i in response['data']['choices']['contents']:
                    result1 = re_valueCheck(i['imgUrl'],regex_expression)
                    result2 = re_valueCheck(i['appUrl'],'(tuniuapp|http)\S+')
                    result3 = re_valueCheck(i['mUrl'],'(tuniuapp|http)\S+')
                    value_err = value_err + result1+result2+ result3
                    if result1 == []:
                        result4 = url_request_test(i['imgUrl'])
                        value_err = value_err + result4

        elif response['success'] is True and response['data'] is None:
            value_err.append(('portal_app_channel_index_出境游','接口返回data数据为null'))
        else:
            value_err.append(('portal_app_channel_index_出境游',response['msg']))

        if len(value_err)>0:
            print(sys._getframe().f_code.co_name, '校验 False','失败详情如下：\n')
            for err in value_err:
                print(err)
            print('~~~ The End ~~~~~')
        else:
            print(sys._getframe().f_code.co_name,'校验：Success')

        self.assertEqual(value_err,[],msg = '校验失败结果')

    @data(*cityCode)
    def test_境内游频道页(self,cityCode):
        value_err = []
        regex_expression = "(http|https)://((m|m\d)\.tuniucdn.com|m.tuniucdn.com|s.tuniu.net|img3.tuniucdn.com)/\S+.(jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF|(/w/\d+/h/\d+))$"
        params = 'c={"cc":'+str(cityCode[0])+',"ct":10,"p":14588,"ov":20,"dt":0,"v":"'+version +'"}&d={"productPageId":2058,"channelType":2,"pageId":3484,"width":750,"bookCityName":"'+cityCode[1]+'","tact":"9EA881B7-E104-412A-BD96-5B57413B75B3","lat":"32.087298","token":"bi","height":750,"uniqueKey":"c6777549d3dca9d907271ee6ac3d189df00fdb49","lng":"118.882238","locateCityCode":"1602"}'

        response = interface_test('portal_app_channel_index',params,env)
        print("response:",response)
        if response['success'] is True and response['data'] is not None:

            # 1, 轮播图区块检查
            if response['data']['slider']['contents'] is not None and len(response['data']['slider']['contents']) > 0:
                for i in response['data']['slider']['contents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

            # 2，爆款特价区块检查
            if len(response['data']['flashSales']['saleContents']) >0:
                for i in response['data']['flashSales']['saleContents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

            # 3，热门主题区块检查
            if len(response['data']['choices']['contents']) >0:
                for i in response['data']['choices']['contents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2
        elif response['success'] is True and response['data'] is None:
            value_err.append(('portal_app_channel_index_境内游','接口返回data数据为null'))
        else:
            value_err.append(('portal_app_channel_index_境内游',response['msg']))

        if len(value_err)>0:
            print(sys._getframe().f_code.co_name,'校验 False','失败详情如下：\n')
            for err in value_err:
                print(err)
            print('~~~ The End ~~~~~')
        else:
            print(sys._getframe().f_code.co_name,'校验：Success')

        self.assertEqual(value_err,[],msg = '存在校验失败结果')

    @data(*cityCode)
    def test_周边游频道页(self,cityCode):
        value_err = []
        regex_expression = "(http|https)://((m|m\d)\.tuniucdn.com|m.tuniucdn.com|s.tuniu.net|img3.tuniucdn.com)/\S+.(jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF|(/w/\d+/h/\d+))$"
        params = 'c={"cc":'+str(cityCode[0])+',"ct":10,"p":14588,"ov":20,"dt":0,"v":"'+version +'"}&d={"productPageId":3011,"channelType":3,"pageId":3498,"width":750,"bookCityName":"'+cityCode[1]+'","tact":"9EA881B7-E104-412A-BD96-5B57413B75B3","lat":"32.087298","token":"bi","height":750,"uniqueKey":"c6777549d3dca9d907271ee6ac3d189df00fdb49","lng":"118.882238","locateCityCode":"1602"}'

        response = interface_test('portal_app_channel_index',params,env)
        if response['success'] is True and response['data'] is not None:

            # 1, 轮播图区块检查
            if response['data']['slider']['contents'] is not None and len(response['data']['slider']['contents']) > 0:
                for i in response['data']['slider']['contents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

            #2, 品类和游玩区块检查
            if response['data']['categoryAndThemes']['contents'] is not None and\
                len(response['data']['categoryAndThemes']['contents']) > 0:
                for i in response['data']['categoryAndThemes']['contents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

            #3,精选玩法、周边必去检查
            if response['data']['advertisement'] is not None and\
                len(response['data']['advertisement']['contents']) > 0:
                for i in response['data']['advertisement']['contents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

            # 4，主题榜单区块检查
            if response['data']['themeAndTopic'] is not None and \
                            len(response['data']['themeAndTopic']['contents']) >0:
                for i in response['data']['themeAndTopic']['contents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2
        elif response['success'] is True and response['data'] is None:
            value_err.append(('portal_app_channel_index_周边游','接口返回data数据为null'))
        else:
            value_err.append(('portal_app_channel_index_周边游',response['msg']))

        if len(value_err)>0:
            print(sys._getframe().f_code.co_name,'校验 False','失败详情如下：\n')
            for err in value_err:
                print(err)
            print('~~~ The End ~~~~~')
        else:
            print(sys._getframe().f_code.co_name,'校验：Success')

        self.assertEqual(value_err,[],msg = '存在校验失败结果')

    @data(*cityCode)
    def test_跟团游频道页(self,cityCode):
        value_err = []
        regex_expression = "(http|https)://((m|m\d)\.tuniucdn.com|m.tuniucdn.com|s.tuniu.net|img3.tuniucdn.com)/\S+.(jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF|(/w/\d+/h/\d+))$"
        params = 'c={"cc":'+str(cityCode[0])+',"ct":10,"p":14588,"ov":20,"dt":0,"v":"'+version +'"}&d={"productPageId":1534,"channelType":4,"pageId":3482,"width":750,"bookCityName":"'+cityCode[1]+'","tact":"9EA881B7-E104-412A-BD96-5B57413B75B3","lat":"32.087298","token":"bi","height":750,"uniqueKey":"c6777549d3dca9d907271ee6ac3d189df00fdb49","lng":"118.882238","locateCityCode":"1602"}'

        response = interface_test('portal_app_channel_index_跟团',params,env)
        if response['success'] is True and response['data'] is not None:

            # 1, 轮播图区块检查
            if len(response['data']['slider']['contents']) > 0:
                for i in response['data']['slider']['contents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

            # 2，爆款特价区块检查
            if len(response['data']['flashSales']['saleContents']) >0:
                for i in response['data']['flashSales']['saleContents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

            # 3，热玩主题区块检查
            if len(response['data']['choices']['contents']) >0:
                for i in response['data']['choices']['contents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

            # 4，特色跟团区块检查
            if len(response['data']['featuredCategory']['contents']) >0:
                for i in response['data']['featuredCategory']['contents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

        elif response['success'] is True and response['data'] is None:
            value_err.append(('portal_app_channel_index_跟团','接口返回data数据为null'))
        else:
            value_err.append(('portal_app_channel_index_跟团',response['msg']))

        if len(value_err)>0:
            print(sys._getframe().f_code.co_name,'校验 False','失败详情如下：\n')
            for err in value_err:
                print(err)
            print('~~~ The End ~~~~~')
        else:
            print(sys._getframe().f_code.co_name,'校验：Success')

        self.assertEqual(value_err,[],msg = '存在校验失败结果')

    @data(*cityCode)
    def test_自由行频道页(self,cityCode):
        value_err = []
        regex_expression = "(http|https)://((m|m\d)\.tuniucdn.com|m.tuniucdn.com|s.tuniu.net|img3.tuniucdn.com)/\S+.(jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF|(/w/\d+/h/\d+))$"
        params = 'c={"cc":'+str(cityCode[0])+',"ct":10,"p":14588,"ov":20,"dt":0,"v":"'+version +'"}&d={"productPageId":2060,"channelType":5,"pageId":3483,"width":750,"bookCityName":"'+cityCode[1]+'","tact":"9EA881B7-E104-412A-BD96-5B57413B75B3","lat":"32.087298","token":"bi","height":750,"uniqueKey":"c6777549d3dca9d907271ee6ac3d189df00fdb49","lng":"118.882238","locateCityCode":"1602"}'

        response = interface_test('portal_app_channel_index',params,env)
        if response['success'] is True and response['data'] is not None:

            # 1, 轮播图区块检查
            if response['data']['slider']['contents'] is not None and \
                            len(response['data']['slider']['contents']) > 0:
                for i in response['data']['slider']['contents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

            # 2，爆款特价区块检查
            if response['data']['flashSales'] is not None and \
                            len(response['data']['flashSales']['saleContents']) >0:
                for i in response['data']['flashSales']['saleContents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

            # 3，热玩主题区块检查
            if response['data']['choices'] is not None and\
                            len(response['data']['choices']['contents']) >0:
                for i in response['data']['choices']['contents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

        elif response['success'] is True and response['data'] is None:
            value_err.append(('portal_app_channel_index_自由行','接口返回data数据为null'))
        else:
            value_err.append(('portal_app_channel_index_自由行',response['msg']))

        if len(value_err)>0:
            print(sys._getframe().f_code.co_name,'校验 False','失败详情如下：\n')
            for err in value_err:
                print(err)
            print('~~~ The End ~~~~~')
        else:
            print(sys._getframe().f_code.co_name,'校验：Success')

        self.assertEqual(value_err,[],msg = '存在校验失败结果')

    @data(*cityCode)
    def test_酒加景频道页(self,cityCode):
        value_err = []
        regex_expression = "(http|https)://((m|m\d)\.tuniucdn.com|m.tuniucdn.com|s.tuniu.net|img3.tuniucdn.com)/\S+.(jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF|(/w/\d+/h/\d+))$"
        params = 'c={"cc":'+str(cityCode[0])+',"ct":10,"p":14588,"ov":20,"dt":0,"v":"'+version +'"}&d={"productPageId":0,"channelType":6,"pageId":3332,"width":750,"bookCityName":"'+cityCode[1]+'","tact":"9EA881B7-E104-412A-BD96-5B57413B75B3","lat":"32.087298","token":"bi","height":750,"uniqueKey":"c6777549d3dca9d907271ee6ac3d189df00fdb49","lng":"118.882238","locateCityCode":"1602"}'

        response = interface_test('portal_app_channel_index',params, env)
        print("response:",response)
        if response['success'] is True and response['data'] is not None:

            # 1, 轮播图区块检查
            if response['data']['slider'] is not None and \
                            len(response['data']['slider']['contents']) > 0:
                for i in response['data']['slider']['contents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

            # 2，本周特价区块检查
            if response['data']['flashSales']['saleContents'] is not None and \
                            len(response['data']['flashSales']['saleContents']) >0:
                for i in response['data']['flashSales']['saleContents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

            # 3，主题游区块检查
            if response['data']['themeAndTopic'] is not None and\
                            len(response['data']['themeAndTopic']['contents']) >0:
                for i in response['data']['themeAndTopic']['contents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2
            #4,轮播图下产品卡区块
            if response['data']['destinationTab']['categoryList'] is not None and\
                len(response['data']['destinationTab']['categoryList'])>0:
                for i in response['data']['destinationTab']['categoryList']:
                    if i['destinationList'] is not None and len(i['destinationList'])>0:
                        for j in i['destinationList']:
                            result = re_valueCheck(j['imgUrl'],regex_expression)
                            value_err = value_err + result
                            if result == []:
                                result2 = url_request_test(j['imgUrl'])
                                value_err = value_err + result2

        elif response['success'] is True and response['data'] is None:
            value_err.append(('portal_app_channel_index_酒+景','接口返回data数据为null'))
        else:
            value_err.append(('portal_app_channel_index_酒+景',response['msg']))

        if len(value_err)>0:
            print(sys._getframe().f_code.co_name,'校验 False','失败详情如下：\n')
            for err in value_err:
                print(err)
            print('~~~ The End ~~~~~')
        else:
            print(sys._getframe().f_code.co_name,'校验：Success')

        self.assertEqual(value_err,[],msg = '存在校验失败结果')


    @data(*cityCode)
    def test_私家团频道页(self,cityCode):
        value_err = []
        regex_expression = "(http|https)://((m|m\d)\.tuniucdn.com|m.tuniucdn.com|s.tuniu.net|img3.tuniucdn.com)/\S+.(jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF|(/w/\d+/h/\d+))$"
        params = 'c={"cc":'+str(cityCode[0])+',"ct":10,"p":14588,"ov":20,"dt":0,"v":"'+version +'"}&d={"productPageId":0,"channelType":9,"pageId":3705,"width":750,"bookCityName":"'+cityCode[1]+'","tact":"9EA881B7-E104-412A-BD96-5B57413B75B3","lat":"32.087298","token":"bi","height":750,"uniqueKey":"c6777549d3dca9d907271ee6ac3d189df00fdb49","lng":"118.882238","locateCityCode":"1602"}'

        response = interface_test('portal_app_channel_index',params, env)
        if response['success'] is True and response['data'] is not None:

            # 1, 轮播图区块检查
            if response['data']['slider'] is not None and \
                            len(response['data']['slider']['contents']) > 0:
                for i in response['data']['slider']['contents']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

            # 2，轮播图下方产品卡区块检查
            if response['data']['destinationTab2Wrapper1'] is not None and \
                            len(response['data']['destinationTab2Wrapper1']['destinationTab2']) >0:
                for i in response['data']['destinationTab2Wrapper1']['destinationTab2']:
                    for j in i['contents'][0]['destinationsWithPic']:
                        result = re_valueCheck(j['imgUrl'],regex_expression)
                        value_err = value_err + result
                        if result == []:
                            result2 = url_request_test(j['imgUrl'])
                            value_err = value_err + result2

        elif response['success'] is True and response['data'] is None:
            value_err.append(('portal_app_channel_index_私家团','接口返回data数据为null'))
        else:
            value_err.append(('portal_app_channel_index_私家团',response['msg']))

        if len(value_err)>0:
            print(sys._getframe().f_code.co_name,'校验 False','失败详情如下：\n')
            for err in value_err:
                print(err)
            print('~~~ The End ~~~~~')
        else:
            print(sys._getframe().f_code.co_name,'校验：Success')

        self.assertEqual(value_err,[],msg = '存在校验失败结果')

    @data(*cityCode)
    def test_首页猜你喜欢(self,cityCode):
        value_err = []
        regex_expression = "(http|https)://((m|m\d)\.tuniucdn.com|m.tuniucdn.com|s.tuniu.net|img3.tuniucdn.com)/\S+.(jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF|(/w/\d+/h/\d+))$"
        params = 'c={"cc":'+str(cityCode[0])+',"ct":10,"p":14588,"ov":20,"dt":0,"v":"'+version +'"}&d={"needDestination":true,"adPlan":"BI","isAbroad":false,"tact":"9EA881B7-E104-412A-BD96-5B57413B75B3","width":750,"bookCityName":"'+cityCode[1]+'","needFlashSale":true,"foreignCC":"'+str(cityCode[0])+'","locatePoiId":"1602","isChanged":true,"token":"bi","saleSpecialPlan":"BI","saleFlightPlan":"BI","height":1334,"uniqueKey":"c6777549d3dca9d907271ee6ac3d189df00fdb49","did":"OUVBODgxQjctRTEwNC00MTJBLUJEOTYtNUI1NzQxM0I3NUIz"}'

        response = interface_test('guessLike',params,env)
        if response['success'] is True and response['data'] is not None:

            # 1, 超值特卖区块检查
            if response['data']['flashSale']['special'] is not None:
                result = re_valueCheck(response['data']['flashSale']['special']['imgUrl'],regex_expression)
                value_err = value_err + result
                if result == []:
                    result2 = url_request_test(response['data']['flashSale']['special']['imgUrl'])
                    value_err = value_err + result2
                #下面校验跳转连接
                result = re_valueCheck(response['data']['flashSale']['special']['url'],'(http|https)\S+')
                value_err = value_err + result
                if result == []:
                    result2 = url_request_test(response['data']['flashSale']['special']['url'])
                    value_err = value_err + result2

            # 2，超值特卖区块 -- 周末酒店 图片检查
            if response['data']['flashSale']['weekendHotel'] is not None:
                result = re_valueCheck(response['data']['flashSale']['weekendHotel']['imgUrl'],regex_expression)
                value_err = value_err + result
                if result == []:
                    result2 = url_request_test(response['data']['flashSale']['weekendHotel']['imgUrl'])
                    value_err = value_err + result2
                #下面校验跳转连接
                result = re_valueCheck(response['data']['flashSale']['weekendHotel']['url'],'(http|https)\S+')
                value_err = value_err + result
                if result == []:
                    result2 = url_request_test(response['data']['flashSale']['weekendHotel']['url'])
                    value_err = value_err + result2
            # 3，超值特卖区块 -- 自由行产品 图片检查
            if response['data']['flashSale']['diy'] is not None:
                result = re_valueCheck(response['data']['flashSale']['diy']['imgUrl'],regex_expression)
                value_err = value_err + result
                if result == []:
                    result2 = url_request_test(response['data']['flashSale']['diy']['imgUrl'])
                    value_err = value_err + result2
                #下面校验跳转连接
                result = re_valueCheck(response['data']['flashSale']['diy']['url'],'(http|https)\S+')
                value_err = value_err + result
                if result == []:
                    result2 = url_request_test(response['data']['flashSale']['diy']['url'])
                    value_err = value_err + result2

            # 4，超值特卖区块 -- 跟团产品 图片检查
            if response['data']['flashSale']['diy'] is not None:
                result = re_valueCheck(response['data']['flashSale']['tours']['imgUrl'],regex_expression)
                value_err = value_err + result
                if result == []:
                    result2 = url_request_test(response['data']['flashSale']['tours']['imgUrl'])
                    value_err = value_err + result2
                #下面校验跳转连接
                result = re_valueCheck(response['data']['flashSale']['tours']['url'],'(http|https)\S+')
                value_err = value_err + result
                if result == []:
                    result2 = url_request_test(response['data']['flashSale']['tours']['url'])
                    value_err = value_err + result2

            # 5，超值特卖区块 -- 底部跳转链接检查
            if response['data']['flashSale']['bottom'] is not None and\
                    len(response['data']['flashSale']['bottom'])>0:
                for i in response['data']['flashSale']['bottom']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2
                    #下面校验跳转连接
                    result = re_valueCheck(i['url'],'(http|https)\S+')
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['url'])
                        value_err = value_err + result2

            # 6，目的地推荐区块 检查
            if response['data']['destRecommend']['destinations'] is not None and\
                    len(response['data']['destRecommend']['destinations'])>0:
                for i in response['data']['destRecommend']['destinations']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

            #7，目的地推荐区块bottom检查
            if response['data']['destRecommend']['bottom'] is not None and\
                    len(response['data']['destRecommend']['bottom'])>0:
                for i in response['data']['destRecommend']['bottom']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2

        elif response['success'] is True and response['data'] is None:
            value_err.append(('guessLike','接口返回data数据为null'))
        else:
            value_err.append(('guessLike',response['msg']))

        if len(value_err)>0:
            print(sys._getframe().f_code.co_name,'校验 False','失败详情如下：\n')
            for err in value_err:
                print(err)
            print('~~~ The End ~~~~~')
        else:
            print(sys._getframe().f_code.co_name,'校验：Success')

        self.assertEqual(value_err,[],msg = '存在校验失败结果')


    @data(*cityCode)
    def test_首页宫格数据(self,cityCode):
        value_err = []
        regex_expression = "(http|https)://((m|m\d)\.tuniucdn.com|m.tuniucdn.com|s.tuniu.net|img3.tuniucdn.com)/\S+.(jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF|(/w/\d+/h/\d+))$"
        params = 'c={"cc":'+str(cityCode[0])+',"ct":10,"p":14588,"ov":20,"dt":0,"v":"'+version +'"}&d={"height":1334,"did":"OUVBODgxQjctRTEwNC00MTJBLUJEOTYtNUI1NzQxM0I3NUIz","policies":{"41":"新频道页","34":"原频道页","29":"unknown","37":"原频道页","32":"原频道页","35":"原频道页","30":"原频道页","33":"原频道页","28":"unknown","36":"原频道页","31":"原频道页"},"uniqueKey":"c6777549d3dca9d907271ee6ac3d189df00fdb49","localCityCode":"1602","width":750,"bookCityName":"'+cityCode[1]+'","clientModel":"iPhone 6s","lng":118.8822740417081,"lat":32.08731194139533}'

        response = interface_test('portal_home_data_index',params,env)
        if response['success'] is True and response['data'] is not None:

            # 1, 首页轮播图
            if response['data']['advertises'] is not None and\
                    len(response['data']['advertises']) > 0:
                for i in response['data']['advertises']:
                    result = re_valueCheck(i['image'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['image'])
                        value_err = value_err + result2
                    result = re_valueCheck(i['url'],'(http)\S+')
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['url'])
                        value_err = value_err + result2

            # 2, 首页宫格检查
            if response['data']['categoryNew'] is not None and\
                    len(response['data']['categoryNew']) > 0:
                for i in response['data']['categoryNew']:
                    for j in i['ads']:
                        result = re_valueCheck(j['imgUrl'],regex_expression)
                        value_err = value_err + result
                        if result == []:
                            result2 = url_request_test(j['imgUrl'])
                            value_err = value_err + result2
            #3,小品类入口检查
            if response['data']['smallCategory'] is not None and \
                len(response['data']['smallCategory']['content'])>0:
                for i in response['data']['smallCategory']['content']:
                    result = re_valueCheck(i['imgUrl'],regex_expression)
                    value_err = value_err + result
                    if result == []:
                        result2 = url_request_test(i['imgUrl'])
                        value_err = value_err + result2
        elif response['success'] is True and response['data'] is None:
            value_err.append(('portal_home_data_index','接口返回data数据为null'))
        else:
            value_err.append(('portal_home_data_index',response['msg']))

        if len(value_err)>0:
            print(sys._getframe().f_code.co_name,'校验 False','失败详情如下：\n')
            for err in value_err:
                print(err)
            print('~~~ The End ~~~~~')
        else:
            print(sys._getframe().f_code.co_name,'校验：Success')

        self.assertEqual(value_err,[],msg = '存在校验失败结果')

    @data(*page)
    def test_首页瀑布流v3(self,page):
        value_err = []
        regex_expression = "(http|https)://((m|m\d)\.tuniucdn.com|m.tuniucdn.com|s.tuniu.net|img3.tuniucdn.com)/\S+.(jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF|(/w/\d+/h/\d+))$"
        params = 'c={"cc":'+str(page[0])+',"ct":10,"p":14588,"ov":20,"dt":0,"v":"'+version +'"}&d={"pageLimit":10,"bottomOffset":-1,"currentPage":'+str(page[1])+',"needPlay":true,"width":750,"deviceNum":"c6777549d3dca9d907271ee6ac3d189df00fdb49","getRecommendFlag":false,"moduleName":"全部","moduleId":"15539527","abTest":"bi","sessionId":"04da2fed402d55d1061caa4c1b29433f_","uniqueKey":"9EA881B7-E104-412A-BD96-5B57413B75B3","isFirst":true}'
        response = interface_test('portal_home_list_v3',params,env)
        if response['success'] is True and response['data'] is not None:

            # 1, 首页轮播图
            if response['data']['items'] is not None and\
                    len(response['data']['items']) > 0:
                for i in response['data']['items']:
                    if i['type'] == 1:
                        result = re_valueCheck(i['product']['imgUrl'],regex_expression)
                        value_err = value_err + result
                        if result == []:
                            result2 = url_request_test(i['product']['imgUrl'])
                            value_err = value_err + result2
                    elif i['type'] == 2:
                        if i['content']['coverImgUrl'] is not None:
                            result = re_valueCheck(i['content']['coverImgUrl'],regex_expression)
                            value_err = value_err + result
                            if result == []:
                                result2 = url_request_test(i['content']['coverImgUrl'])
                                value_err = value_err + result2

                        if i['content']['imageUrls'] is not None and\
                            len(i['content']['imageUrls']) > 0:
                            for j in i['content']['imageUrls']:
                                result = re_valueCheck(j,regex_expression)
                                value_err = value_err + result
                                if result == []:
                                    result2 = url_request_test(j)
                                    value_err = value_err + result2
        elif response['success'] is True and response['data'] is None:
            value_err.append(('portal_home_list_v3','接口返回data数据为null'))
        else:
            value_err.append(('portal_home_list_v3',response['msg']))

        if len(value_err)>0:
            print(sys._getframe().f_code.co_name,'校验 False','失败详情如下：\n')
            for err in value_err:
                print(err)
            print('~~~ The End ~~~~~')
        else:
            print(sys._getframe().f_code.co_name,'校验：Success')

        self.assertEqual(value_err,[],msg = '存在校验失败结果')


if __name__ == '__main__':
    #全部case执行
    # unittest.main()

    #执行某个case
    # test_runner = unittest.TextTestRunner()
    test_suite = unittest.TestSuite()
    test_suite.addTest(mob_portal('test_出境游频道页'))
    test_result = unittest.TextTestRunner().run(test_suite)
    # unittest.TextTestRunner(verbosity=2).run(test_suite)