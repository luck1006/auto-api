# -*- coding:UTF-8 -*-
# @Author  : huangfang

# from _02Businesskeyword._01Package.abstract.prdTourJourneyResAbtract import prdTourJourneyResAbtract
from app.actions.tools import BaseApplication
from app.actions.tools.InterfaceKeyword import InterfaceKeyword
import json

# @BaseApplication.container
class GenTuan_Order(BaseApplication.BaseApplication):

    def __init__(self):
        self.orderType='11'

    def GenTuan_Params_channelData(self):
        channelData='''"channelData": {
"callPhone": "",
"clientType": 20000,
"clientTypeExpand": 0,
"fromUrl": "",
"pSource": 3,
"pValue": "100",
"channelRelationId": "010100000020"
}'''

        return channelData

    def GenTuan_Params_order(self):
        order='''"order": {
"memberId": 6676180,
"source": 3,
"sourceType": 0,
"systemInfo": {
  "transferMode": 1,
  "requestId": "OLBB_PC_0150d01b-4ac1-441b-b710-c7dd65c6a912"
},
"interFlightResFlag": 1,
"extension": {
  "transferNetReason": ""
}
}'''

        return order


    def GenTuan_Params_subOrders(self):
        subOrders='''  "subOrders": [
    {
      "orderId": 0,
      "orderType": 11,
      "totalPrice": 316280,
      "totalResPrice": 316280,
      "contactList": [
        {
          "appellation": 1,
          "email": "",
          "isDefault": 1,
          "name": "\u4f55\u806a",
          "phone": null,
          "tel": "18876594036",
          "type": 2,
          "telCountryId": 40,
          "intlCode": "0086",
          "intlTel": "008618876594036"
        }
      ],
      "promotionList": [
        
      ],
      "journey": [
        {
          "journeySeqNum": 0,
          "isChange": 0,
          "destinations": "",
          "journeyId": 598051,
          "resourceTour": [
            
          ],
          "resourceScatterFlightTicket": [
            
          ],
          "resourceFlightTicket": [
            
          ],
          "resourceGenShuttle": [
            
          ],
          "resourceAddition": [
            
          ],
          "resourceInsurance": [
            
          ],
          "resourceTrainTicket": [
            
          ],
          "resourceHotelRoom": [
            
          ],
          "resourceBusTicket": [
            
          ],
          "resourceMenpiao": [
            
          ],
          "resourceVisa": [
            
          ],
          "resourcePackage": [
            
          ],
          "resourceCon": [
            
          ],
          "resourceLocal": [
            
          ]
        },
        {
          "journeySeqNum": 1,
          "isChange": 0,
          "destinations": "\u82cf\u5dde",
          "journeyId": 598052,
          "resourceTour": [
            {
              "resourceId": 2249640554,
              "resourceName": "[\u6625\u8282]<gwl\u8ddf\u56e2\u6253\u5305\u6e38>\u5c0f\u9ed1\u5361",
              "resourceType": 27,
              "adultCount": 3,
              "childCount": 0,
              "memo": "",
              "subResourceType": 27,
              "endDate": "2019-04-02",
              "startDate": "2019-03-31"
            }
          ],
          "resourceAddition": [
            
          ],
          "resourceInsurance": [
            
          ],
          "resourceHotelRoom": [
            
          ],
          "resourceBusTicket": [
            
          ],
          "resourceMenpiao": [
            
          ],
          "resourceVisa": [
            
          ],
          "resourcePackage": [
            
          ],
          "resourceCon": [
            
          ],
          "resourceLocal": [
            
          ]
        }
      ],
      "product": {
        "desCity": "\u82cf\u5dde",
        "desCityCode": 1615,
        "duration": 3,
        "endDate": "2019-04-02",
        "night": 2,
        "price": 105760,
        "tuniuPrice": 105760,
        "tuniuChildPrice": 74182,
        "productId": 210017573,
        "productLineDestId": 0,
        "productLineId": 40262,
        "productLineTypeId": 0,
        "productNewLineTypeId": 12,
        "productName": "&lt;\u81ea\u52a8\u5316\u751f\u6210\u8ddf\u56e2\u4ea7\u54c1&gt;",
        "productType": 1,
        "startCity": "\u5357\u4eac",
        "startCityCode": 1602,
        "startDate": "2019-03-31",
        "productClassId": 1,
        "productChildClassId": 0,
        "productLineDesName": 97,
        "productLineDesGroup": 17,
        "productLineDesType": 12,
        "isGiveIns": 1
      },
      "requirement": {
        "planId": null,
        "backCityCode": null,
        "backCityName": null,
        "bookCity": "\u5317\u4eac",
        "bookCityCode": 200,
        "departureDate": "2019-03-31",
        "endDate": "2019-04-02",
        "desCity": "\u82cf\u5dde",
        "desCityCode": 1615,
        "groupCost": 316280,
        "hasOld": 0,
        "isL": 0,
        "roomCharge": 1,
        "roomChargeRemark": "",
        "startCity": "\u5357\u4eac",
        "startCityCode": 1602,
        "adultCount": 3,
        "childCount": 0
      },
      "touristList": [
        {
          "name": "\u9648\u672f",
          "tel": "15295115732",
          "firstname": null,
          "lastname": null,
          "country": "\u4e2d\u56fd",
          "psptType": 1,
          "psptId": "32118119911225353x",
          "psptEndDate": "",
          "sex": 1,
          "personId": 1949205,
          "birthday": "1991-12-25",
          "telCountryId": 40,
          "intlCode": "0086",
          "intlTel": "008615295115732",
          "relatedResList": [
            
          ],
          "isAdult": 1,
          "touristType": 0
        },
        {
          "name": "ZHOUHUI",
          "tel": null,
          "firstname": null,
          "lastname": null,
          "country": "\u4e2d\u56fd",
          "psptType": 2,
          "psptId": "G12344678",
          "psptEndDate": "2020-01-01",
          "sex": 1,
          "personId": 1948279,
          "birthday": "1975-06-19",
          "relatedResList": [
            
          ],
          "isAdult": 1,
          "touristType": 0
        },
        {
          "name": "TESTTST",
          "tel": "15000123456",
          "firstname": null,
          "lastname": null,
          "country": "\u4e2d\u56fd",
          "psptType": 4,
          "psptId": "6525466532",
          "psptEndDate": "2116-01-01",
          "sex": 1,
          "personId": 1945223,
          "birthday": "1985-01-01",
          "telCountryId": 31,
          "intlCode": "0061",
          "intlTel": "006115000123456",
          "relatedResList": [
            
          ],
          "isAdult": 1,
          "touristType": 0
        }
      ],
      "couponList": [
        {
          "couponType": 1,
          "useValue": 0
        }
      ],
      "invoiceList": [
        
      ]
    }
  ]'''

        return subOrders


    def GenTuan_Create_Order(self,url,params):
        #创建订单
        #url = 'http://public-api.bj.pga.tuniu-sit.org/pga-web/nws/order/add'
        #params='''{"channelData":{"callPhone":"","clientType":20000,"clientTypeExpand":0,"fromUrl":"","pSource":3,"pValue":"100","channelRelationId":"010100000020"},"order":{"memberId":6676180,"source":3,"sourceType":0,"systemInfo":{"transferMode":0,"requestId":"OLBB_PC_0150d01b-4ac1-441b-b710-c7dd65c6a912"},"interFlightResFlag":1,"extension":{"transferNetReason":""}},"subOrders":[{"orderId":0,"orderType":11,"totalPrice":10290,"contactList":[{"appellation":1,"email":"","isDefault":1,"name":"\u4f55\u806a","phone":null,"tel":"18876594036","type":2,"telCountryId":40,"intlCode":"0086","intlTel":"008618876594036"}],"promotionList":[],"journey":[{"journeySeqNum":0,"isChange":0,"destinations":"","journeyId":387407,"resourceTour":[],"resourceScatterFlightTicket":[],"resourceFlightTicket":[{"resourceId":2249302900,"resourceName":"","resourceType":7,"adultCount":2,"childCount":0,"startDate":"2019-01-15","ibeRule":[],"externalInfo":null,"solutionId":0,"adultPrice":1064,"childPrice":958}],"resourceGenShuttle":[],"resourceAddition":[],"resourceInsurance":[{"resourceId":1432902088,"resourceName":"\u76f4\u8fde\u592a\u4fdd\u65c5\u7a0b\u9884\u5b9a\u53d6\u6d88\u9669\u6d4b\u8bd520000","resourceType":29,"adultCount":1,"childCount":0,"endDate":"2019-01-16","startDate":"2019-01-15","memo":"","isGive":0,"subResourceId":0,"subResourceType":0},{"resourceId":1517339468,"resourceName":"SIT_\u73af\u5883\u9ed8\u8ba4\u4fdd\u9669\u65c5\u884c\u610f\u5916\u9669\u65b9\u6848\u4e00","resourceType":29,"adultCount":1,"childCount":0,"endDate":"2019-01-16","startDate":"2019-01-15","memo":"","isGive":0,"subResourceId":0,"subResourceType":0}],"resourceTrainTicket":[],"resourceHotelRoom":[],"resourceBusTicket":[],"resourceMenpiao":[],"resourceVisa":[],"resourcePackage":[],"resourceCon":[],"resourceLocal":[]},{"journeySeqNum":1,"isChange":0,"destinations":"\u85e9\u5207","journeyId":571432,"resourceTour":[{"resourceId":2147505206,"resourceName":"<SIT\u8ddf\u56e2\u8d44\u6e90-\u53f2\u7ef4\u5f3a\u6e38>\u5367\u69fd \u522b\u626f\u6de1 (\u590d\u5236)","resourceType":27,"adultCount":2,"childCount":0,"memo":"","subResourceType":1,"endDate":"2019-01-16","startDate":"2019-01-15"}],"resourceAddition":[],"resourceInsurance":[],"resourceHotelRoom":[],"resourceBusTicket":[],"resourceMenpiao":[],"resourceVisa":[],"resourcePackage":[],"resourceCon":[],"resourceLocal":[]}],"product":{"desCity":"\u85e9\u5207","desCityCode":784231,"duration":2,"endDate":"2019-01-16","night":1,"price":4760,"tuniuPrice":4760,"tuniuChildPrice":4020,"productId":210007496,"productLineDestId":0,"productLineId":2067,"productLineTypeId":0,"productNewLineTypeId":11,"productName":"&lt;SIT\u56de\u5f52\u6d4b\u8bd5\u4e13\u7528&gt;\u6d4b\u8bd5\u6d4b\u8bd5\u6d4b\u8bd5\u6d4b\u8bd5","productType":1,"startCity":"\u4e0a\u6d77","startCityCode":2500,"startDate":"2019-01-15","productClassId":1,"productChildClassId":0,"productLineDesName":10,"productLineDesGroup":156,"productLineDesType":11},"requirement":{"planId":84179,"backCityCode":2500,"backCityName":"\u4e0a\u6d77","bookCity":"\u5317\u4eac","bookCityCode":200,"departureDate":"2019-01-15","endDate":"2019-01-16","desCity":"\u85e9\u5207","desCityCode":784231,"groupCost":10290,"hasOld":0,"isL":0,"roomCharge":4,"roomChargeRemark":"","startCity":"\u4e0a\u6d77","startCityCode":2500,"adultCount":2,"childCount":0},"touristList":[{"name":"ZHANGXIAO","tel":"13585607576","firstname":null,"lastname":null,"country":"\u4e2d\u56fd","psptType":2,"psptId":"G4561230","psptEndDate":"2019-11-01","sex":"","personId":1950284,"birthday":"1985-01-01","telCountryId":40,"intlCode":"0086","intlTel":"008613585607576","relatedResList":[],"isAdult":1,"touristType":0,"insuranceResIds":[1432902088,1517339468],"flightResIds":[2249302900]},{"name":"\u9648\u672f","tel":"15295115732","firstname":null,"lastname":null,"country":"\u4e2d\u56fd","psptType":1,"psptId":"32118119911225353x","psptEndDate":"","sex":1,"personId":1949205,"birthday":"1991-12-25","telCountryId":40,"intlCode":"0086","intlTel":"008615295115732","relatedResList":[],"isAdult":1,"touristType":0,"insuranceResIds":[1432902088,1517339468],"flightResIds":[2249302900]}],"couponList":[{"couponType":1,"useValue":0}],"invoiceList":[]}]}'''

        headers = {"Content-Type": "application/json"}

        params=json.loads(params)

        p=InterfaceKeyword.InterfaceKeyword().Put(url,params,headers)

        return p


    def GenTuan_CheckResponse(self,rsp):
        #print type(rsp),rsp
        #print rsp['text'],rsp['code']
        if rsp is not None:
            self.loggers.debug(rsp['text'])
            if rsp['code']==200:
                text_base64Decode = InterfaceKeyword.InterfaceKeyword().base64Decode(rsp['text'])
                print ("text_base64Decode==",text_base64Decode)
                text = json.loads(text_base64Decode)
                if text.has_key("success") == False:
                    self.loggers.error("返回消息格式有误");
                    return False
                if text["success"] == False:
                    self.loggers.error("返回失败，code为" + str(text["errorCode"]))
                    return False
                else:
                    return text
            else:
                self.loggers.error("返回状态"+rsp.status_code)
                return False

        else:
            self.loggers.error("返回结果为空")


    def GenTuan_GET_orderId(self,params):
        if params:
            orderId = params['data'][0]['orderId']
            return orderId
        else:
            self.loggers.error("返回结果为空")
            return False



