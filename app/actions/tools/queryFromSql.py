# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging


class queryFromSql(object):

    def __init__(self, Dbname, sql, export=0):
        self.sql = sql
        self.Dbname = Dbname
        self.export = export

    # @pysnooper.snoop('log.log')
    def querySql(self):
        '''
        :param Dbname:
        :param sql:
        :return:list  以[[],[]...] 的形式返回数据
        '''
        url = "http://newsqladmin.tuniu.org/sqladmin"
        headers = {
            'Referer'
            'Connection': "keep-alive",
            'Pragma': "no-cache",
            'Cache-Control': "no-cache",
            'Origin': "http://newsqladmin.tuniu.org",
            'Upgrade-Insecure-Requests': "1",
            'Content-Type': "application/x-www-form-urlencoded",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'Referer': "http://newsqladmin.tuniu.org/sqladmin",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cookie': "username=xingenlu",
            'cache-control': "no-cache"
        }
        if self.Dbname in ['d_mall_booking', 'd_mall_ord', 'd_mall_prd']:
            headers['Cookie'] = 'username=liutaotao'
        times = 0
        endId = 30
        data = []
        key = []
        idx = 0
        logging.info(self.sql)
        while endId == 30:
            logging.info(f'计数{times}')
            # newsqladmin 每次最大返回100条数据,现在30了
            startId = times * 30
            if "limit" not in self.sql:
                Sqlstr = self.sql + f" limit {startId} , 30 "
            else:
                Sqlstr = self.sql
            payload = {
                "Dbname": self.Dbname,
                "Sqlstr": Sqlstr,
                "Sqlstr_hide": Sqlstr
            }
            retry = 0
            time1 = time.time()
            try:
                response = requests.post(url, payload, headers=headers)
                time.sleep(0.5)
                while response.status_code != 200 or 'newsqladmin自动kill' in str(response.content, 'utf8'):
                    time.sleep(1)
                    response = requests.post(url, payload, headers=headers)
                    retry += 1
                    logging.info(f"retry{retry}次")
                    if retry > 10:
                        break
            except Exception as e:
                logging.exception(f'exception: {response.text}')
                raise e
            time2 = time.time()
            t = time2 - time1
            logging.info(f'耗时: {t}s ')
            soup = BeautifulSoup(response.text, 'lxml')

            # 优化点 后边再看
            # resultset = soup.select('#qryresult tr')
            # print(resultset)

            for idx, tr in enumerate(soup.find_all('tr')):
                tds = tr.find_all('td')
                list = []
                if idx != 0:
                    for c in tds[1:]:
                        # 一堆数据库报错信息的再解释
                        if 'newsqladmin自动kill' in c.text:
                            list.append('查询超时，请优化')
                        elif '执行select语句失败' in c.text:
                            list.append('查询失败，请检查')
                        elif '无该数据库的访问权限' in c.text:
                            list.append('无权限')
                        else:
                            list.append(c.text)
                    data.append(list)
                elif startId == 0:
                    for c in tds[1:]:
                        key.append(c.text)
                    data.append(key)
            endId = idx
            times = times + 1
            # 非jira库 最多查询100条
            if 'limit' in self.sql.lower():
                break
            if self.Dbname == 'jira' or self.export == 1:
                pass
            else:
                break
        return data

    def tokv(self, data):
        '''
        :param data: [[data1],[],[],...]
        :return: [{key1:value1,...},{},...] key为data1
        '''
        list = []
        keyList = data[0]
        for i in data:
            if i != keyList:
                c = dict(zip(keyList, i))
                list.append(c)
        return list

    def sqlToList(self):
        data = queryFromSql(self.Dbname, self.sql)
        data = data.querySql()
        res = queryFromSql.tokv(self, data)
        return res

    def toexcel(self, sheet_name='Sheet1'):
        data = queryFromSql(self.Dbname, self.sql, 1).querySql()
        df = pd.DataFrame(data[1:], columns=data[0])
        writer = pd.ExcelWriter('result.xlsx')
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        writer.save()

    def toechart(self):
        d = queryFromSql(self.Dbname, self.sql, self.export).querySql()
        d = list(zip(*d))
        return d
