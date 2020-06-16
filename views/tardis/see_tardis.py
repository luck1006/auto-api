# -*- coding: utf-8 -*-
import json
from bs4 import BeautifulSoup
import re
import time
import requests
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from app.actions.tools.secret import decrypt


class Tardis():
    def tardis_cookies(self, user_name, user_pw, url='https://tardis.tuniu.io/systems'):
        try:
            executable_path = "../../static/chromedriver_linux"
            c_service = Service(executable_path)
            c_service.command_line_args()
            c_service.start()
        except:
            executable_path = "../../static/chromedriver_mac"
            c_service = Service(executable_path)
            c_service.command_line_args()
            c_service.start()
        finally:
            browser = webdriver.Chrome(executable_path)
            # browser.maximize_window()  # 窗口最大化
        try:
            browser.get(url)
            # time.sleep(2)
            browser.find_element_by_id('username').send_keys(user_name)
            browser.find_element_by_id('password').send_keys(user_pw)
            browser.find_element_by_name('submit').click()
            cookie = browser.get_cookies()
            for i in cookie:
                if i['name'] == 'PHPSESSID':
                    break
            PHPSESSID = i['value']
            print(cookie)
            browser.quit()
            c_service.stop()
            return PHPSESSID
        except Exception as e:
            print("PHPSESSID 异常", e)


class TardisSysLog():

    def __init__(self, sessionId, tag, key_word):
        self.PHPSESSID = sessionId
        self.tag = tag
        self.key_word = key_word
        self.headers = {
            'Connection': "keep-alive",
            'Cache-Control': "max-age=0",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cookie': f"PHPSESSID={self.PHPSESSID}",
            'Host': "tardis.tuniu.io",
            'cache-control': "no-cache"
        }
        with open('file.txt', 'w') as f:
            print('新建或清空文件')

    def sys_log_ids(self):
        tomcat = ["/opt/tuniu/logs/tomcat/app/tomcat_mob_reward/reward.log",
                  "/opt/tuniu/logs/tomcat/app/tomcat_mob_hercules/mob_hercules.log",
                  "/opt/tuniu/logs/tomcat/app/tomcat_mob_energy/energy.log",
                  "/opt/tuniu/logs/tomcat/app/tomcat_mall_prd/prd.log",
                  "/opt/tuniu/logs/tomcat/app/tomcat_mall_ord/ord.log"
                  ]
        url = "https://tardis.tuniu.io/systems/logrecords/getrawloginfo"
        querystring = {"SystemName": f"{self.tag}"}
        response = requests.get(url, headers=self.headers, params=querystring)
        soup = BeautifulSoup(response.text, 'lxml')
        # 本想解析html 但使用起来正则更简单
        r = re.findall('JSON.parse\(\'([\\s\\S]*?)\'\)', str(soup))[0]
        r = json.loads(r)
        ids = []
        for i in r:
            if i in tomcat:
                for y in r[i]:
                    for w in r[i][y]:
                        id = r[i][y][w]
                        ids.append(id)
            # break  # 第一个就是需要的 不是要自己写逻辑

        return ids

    def logs(self, ids):
        resp = []
        for id in ids:
            self.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            start_id = 1
            end_id = 1000
            end = 1
            page = 1
            while end > 0:
                url = 'https://tardis.tuniu.io/systems/logrecords/getrawlogsdata'
                payload = f"LogId={id}&ActionType=&SearchString={self.key_word}&StartLine={start_id}&EndLine={end_id}"
                response = requests.post(url, data=payload, headers=self.headers)
                # print(id, page)
                with open("file.txt", "a+") as f:
                    f.write(response.text)
                end = len(response.text)
                print(id, page, end)
                page += 1
                start_id += 1000
                end_id += 1000
                if page > 100 or 'Get log error' in response.text:
                    break
                with open("file.txt", "a+") as f:
                    f.write(response.text)
        with open("file.txt", "r") as f:
            for i in f:
                try:
                    k = i.split(' - ')[1]
                    resp.append(k)
                except Exception as e:
                    resp.append(i)

        l = list(set(resp))
        data = []
        for ii in l:
            res = (ii, resp.count(ii))
            data.append(res)
        data.sort(key=lambda k: k[1], reverse=True)
        return data


if __name__ == '__main__':
    sessionId = Tardis().tardis_cookies(decrypt('e28f4f661afa2f6ae905ccba89e42dc7'),
                                        decrypt('60fcc539746f3cd74d9cd1f8c65700bc'))
    print(sessionId)
    # PHPSESSID = 'tgea6pehn1otuf7p8kvv6tn8g4'
    # TAG = 'mob-hercules-prd'
    # time1 = time.time()
    # d = TardisSysLog(PHPSESSID, TAG, 'ception')
    # ids = d.sys_log_ids()
    # data = d.logs(ids)
    # data = json.dumps(data)
    # print(data)
    # time2 = time.time()
    # print(time2 - time1)
    # pass
    # time1 =time.time()
