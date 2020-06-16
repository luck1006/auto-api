# -*- coding:UTF-8 -*-
# @Author  : huangfang

from views.productOrder.BOH_params.Zizhu_BOH_train import Zizhu_BOH_train
from app.actions.tools.commonData import productdata_zizhu
import datetime

class Zizhu_Order_params_zizhutrain(Zizhu_BOH_train):
    #获取行程1ID
    def zizhu_get_journeyId1(self):
        journeyId1 = Zizhu_BOH_train().getDetailResources()['journeyId1']
        return journeyId1

    # 获取行程2ID
    def zizhu_get_journeyId2(self):
        journeyId2 = Zizhu_BOH_train().getDetailResources()['journeyId2']
        return journeyId2


    #获取行程资源ID1
    def zizhu_get_resId1(self):
        resId1 = Zizhu_BOH_train().getDetailResources()['resId1']
        #resourceId1 = '2249640554'
        return resId1

    # 获取行程资源ID2
    def zizhu_get_resId2(self):
        resId2 = Zizhu_BOH_train().getDetailResources()['resId2']
        # resourceId1 = '2249640554'
        return resId2

    # 获取行程资源type
    def zizhu_get_resType(self):
        resType = Zizhu_BOH_train().getDetailResources()['resType']
        return resType

    # 获取行程子资源type
    def zizhu_get_resSubType(self):
        resSubType = Zizhu_BOH_train().getDetailResources()['resSubType']
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
        productId = productdata_zizhu["productId_zizhu_train"]
        return productId

    # 获取火车票资源id
     # 去程火车票资源

    def zizhu_get_resourceId1(self):
        resourceId1 = Zizhu_BOH_train().getDetailResources()['resId1_train']
        return resourceId1

    # 返程火车票资源

    def zizhu_get_resourceId2(self):
        resourceId2 = Zizhu_BOH_train().getDetailResources()['resId2_train']
        return resourceId2

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
      "totalPrice": 1786,
      "totalResPrice": 1786,
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
            {
              "resourceId": '''+self.zizhu_get_resourceId1()+''',
              "resourceName": "",
              "resourceType": 8,
              "adultCount": 2,
              "childCount": 0,
              "adultPrice": 46.5,
              "childPrice": 46.5,
              "startDate": "'''+self.zizhu_get_startDate()+'''"
            },
            {
              "resourceId": '''+self.zizhu_get_resourceId2()+''',
              "resourceName": "",
              "resourceType": 8,
              "adultCount": 2,
              "childCount": 0,
              "adultPrice": 46.5,
              "childPrice": 46.5,
              "startDate": "'''+self.zizhu_get_startDate()+'''"
            }
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
              "resourceName": "\u6253\u5305\u8d44\u6e90",
              "journey": 599159,
              "resourceType": 5,
              "startDate": "'''+self.zizhu_get_startDate()+'''",
              "endDate": "'''+self.zizhu_get_endDate()+'''",
              "adultCount": 2,
              "childCount": 0,
              "resourcePackageList": [
                {
                  "resourceId": "2248987392",
                  "resourceType": 7,
                  "resourceName": "\u5357\u4eac\u5230\u4e0a\u6d77 \u5355\u7a0b\u7968",
                  "startDate": "'''+self.zizhu_get_startDate()+'''",
                  "endDate": "'''+self.zizhu_get_endDate()+'''"
                },
                {
                  "resourceId": "2249518009",
                  "resourceType": 4,
                  "resourceName": "gwl\u95e8\u7968\u4e09\u7ea7\u57ce\u5e02",
                  "startDate": "'''+self.zizhu_get_startDate()+'''",
                  "endDate": "'''+self.zizhu_get_endDate()+'''"
                }
              ],
              "adultPrice": 800,
              "childPrice": 500
            }
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
        "duration": 4,
        "endDate": "'''+self.zizhu_get_endDate()+'''",
        "night": 2,
        "price": 893,
        "tuniuPrice": 893,
        "tuniuChildPrice": 593,
        "productId": '''+self.zizhu_get_productId()+''',
        "productLineDestId": 0,
        "productLineId": 10830588,
        "productLineTypeId": 0,
        "productNewLineTypeId": 11,
        "productName": "&lt;\u81ea\u52a9\u6e38\u81ea\u52a8\u5316\u706b\u8f66\u7968+\u8d44\u6e90&gt;",
        "productType": 2,
        "startCity": "\u5357\u4eac",
        "startCityCode": 1602,
        "startDate": "'''+self.zizhu_get_startDate()+'''",
        "productClassId": 2,
        "productChildClassId": 16,
        "productLineDesName": 5364,
        "productLineDesGroup": 78,
        "productLineDesType": 11
      },
      "requirement": {
        "planId": 94394,
        "backCityCode": 1602,
        "backCityName": "\u5357\u4eac",
        "bookCity": "\u5357\u4eac",
        "bookCityCode": 1602,
        "departureDate": "'''+self.zizhu_get_startDate()+'''",
        "endDate": "'''+self.zizhu_get_endDate()+'''",
        "desCity": "\u5357\u4eac",
        "desCityCode": 1602,
        "groupCost": 1786,
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
            {
              "resourceType": 8,
              "resourceId": '''+self.zizhu_get_resourceId1()+''',
              "sellMode": 1
            },
            {
              "resourceType": 8,
              "resourceId": '''+self.zizhu_get_resourceId2()+''',
              "sellMode": 1
            }
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
          "psptType": 1,
          "psptId": "372901194503255929",
          "psptEndDate": "",
          "sex": 0,
          "personId": 1940147,
          "birthday": "1945-03-25",
          "telCountryId": 40,
          "intlCode": "0086",
          "intlTel": "008618876594036",
          "relatedResList": [
            {
              "resourceType": 8,
              "resourceId": 30803494,
              "sellMode": 1
            },
            {
              "resourceType": 8,
              "resourceId": 31218074,
              "sellMode": 1
            }
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


    def Zizhu_Order_params_zizhutrain(self):
        Zizhu_Order_params_zizhutrain = "{" + str(self.Zizhu_Params_channelData()) + "," + str(self.Zizhu_Params_order()) + "," + str(self.Zizhu_Params_subOrders()) + "}"

        return Zizhu_Order_params_zizhutrain


if __name__ == '__main__':

    genp = Zizhu_Order_params_zizhutrain()
    params=genp.Zizhu_Order_params_zizhutrain()
    print (params)



