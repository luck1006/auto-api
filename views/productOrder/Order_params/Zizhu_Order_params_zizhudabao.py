# -*- coding:UTF-8 -*-
# @Author  : huangfang

from views.productOrder.BOH_params.Zizhu_BOH_dabao import Zizhu_BOH_dabao
from app.actions.tools.commonData import productdata_zizhu
import datetime

class Zizhu_Order_params_zizhudabao(Zizhu_BOH_dabao):
    #获取行程1ID
    def zizhu_get_journeyId1(self):
        journeyId1 = Zizhu_BOH_dabao().getDetailResources()['journeyId1']
        return journeyId1

    # 获取行程2ID
    def zizhu_get_journeyId2(self):
        journeyId2 = Zizhu_BOH_dabao().getDetailResources()['journeyId2']
        return journeyId2


    #获取行程资源ID1
    def zizhu_get_resId1(self):
        resId1 = Zizhu_BOH_dabao().getDetailResources()['resId1']
        #resourceId1 = '2249640554'
        return resId1

    # 获取行程资源ID2
    def zizhu_get_resId2(self):
        resId2 = Zizhu_BOH_dabao().getDetailResources()['resId2']
        # resourceId1 = '2249640554'
        return resId2

    # 获取行程资源type
    def zizhu_get_resType(self):
        resType = Zizhu_BOH_dabao().getDetailResources()['resType']
        return resType

    # 获取行程子资源type
    def zizhu_get_resSubType(self):
        resSubType = Zizhu_BOH_dabao().getDetailResources()['resSubType']
        return resSubType

    #设置出发时间为当前时间+10天
    def zizhu_get_startDate(self):
        startDate = (datetime.datetime.now()+datetime.timedelta(days=10)).strftime("%Y-%m-%d")
        return startDate

    #行程结束时间
    def zizhu_get_endDate(self):
        endDate = (datetime.datetime.now()+datetime.timedelta(days=12)).strftime("%Y-%m-%d")
        return endDate

    #获取产品id
    def zizhu_get_productId(self):
        productId = productdata_zizhu["productId_zizhu_dabao"]
        return productId

    #获取产品出发城市
    def zizhu_get_startCityCode(self):
        #startCityCode = Gentuan_BOH().getDetailResources()['startCityCode']
        startCityCode = '1602'
        return startCityCode

    def Zizhu_Params_channelData(self):
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
    #备用的memberid：6676180,71656257,71656195
    def Zizhu_Params_order(self):
        order='''"order": {
                "memberId": 71656257,
                "source": 3,
                "sourceType": 0,
                "systemInfo": {
                  "transferMode": 0,
                  "requestId": "OLBB_PC_0150d01b-4ac1-441b-b710-c7dd65c6a972"
                },
                "interFlightResFlag": 1,
                "extension": {
                  "transferNetReason": ""
                }
                }'''

        return order

    def Zizhu_Params_subOrders(self):
        subOrders=''' "subOrders": [
    {
      "orderId": 0,
      "orderType": 53,
      "totalPrice": 7000,
      "totalResPrice": 7000,
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
          "journeyId": '''+self.zizhu_get_journeyId1()+''',
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
          "destinations": "\u5e38\u5dde",
          "journeyId": '''+self.zizhu_get_journeyId2()+''',
          "resourceTour": [
            
          ],
          "resourceFlightTicket": [
            
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
            {
              "resourceId": '''+self.zizhu_get_resId1()+''',
              "resourceName": "zy\u9152\u5e97+\u95e8\u7968\u6253\u5305\u6d4b\u8bd5",
              "journey": 599155,
              "resourceType": 5,
              "startDate": "'''+self.zizhu_get_startDate()+'''",
              "endDate": "'''+self.zizhu_get_endDate()+'''",
              "adultCount": 2,
              "childCount": 0,
              "resourcePackageList": [
                {
                  "resourceId": "2249429657",
                  "resourceType": 4,
                  "resourceName": "\u5927\u962a\u73af\u7403\u5f71\u57ce(\u5927\u95e8\u7968)+JRPASS\u5173\u897f\u94c1\u8def\u5468\u6e38\u5238(\u666e\u901a\u5e2d4\u65e5\u5238)\u513f\u7ae5\u7968(\u67dc\u53f0\u53d6\u7968)",
                  "startDate": "'''+self.zizhu_get_startDate()+'''",
                  "endDate": "'''+self.zizhu_get_endDate()+'''"
                },
                {
                  "resourceId": "2250054360",
                  "resourceType": 2,
                  "resourceName": "\u5317\u4eac\u4e16\u7eaa\u534e\u5929\u5927\u9152\u5e97&#160;&#160;&#160;[\u65e0\u65e9](\u53cc\u5e8a)",
                  "startDate": "'''+self.zizhu_get_startDate()+'''",
                  "endDate": "'''+self.zizhu_get_endDate()+'''"
                }
              ],
              "adultPrice": 3500,
              "childPrice": 3000
            }
          ],
          "resourceCon": [
            
          ],
          "resourceLocal": [
            
          ]
        }
      ],
      "product": {
        "desCity": "\u5e38\u5dde",
        "desCityCode": 1604,
        "duration": 6,
        "endDate": "'''+self.zizhu_get_endDate()+'''",
        "night": 0,
        "price": 3500,
        "tuniuPrice": 3500,
        "tuniuChildPrice": 3000,
        "productId": '''+self.zizhu_get_productId()+''',
        "productLineDestId": 0,
        "productLineId": 500802,
        "productLineTypeId": 0,
        "productNewLineTypeId": 11,
        "productName": "&lt;\u81ea\u52a9\u6e38\u81ea\u52a8\u5316\u4ea7\u54c1\u6253\u5305\u52ff\u52a8&gt;",
        "productType": 2,
        "startCity": "\u5357\u4eac",
        "startCityCode": 1602,
        "startDate": "'''+self.zizhu_get_startDate()+'''",
        "productClassId": 2,
        "productChildClassId": 16,
        "productLineDesName": 2300,
        "productLineDesGroup": 78,
        "productLineDesType": 11
      },
      "requirement": {
        "planId": null,
        "backCityCode": null,
        "backCityName": null,
        "bookCity": "\u5357\u4eac",
        "bookCityCode": 1602,
        "departureDate": "'''+self.zizhu_get_startDate()+'''",
        "endDate": "'''+self.zizhu_get_endDate()+'''",
        "desCity": "\u5e38\u5dde",
        "desCityCode": 1604,
        "groupCost": 7000,
        "hasOld": 0,
        "isL": 0,
        "roomCharge": 4,
        "roomChargeRemark": "",
        "startCity": "\u5357\u4eac",
        "startCityCode": 1602,
        "adultCount": 2,
        "childCount": 0
      },
      "touristList": [
        {
          "name": "\u9648\u672f",
          "tel": "15295115732",
          "firstname": null,
          "lastname": null,
          "country": "\u4e2d\u56fd",
          "psptType": 0,
          "psptId": null,
          "psptEndDate": "",
          "sex": 9,
          "personId": 1949205,
          "telCountryId": 40,
          "intlCode": "0086",
          "intlTel": "008615295115732",
          "relatedResList": [
            
          ],
          "isAdult": 1,
          "touristType": 0
        },
        {
          "name": "\u6731\u7d20\u59b9",
          "tel": "18876594036",
          "firstname": null,
          "lastname": null,
          "country": "\u4e2d\u56fd",
          "psptType": 0,
          "psptId": null,
          "psptEndDate": "",
          "sex": 9,
          "personId": 1940147,
          "telCountryId": 40,
          "intlCode": "0086",
          "intlTel": "008618876594036",
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


    def Zizhu_Order_params_zizhudabao(self):
        Zizhu_Order_params_zizhudabao = "{" + str(self.Zizhu_Params_channelData()) + "," + str(self.Zizhu_Params_order()) + "," + str(self.Zizhu_Params_subOrders()) + "}"

        return Zizhu_Order_params_zizhudabao


if __name__ == '__main__':

    genp = Zizhu_Order_params_zizhudabao()
    params=genp.Zizhu_Order_params_zizhudabao()
    print (params)