if __name__ == '__main__':
    gentuan = GenTuan_Order()

    url='http://public-api.bj.pga.tuniu-sit.org/pga-web/nws/order/add'

    #params = '''{"channelData":{"callPhone":"","clientType":20000,"clientTypeExpand":0,"fromUrl":"","pSource":3,"pValue":"100","channelRelationId":"010100000020"},"order":{"memberId":6676180,"source":3,"sourceType":0,"systemInfo":{"transferMode":1,"requestId":"OLBB_PC_0150d01b-4ac1-441b-b710-c7dd65c6a912"},"interFlightResFlag":1,"extension":{"transferNetReason":""}},"subOrders":[{"orderId":0,"orderType":11,"totalPrice":10290,"contactList":[{"appellation":1,"email":"","isDefault":1,"name":"\u4f55\u806a","phone":null,"tel":"18876594036","type":2,"telCountryId":40,"intlCode":"0086","intlTel":"008618876594036"}],"promotionList":[],"journey":[{"journeySeqNum":0,"isChange":0,"destinations":"","journeyId":387407,"resourceTour":[],"resourceScatterFlightTicket":[],"resourceFlightTicket":[{"resourceId":2249302900,"resourceName":"","resourceType":7,"adultCount":2,"childCount":0,"startDate":"2019-01-15","ibeRule":[],"externalInfo":null,"solutionId":0,"adultPrice":1064,"childPrice":958}],"resourceGenShuttle":[],"resourceAddition":[],"resourceInsurance":[{"resourceId":1432902088,"resourceName":"\u76f4\u8fde\u592a\u4fdd\u65c5\u7a0b\u9884\u5b9a\u53d6\u6d88\u9669\u6d4b\u8bd520000","resourceType":29,"adultCount":1,"childCount":0,"endDate":"2019-01-16","startDate":"2019-01-15","memo":"","isGive":0,"subResourceId":0,"subResourceType":0},{"resourceId":1517339468,"resourceName":"SIT_\u73af\u5883\u9ed8\u8ba4\u4fdd\u9669\u65c5\u884c\u610f\u5916\u9669\u65b9\u6848\u4e00","resourceType":29,"adultCount":1,"childCount":0,"endDate":"2019-01-16","startDate":"2019-01-15","memo":"","isGive":0,"subResourceId":0,"subResourceType":0}],"resourceTrainTicket":[],"resourceHotelRoom":[],"resourceBusTicket":[],"resourceMenpiao":[],"resourceVisa":[],"resourcePackage":[],"resourceCon":[],"resourceLocal":[]},{"journeySeqNum":1,"isChange":0,"destinations":"\u85e9\u5207","journeyId":571432,"resourceTour":[{"resourceId":2147505206,"resourceName":"<SIT\u8ddf\u56e2\u8d44\u6e90-\u53f2\u7ef4\u5f3a\u6e38>\u5367\u69fd \u522b\u626f\u6de1 (\u590d\u5236)","resourceType":27,"adultCount":2,"childCount":0,"memo":"","subResourceType":1,"endDate":"2019-01-16","startDate":"2019-01-15"}],"resourceAddition":[],"resourceInsurance":[],"resourceHotelRoom":[],"resourceBusTicket":[],"resourceMenpiao":[],"resourceVisa":[],"resourcePackage":[],"resourceCon":[],"resourceLocal":[]}],"product":{"desCity":"\u85e9\u5207","desCityCode":784231,"duration":2,"endDate":"2019-01-16","night":1,"price":4760,"tuniuPrice":4760,"tuniuChildPrice":4020,"productId":210007496,"productLineDestId":0,"productLineId":2067,"productLineTypeId":0,"productNewLineTypeId":11,"productName":"&lt;SIT\u56de\u5f52\u6d4b\u8bd5\u4e13\u7528&gt;\u6d4b\u8bd5\u6d4b\u8bd5\u6d4b\u8bd5\u6d4b\u8bd5","productType":1,"startCity":"\u4e0a\u6d77","startCityCode":2500,"startDate":"2019-01-15","productClassId":1,"productChildClassId":0,"productLineDesName":10,"productLineDesGroup":156,"productLineDesType":11},"requirement":{"planId":84179,"backCityCode":2500,"backCityName":"\u4e0a\u6d77","bookCity":"\u5317\u4eac","bookCityCode":200,"departureDate":"2019-01-15","endDate":"2019-01-16","desCity":"\u85e9\u5207","desCityCode":784231,"groupCost":10290,"hasOld":0,"isL":0,"roomCharge":4,"roomChargeRemark":"","startCity":"\u4e0a\u6d77","startCityCode":2500,"adultCount":2,"childCount":0},"touristList":[{"name":"ZHANGXIAO","tel":"13585607576","firstname":null,"lastname":null,"country":"\u4e2d\u56fd","psptType":2,"psptId":"G4561230","psptEndDate":"2019-11-01","sex":"","personId":1950284,"birthday":"1985-01-01","telCountryId":40,"intlCode":"0086","intlTel":"008613585607576","relatedResList":[],"isAdult":1,"touristType":0,"insuranceResIds":[1432902088,1517339468],"flightResIds":[2249302900]},{"name":"\u9648\u672f","tel":"15295115732","firstname":null,"lastname":null,"country":"\u4e2d\u56fd","psptType":1,"psptId":"32118119911225353x","psptEndDate":"","sex":1,"personId":1949205,"birthday":"1991-12-25","telCountryId":40,"intlCode":"0086","intlTel":"008615295115732","relatedResList":[],"isAdult":1,"touristType":0,"insuranceResIds":[1432902088,1517339468],"flightResIds":[2249302900]}],"couponList":[{"couponType":1,"useValue":0}],"invoiceList":[]}]}'''

    params = "{" + str(gentuan.GenTuan_Params_channelData()) + ","  + str(gentuan.GenTuan_Params_order()) + "," + str(gentuan.GenTuan_Params_subOrders()) + "}"
    print (params)

    resp_dict = gentuan.GenTuan_Create_Order(url,params)
    print (resp_dict)

    GenTuan_CheckResponse_DATA = gentuan.GenTuan_CheckResponse(resp_dict)
    print (GenTuan_CheckResponse_DATA)

    orderId =  gentuan.GenTuan_GET_orderId(GenTuan_CheckResponse_DATA)
    print (orderId)




