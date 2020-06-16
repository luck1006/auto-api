# -*- coding:UTF-8 -*-
# @Author  : huangfang

from views.productOrder.BOH_params.Zizhu_BOH_ziyuanzuhe import Zizhu_BOH_ziyuanzuhe
from app.actions.tools.commonData import productdata_zizhu
import datetime

class Zizhu_Order_params_zizhuziyuanzuhe(Zizhu_BOH_ziyuanzuhe):
    #获取行程1ID
    def zizhu_get_journeyId1(self):
        journeyId1 = Zizhu_BOH_ziyuanzuhe().getDetailResources()['journeyId1']
        return journeyId1

    # 获取行程2ID
    def zizhu_get_journeyId2(self):
        journeyId2 = Zizhu_BOH_ziyuanzuhe().getDetailResources()['journeyId2']
        return journeyId2


    #获取行程资源ID1
    def zizhu_get_resId1(self):
        resId1 = Zizhu_BOH_ziyuanzuhe().getDetailResources()['resId1']
        #resourceId1 = '2249640554'
        return resId1

    # 获取行程资源ID2
    def zizhu_get_resId2(self):
        resId2 = Zizhu_BOH_ziyuanzuhe().getDetailResources()['resId2']
        # resourceId1 = '2249640554'
        return resId2

    # 获取行程资源type
    def zizhu_get_resType(self):
        resType = Zizhu_BOH_ziyuanzuhe().getDetailResources()['resType']
        return resType

    # 获取行程子资源type
    def zizhu_get_resSubType(self):
        resSubType = Zizhu_BOH_ziyuanzuhe().getDetailResources()['resSubType']
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
        productId = productdata_zizhu["productId_zizhu_ziyuanzuhe"]
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
        subOrders='''  "subOrders": [
    {
      "orderId": 0,
      "orderType": 53,
      "totalPrice": 1000,
      "totalResPrice": 1000,
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
          "destinations": "",
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
            {
              "resourceId": '''+self.zizhu_get_resId1()+''',
              "resourceName": "\u4e0a\u6d77\u675c\u838e\u592b\u4eba\u8721\u50cf\u9986-\u6761\u4ef6\u9000",
              "resourceType": 4,
              "adultPrice": 1000,
              "adultCount": 1,
              "startDate": "'''+self.zizhu_get_startDate()+'''",
              "endDate": "'''+self.zizhu_get_endDate()+'''",
              "memo": "",
              "limitNum": 0,
              "subResourceType": 4
            }
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
        "desCity": "\u4e0a\u6d77",
        "desCityCode": 2500,
        "duration": 2,
        "endDate": "'''+self.zizhu_get_endDate()+'''",
        "night": 1,
        "price": 1000,
        "tuniuPrice": 1000,
        "tuniuChildPrice": 0,
        "productId": '''+self.zizhu_get_productId()+''',
        "productLineDestId": 0,
        "productLineId": 14322,
        "productLineTypeId": 0,
        "productNewLineTypeId": 11,
        "productName": "&lt;\u81ea\u52a9\u6e38\u81ea\u52a8\u5316\u7ebf\u8def\u8d44\u6e90\u7ec4\u5408&gt;2016-09-18",
        "productType": 2,
        "startCity": "\u5357\u4eac",
        "startCityCode": 1602,
        "startDate": "'''+self.zizhu_get_startDate()+'''",
        "productClassId": 2,
        "productChildClassId": 16,
        "productLineDesName": 7,
        "productLineDesGroup": 34,
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
        "desCity": "\u4e0a\u6d77",
        "desCityCode": 2500,
        "groupCost": 1000,
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
            {
              "resourceId": 2250693514,
              "resourceType": 4
            }
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


    def Zizhu_Order_params_zizhuziyuanzuhe(self):
        Zizhu_Order_params_zizhuziyuanzuhe = "{" + str(self.Zizhu_Params_channelData()) + "," + str(self.Zizhu_Params_order()) + "," + str(self.Zizhu_Params_subOrders()) + "}"

        return Zizhu_Order_params_zizhuziyuanzuhe


if __name__ == '__main__':

    genp = Zizhu_Order_params_zizhuziyuanzuhe()
    params=genp.Zizhu_Order_params_zizhuziyuanzuhe()
    print (params)



