# -*- coding:UTF-8 -*-
# @Author  : huangfang

from views.productOrder.BOH_params.Zijia_BOH import Zijia_BOH
from app.actions.tools.commonData import productdata_zijia
import datetime

class Zijia_Order_params(Zijia_BOH):
    #获取行程1ID
    def zijia_get_journeyId1(self):
        journeyId1 = Zijia_BOH().getDetailResources()['journeyId1']
        return journeyId1

    # 获取行程2ID
    def zijia_get_journeyId2(self):
        journeyId2 = Zijia_BOH().getDetailResources()['journeyId2']
        return journeyId2


    #获取行程资源ID
    def zijia_get_resId1(self):
        resId1 = Zijia_BOH().getDetailResources()['resId1']
        return resId1

    # 获取行程资源ID
    def zijia_get_resId2(self):
        resId2 = Zijia_BOH().getDetailResources()['resId2']
        return resId2

    # 获取行程资源type
    def zijia_get_resType(self):
        resType = Zijia_BOH().getDetailResources()['resType']
        return resType

    # 获取行程子资源type
    def zijia_get_resSubType(self):
        resSubType = Zijia_BOH().getDetailResources()['resSubType']
        return resSubType

    #设置出发时间为当前时间+10天
    def zijia_get_startDate(self):
        startDate = (datetime.datetime.now()+datetime.timedelta(days=10)).strftime("%Y-%m-%d")
        return startDate

    #行程结束时间
    def zijia_get_endDate(self):
        endDate = (datetime.datetime.now()+datetime.timedelta(days=12)).strftime("%Y-%m-%d")
        return endDate

    # 获取门票产品id
    def zijia_get_productId(self):
        productId = productdata_zijia["productId_zijia"]
        return productId



    def Zijia_Params_channelData(self):
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
    #备用的memberid：6676180,71656257
    def Zijia_Params_order(self):
        order = '''"order": {
                        "memberId": 71656257,
                        "source": 3,
                        "sourceType": 0,
                        "systemInfo": {
                          "transferMode": 0,
                          "requestId": "OLBB_PC_0390d01b-4ac1-441b-b710-c7dd65c6a972"
                        },
                        "interFlightResFlag": 1,
                        "extension": {
                          "transferNetReason": ""
                        }
                        }'''

        return order

    def Zijia_Params_subOrders(self):
        subOrders='''    "subOrders": [
    {
      "orderId": 0,
      "orderType": 50,
      "totalPrice": 4210,
      "totalResPrice": 4210,
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
          "journeyId": '''+self.zijia_get_journeyId1()+''',
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
          "destinations": "\u5357\u4eac",
          "journeyId": '''+self.zijia_get_journeyId2()+''',
          "resourceTour": [
            {
              "resourceId": '''+self.zijia_get_resId2()+''',
              "resourceName": "[\u5143\u65e6]<qj\u6d4b\u8bd5\u6570\u636e\u52ff\u52a81\u6e38>qj\u6d4b\u8bd5\u6570\u636e\u52ff\u52a81",
              "resourceType": 27,
              "adultCount": 2,
              "childCount": 0,
              "memo": "",
              "subResourceType": 1,
              "endDate": "'''+self.zijia_get_startDate()+'''",
              "startDate": "'''+self.zijia_get_endDate()+'''"
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
        "desCity": "\u5357\u4eac",
        "desCityCode": 1602,
        "duration": 3,
        "endDate": "'''+self.zijia_get_endDate()+'''",
        "night": 2,
        "price": 2105,
        "tuniuPrice": 2105,
        "tuniuChildPrice": 1053,
        "productId": '''+self.zijia_get_productId()+''',
        "productLineDestId": 0,
        "productLineId": 1014097,
        "productLineTypeId": 0,
        "productNewLineTypeId": 80,
        "productName": "&lt;\u81ea\u9a7e\u81ea\u52a8\u5316\u7ebf\u8def\u8ddf\u961f\u81ea\u9a7e&gt;",
        "productType": 8,
        "startCity": "\u5357\u4eac",
        "startCityCode": 1602,
        "startDate": "'''+self.zijia_get_startDate()+'''",
        "productClassId": 8,
        "productChildClassId": 20,
        "productLineDesName": 5,
        "productLineDesGroup": 78,
        "productLineDesType": 80
      },
      "requirement": {
        "planId": null,
        "backCityCode": null,
        "backCityName": null,
        "bookCity": "\u4e0a\u6d77",
        "bookCityCode": 2500,
        "departureDate": "'''+self.zijia_get_startDate()+'''",
        "endDate": "'''+self.zijia_get_endDate()+'''",
        "desCity": "\u5357\u4eac",
        "desCityCode": 1602,
        "groupCost": 4210,
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
          "name": "\u8d75\u745e\u5f3a",
          "tel": "13062527068",
          "firstname": null,
          "lastname": null,
          "country": "\u4e2d\u56fd",
          "psptType": 0,
          "psptId": null,
          "psptEndDate": "",
          "sex": 9,
          "personId": 1941175,
          "telCountryId": "40",
          "intlCode": "0086",
          "intlTel": "008613062527068",
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


    def Zijia_Order_params(self):
        Zijia_Order_params = "{" + str(self.Zijia_Params_channelData()) + "," + str(self.Zijia_Params_order()) + "," + str(self.Zijia_Params_subOrders())+ "}"

        return Zijia_Order_params


if __name__ == '__main__':

    genp = Zijia_Order_params()
    params=genp.Zijia_Order_params()
    print (params)



