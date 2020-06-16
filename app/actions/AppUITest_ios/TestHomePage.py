from appium import webdriver
import unittest
import os
import time
from appium.webdriver.common.touch_action import TouchAction
from app.actions.AppUITest_ios.com_function import Expected_result_check


class TuniuApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        desire_app = {
            'platformName': 'iOS',
            'platformVersion': '12.4',
            'deviceName': '孙先江的iPhone',
            'udid': '0dc6f9aadee698f5c506afa1ddca221d266d1020',
            'bundleId': 'com.tuniu.app',
            'unicodeKeyboard': True,
            'resetKeyboard': True
        }

        cls.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desire_app)
        #time.sleep(5)
        cls.driver.implicitly_wait(20)


    def test_1机票(self):
        ticket = self.driver.find_element_by_ios_predicate("name == '机票' and type == 'XCUIElementTypeStaticText'")
        action = TouchAction(self.driver)
        action.tap(ticket).perform().release()
        time.sleep(4)

        if self.driver.page_source.find(u'单程') != -1:
            result = True
            print('success')
            # 返回首页
            ticket_back = self.driver.find_element_by_ios_predicate(
                "name = 'airplane ticket home topLeft b' and type = 'XCUIElementTypeButton'")
            action = TouchAction(self.driver)
            action.tap(ticket_back).perform().release()
            time.sleep(3)
        else:
            result = False
            print('failed')
        self.assertTrue(result)


    def test_2酒店(self):
        ticket = self.driver.find_element_by_ios_predicate("name == '酒店' and type == 'XCUIElementTypeStaticText'")
        action = TouchAction(self.driver)
        action.tap(ticket).perform().release()
        time.sleep(4)

        if self.driver.page_source.find(u'境内/出境·中国港澳台') != -1:
            result = True
            print('success')
            # 返回首页
            ticket_back = self.driver.find_element_by_ios_predicate(
                "name = 'hotel home back white backgrou' and type = 'XCUIElementTypeButton'")
            action = TouchAction(self.driver)
            action.tap(ticket_back).perform().release()
            time.sleep(3)
        else:
            result = False
            print('failed')
        self.assertTrue(result)


    def test_3火车票(self):
        ticket = self.driver.find_element_by_ios_predicate("name == '火车票' and type == 'XCUIElementTypeStaticText'")
        action = TouchAction(self.driver)
        action.tap(ticket).perform().release()
        time.sleep(4)

        if self.driver.page_source.find(u'火车票') != -1:
            result = True
            print('success')
            # 返回首页
            # ticket_back = self.driver.find_element_by_ios_predicate(
            #     "id = '51010000-0000-0000-7601-000000000000' and type = 'XCUIElementTypeButton'")
            ticket_back = self.driver.find_element_by_xpath('//XCUIElementTypeApplication[@name="途牛旅游"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeButton')
            action = TouchAction(self.driver)
            action.tap(ticket_back).perform().release()
            time.sleep(3)
        else:
            result = False
            print('failed')
        self.assertTrue(result)

    # def test_4门票(self):
    #     ticket = self.driver.find_element_by_ios_predicate("name == '门票' and type == 'XCUIElementTypeStaticText'")
    #     action = TouchAction(self.driver)
    #     action.tap(ticket).perform().release()
    #     time.sleep(4)
    #
    #     if self.driver.page_source.find(u'火车票') != -1:
    #         result = True
    #         print('success')
    #         # 返回首页
    #         # ticket_back = self.driver.find_element_by_ios_predicate(
    #         #     "id = '51010000-0000-0000-7601-000000000000' and type = 'XCUIElementTypeButton'")
    #         ticket_back = self.driver.find_element_by_xpath('//XCUIElementTypeApplication[@name="途牛旅游"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeButton')
    #         action = TouchAction(self.driver)
    #         action.tap(ticket_back).perform().release()
    #         time.sleep(3)
    #     else:
    #         result = False
    #         print('failed')
    #     self.assertTrue(result)

    def test_5用车汽车(self):
        ticket = self.driver.find_element_by_ios_predicate("name == '用车/汽车' and type == 'XCUIElementTypeStaticText'")
        action = TouchAction(self.driver)
        action.tap(ticket).perform().release()
        time.sleep(4)

        if self.driver.page_source.find(u'国内用车') != -1:
            result = True
            print('success')
            # 返回首页
            # ticket_back = self.driver.find_element_by_ios_predicate(
            #     "id = '51010000-0000-0000-7601-000000000000' and type = 'XCUIElementTypeButton'")
            ticket_back = self.driver.find_element_by_xpath('//XCUIElementTypeApplication[@name="途牛旅游"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeButton')
            action = TouchAction(self.driver)
            action.tap(ticket_back).perform().release()
            time.sleep(3)
        else:
            result = False
            print('failed')
        self.assertTrue(result)




    def test_cityLocate(self):
        city = self.driver.find_element_by_ios_predicate("name == 'icon home locationTriangle gre' and type == 'XCUIElementTypeButton'")
        action = TouchAction(self.driver)
        action.tap(city).perform().release()
        time.sleep(4)

    def test_mind(self):

        mind = self.driver.find_element_by_ios_predicate("name == '我的' and type == 'XCUIElementTypeButton'")
        print('mind: ', mind)
        action = TouchAction(self.driver)
        print('action: ',action)
        #self.driver.excute_script("mobile: tap", {'element': mind})

        action.tap(mind,302,619).perform().release()
        time.sleep(4)

        if Expected_result_check().is_element_exist(self.driver, "账号密码登录"):
            password_login = self.driver.find_element_by_ios_predicate("name == '账号密码登录'")
            action = TouchAction(self.driver)
            action.tap(password_login).perform().release()
            time.sleep(4)
            self.driver.find_element_by_ios_predicate("value == '手机号/会员名/昵称/邮箱' and type == 'XCUIElementTypeTextField'").send_keys('13062527068')
            self.driver.find_element_by_ios_predicate("value == '密码' and type == 'XCUIElementTypeTextField'").send_keys("tuniu520")
            time.sleep(2)
            self.driver.find_element_by_accessibility_id('登录')
            time.sleep(3)

        if self.driver.page_source.find(u'我的订单') != -1:
            result = True
            print('success')
        else:
            result = False
            print('failed')

        self.assertTrue(result)
        print('aaaaaa')

    def test_2(self):
        print('bbbbbb')




if __name__ == '__main__':
    unittest.main()