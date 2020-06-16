#  -*-  coding: utf-8  -*-

import requests
from views.tardis.see_tardis import Tardis
from app.actions.tools.secret import decrypt
from bs4 import BeautifulSoup

sessionId = Tardis().tardis_cookies(decrypt('e28f4f661afa2f6ae905ccba89e42dc7'),
                                    decrypt('60fcc539746f3cd74d9cd1f8c65700bc'),
                                    url='http://oa.tuniu.com/index.php?m=OaTuniuRoom%2Cadmin&floor_id=15&attr=0&name=&add_user=&search=%E6%90%9C%E7%B4%A2')

url = "http://oa.tuniu.com/index_ajax.php?m=OaTuniuRoomOrderAjax,admin,batch_order_room"
# 约旦200
room_id = 200

date = '2020-01-06'
bt = '13:00'
et = "15:00"
subject = '需求评审'

payload = f'room_id={room_id}&dep=系统产品研发BU&user=孙传鑫&subject={subject}&attend_num=10&type=1&begin_time={date} {bt}&end_time={date} {et}'
headers = {
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Origin': 'http://oa.tuniu.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://oa.tuniu.com/index.php?m=OaTuniuRoom%2Cadmin&floor_id=15&attr=0&name=&add_user=&search=%E6%90%9C%E7%B4%A2',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': F'PHPSESSID={sessionId}; tuniu_crm_user=c3VuY2h1YW54aW4%3D; tuniu_crm=MTQ0NDgsMSwyLDM%3D'
}

s = requests.session()
response = s.request("POST", url, headers=headers, data=payload.encode())

print(response.text)

url = f"http://oa.tuniu.com/index.php?m=OaTuniuRoomOrder,admin&floor_id=0&room_id=0&attr=0&type=0&time=0&begin_date={date}&end_date={date}&dep=&user=孙传鑫&add_user=&search=搜索"
res = s.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'lxml')
for idx, tr in enumerate(soup.find_all('tr')):
    tds = tr.find_all('td')
    print([i.text for i in tds[:9]])
