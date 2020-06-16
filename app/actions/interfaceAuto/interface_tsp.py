import base64
import json, requests

tsp_config = {
    "sit": {
        "ip_url": "http://public-api.pla.tuniu-sit.org/tsg/register/service/address/query",
        "path_url": "http://public-api.pla.tuniu-sit.org/tsg/register/service/get",
        "headers": {"Referer": "http://tsp.sit.tuniu.org/PLA/TSG/view/serviceDetail.html?e25hbWU6J0JPSC5OTS5Qcm9kdWN0RG9tYWluQ29udHJvbGxlci5nZXRQcmRCYXNpY0luZm8nfQ==",
           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    },
    "pre": {
        "ip_url": "http://public-api.bj.pla.tuniu.org/tsg/register/service/address/query",
        "path_url": "http://public-api.bj.pla.tuniu.org/tsg/register/service/get",
        "headers": {"Referer": "http://boss.tuniu.org/PLA/TSG_BJ/view/serviceDetail.html?e25hbWU6J01PQi5CQVRDSC5TZWFyY2hMaXN0Q29udHJvbGxlci5jcnVpc2VMaXN0Rm9yUGMnfQ==",
           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
    },
    "prd": {
        "ip_url": "http://public-api.bj.pla.tuniu.org/tsg/register/service/address/query",
        "path_url": "http://public-api.bj.pla.tuniu.org/tsg/register/service/get",
        "headers": {"Referer": "http://boss.tuniu.org/PLA/TSG_BJ/view/serviceDetail.html?e25hbWU6J01PQi5CQVRDSC5TZWFyY2hMaXN0Q29udHJvbGxlci5jcnVpc2VMaXN0Rm9yUGMnfQ==",
           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
    }
}

class TspSearch():
    def __init__(self,name,env='sit'):
        #初始化各环境下tsp服务的ip\路由查询接口信息
        self.name = name
        self.ip_url = tsp_config[env]["ip_url"]
        self.path_url = tsp_config[env]["path_url"]
        self.headers = tsp_config[env]["headers"]

    #将ip信息与路由信息合并在一起
    def tsp2interface(self):
        d1 = self.ip_search()
        d2 = self.path_search()
        if d1 != None and d2 !=None:
            d1.update(d2)
            return json.dumps(d1,ensure_ascii=False)
        else:
            return None

    # 查询tsp服务的ip信息
    def ip_search(self):
        params = {"uid":"28287","token":"","nickname":"董芳芳","r":0.3367168862444896,"name":self.name,"start":0,"limit":10,"sortname":"","sortorder":""}
        params = base64.b64encode(json.dumps(params).encode('utf-8'))
        response = requests.session().get(self.ip_url, params=params, headers=self.headers)
        response_text = response.text+'=='
        response_decode =json.loads(str(base64.b64decode(response_text), 'utf-8'))
        print(response_decode)
        if response_decode['data']['rows'] not in (None,'',[]):
            return {"interface_name":self.name,"ip":response_decode['data']['rows'][0]["providerAddress"]}
        else:
            #若未查询到tsp对应的ip，则返回None
            return None

    #查询tsp服务的路由path信息
    def  path_search(self):
        params = {"uid":"28287","token":"","nickname":"董芳芳","r":0.1223202485042969,"name":self.name}
        params = base64.b64encode(json.dumps(params).encode('utf-8'))
        response = requests.session().get(self.path_url, params=params, headers=self.headers)
        response_text = response.text+'=='
        response_decode =json.loads(str(base64.b64decode(response_text), 'utf-8'))
        print(response_decode)
        if response_decode['data']['rows'] not in (None,'',[]):
            return {"path":response_decode['data']['rows'][0]["mapping"],"method":response_decode['data']['rows'][0]["method"],"interface_comment":response_decode['data']['rows'][0]["description"]}
        else:
            #若未查询到tsp对应的路由，则返回None
            return None

# 根据tsp关键字模糊批量查询所有tsp服务列表信息（服务名称、ip,路由地址、请求方法、接口备注）
def tsp_list_search(search_key):
    url = "http://public-api.pla.tuniu-sit.org/tsg/register/service/query"
    headers = {"Referer": "http://tsp.sit.tuniu.org/PLA/TSG/index.html",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    params = {"uid":"28287","token":"","nickname":"董芳芳","r":0.16956803043931346,"name":search_key,"start":0,"limit":10,"sortname":"","sortorder":""}
    params = base64.b64encode(json.dumps(params).encode('utf-8'))
    response = requests.session().get(url, params=params, headers=headers)
    response_text = response.text+'=='
    response_decode =json.loads(str(base64.b64decode(response_text), 'utf-8'))
    if response_decode['data']['rows'] not in (None,'',[]):
        response_tsps = response_decode['data']['rows']
        tsps_tmp_list = []

        for tsp_item in response_tsps:
            tsp_ip = TspSearch(tsp_item["name"])
            ip = tsp_ip.ip_search()["ip"]
            tsps_tmp = {"interface_name": tsp_item["name"], "ip": ip, "path": tsp_item["mapping"], "method": tsp_item["method"], "interface_comment": tsp_item["description"]}
            tsps_tmp_list.append(tsps_tmp)
        return tsps_tmp_list
    else:
        return None

def base64Decode(origin_str):
    if origin_str is not None or origin_str !='':
        try:
            decode_str = str(base64.b64decode(origin_str),'utf-8')
        except:
            decode_str = origin_str
            print("非二进制数据，无需解码")
        finally:
            return decode_str
    else:
        return ''

def base64Encode(origin_str):
    if origin_str is not None or origin_str != '':
        encode_str = str(base64.urlsafe_b64encode(origin_str.encode('utf-8')))[2:-1]
        return encode_str
    else:
        return ''

if __name__ == '__main__':
    from pprint import  pprint
    # ip_url = "http://public-api.pla.tuniu-sit.org/tsg/register/service/get"
    # path_url = "http://public-api.pla.tuniu-sit.org/tsg/register/service/get"

    # tsp2 = TspSearch('BOH.NM.ProductDomainController.getPrdBasicInfo')
    # result = tsp2.tsp2interface()

    tsp3 = TspSearch("MOB.PORTAL.ThemeController.index","pre")
    result = tsp3.tsp2interface()
    print(result, '\n', type(result))
    #
    # pprint(tsp_list_search("CRM.PRO.SpecialSalerController"))
    # origin_str = "eyJzdWNjZXNzIjp0cnVlLCJtc2ciOm51bGwsImVycm9yQ29kZSI6MTAxMDAwMCwiZGF0YSI6eyJwcm9kdWN0SWQiOjIxMDAwODI2NCwicHJvZHVjdE5hbWUiOiJb5pil6IqCXSZsdDvoh6rpqb7lpJbmuKDpgZPljrvlk6rlhL/liIbljZXkuqflk4EmZ3Q76K+35Yu/5YqoIiwicHJvZHVjdE5hbWVFbiI6IiIsImNsYXNzQnJhbmRJZCI6MTksImNsYXNzQnJhbmROYW1lIjoi5bi46KeE6Ieq6am+IiwiY2xhc3NCcmFuZFBhcmVudElkIjo4LCJjbGFzc0JyYW5kUGFyZW50TmFtZSI6IuiHqumpvua4uCIsImJyYW5kSWQiOjYsImJyYW5kTmFtZSI6IuW4uOinhOiHqumpviIsInByb2R1Y3ROZXdMaW5lRGVzdElkIjoxNTgxLCJwcm9kdWN0TmV3TGluZURlc3ROYW1lIjoi5LiK5rW3RCIsInByb2R1Y3ROZXdMaW5lVHlwZUlkIjoxMiwicHJvZHVjdExpbmVUeXBlTmFtZSI6IuWRqOi+uSIsImRlc3RHcm91cElkIjo3OCwiZGVzdEdyb3VwTmFtZSI6IuWNjuS4nCIsInF1YWxpdHlMZXZlbCI6MCwib3duZXJJZCI6MTMyNDcsIm93bmVyTmFtZSI6IuW8oOmbrzMiLCJtYW5hZ2VySWQiOjEzMjQ3LCJtYW5hZ2VyTmFtZSI6IuW8oOmbrzMiLCJkZXBhcnR1cmVDaXR5Q29kZSI6MCwiZGVwYXJ0dXJlQ2l0eU5hbWUiOiLlhajlm70iLCJkZXBhcnRtZW50SWQiOjEsImlzRGlzdHJpYnV0aW9uIjowLCJpc1N1cHBvcnRDaGFuZ2UiOjEsInByb01vZGUiOjQsIm5vTGVhZGVyIjotMSwiZmluYW5jZUxhYmxlIjoiIiwiaXNTdXBwb3J0TXVsdGlwbGVKb3VybmV5IjowLCJpc0FsbG93U3RvcmVUaWNrZXQiOjAsImlzQ2hpbGQiOjAsInNlcnZpY2VUeXBlIjpudWxsLCJwcm9kdWN0VHlwZSI6MywiZGVhZExpbmVEYXkiOm51bGwsImRlYWRMaW5lVGltZSI6bnVsbCwicHJvVHlwZSI6MCwicHJvbW90aW9uVmVuZG9ySWQiOjAsInByb21vdGlvblZlbmRvck5hbWUiOiIiLCJpc09ubGluZSI6MCwid2FybU5vdGljZSI6bnVsbCwiY2hhcmFjdGVyaXN0aWNXb3JkIjoiIiwic3RhdHVzIjowLCJmaXJzdERlc3RHcm91cElkIjoxOSwiZmlyc3REZXN0R3JvdXBOYW1lIjoi5Zu95YaFIiwiYWRUeXBlIjoxLCJ0YWdUeXBlIjowLCJsaXR0bGVQYWNrYWdlVG91ciI6MCwicHJvZHVjdEJ1c2luZXNzVHlwZSI6IjEwMDAiLCJpc1NsYyI6MCwiZnJlZVdpZmkiOjAsIm5vbkNvc3RDYW5jZWwiOjAsInByb2R1Y3RDaGFubmVsIjpbIjIwMDAwIiwiNTAwMDAiLCI0MDAwMCIsIjMwMDAwIiwiNzAwMDUiLCI3MDAwNCJdLCJjaGFubmVsUmVsYXRpb25JZCI6WyIwMTAxMDAwMDAwMjAiLCIwMTAxMDAwMDAwMzAiLCIwMTAxMDAwMDAwMzIiLCIwMTAxMDAwMDAwNDAiLCIwMTAxMDAwMDMwMDAiLCIwMjAxMTAwMDAwMDAiXSwic2FsZU1vZGUiOjcsInNhbGVNb2RlTmFtZSI6IuWOu+WTquWEvyIsInN0YXJEZXNjcmlwdGlvbiI6Iua7oeaEjyIsImlzU2FtcGxlIjowLCJkaXJlY3Rpb25JZCI6MzE4ODEsImlzQ2hpbmEiOjEsImlzTkJDb25maWdUcmFmZmljIjowLCJqb3VybmV5TmlnaHQiOjMsImR1cmF0aW9uIjo0LCJpc0dpdmVJbnMiOjEsInByZEV4Y2x1c2l2ZSI6MCwiaW5xdWlyeVJ1bGVLZXkiOiJjYWwyMDAiLCJvcE1lbW8iOiIiLCJpc0F1dG9TZW5kIjoxLCJzZXJ2aWNlVGFnTGlzdCI6bnVsbCwiYXV0b1BhY2thZ2UiOjAsImlzU3VwcG9ydEpvdXJuZXlDaGFuZ2UiOjAsInBpZCI6MTAwMDIsInByb2R1Y3RDYXRJbmZvIjpbeyJpZCI6MTI5MTE1NzAsInByb2R1Y3RJZCI6MjEwMDA4MjY0LCJjaXR5Q29kZSI6MjUwMCwiY2l0eU5hbWUiOiLkuIrmtbciLCJjYXRJZCI6MjgzMTQ0LCJjYXROYW1lIjoi5LiK5rW3RCIsIm5ld0NhdElkIjoyODMxNDQsIm5ld0NhdE5hbWUiOiLkuIrmtbdEIiwicHJvZHVjdFZpcnR1YWxJZCI6IjIxMDAwODI2NDI1MDAifV19LCJwcm9kdWN0SWQiOjAsImNsYXNzQnJhbmRJZCI6MCwiY2xhc3NCcmFuZFBhcmVudElkIjowfQ=="
    # print(base64Decode(origin_str))

    # str1 = '{"page":1,"pageSize":10}'
    # print(type(str1))
    # base64Encode(str1)

