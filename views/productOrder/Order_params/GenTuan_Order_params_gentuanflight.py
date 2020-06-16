# -*- coding:UTF-8 -*-
# @Author  : huangfang

from views.productOrder.BOH_params.Gentuan_BOH_flight import Gentuan_BOH_flight
from app.actions.tools.commonData import productdata_gentuan
import datetime

class GenTuan_Order_params_gentuanflight(Gentuan_BOH_flight):
    #获取行程1ID
    def gentuan_get_journeyId1(self):
        journeyId1 = Gentuan_BOH_flight().getDetailResources()['journeyId1']
        return journeyId1

    # 获取行程2ID
    def gentuan_get_journeyId2(self):
        journeyId2 = Gentuan_BOH_flight().getDetailResources()['journeyId2']
        return journeyId2


    #获取行程资源ID
    def gentuan_get_resId1(self):
        resId1 = Gentuan_BOH_flight().getDetailResources()['resId1']
        return resId1
    def gentuan_get_resId2(self):
        resId2 = Gentuan_BOH_flight().getDetailResources()['resId2']
        return resId2
    def gentuan_get_resId3(self):
        resId3 = Gentuan_BOH_flight().getDetailResources()['resId3']
        return resId3

    # 获取行程资源type
    def gentuan_get_resType1(self):
        resType1 = Gentuan_BOH_flight().getDetailResources()['resType1']
        return resType1
    def gentuan_get_resType2(self):
        resType2 = Gentuan_BOH_flight().getDetailResources()['resType2']
        return resType2
    def gentuan_get_resType3(self):
        resType3 = Gentuan_BOH_flight().getDetailResources()['resType3']
        return resType3

    # 获取行程子资源type
    def gentuan_get_resSubType1(self):
        resSubType1 = Gentuan_BOH_flight().getDetailResources()['resSubType1']
        return resSubType1
    def gentuan_get_resSubType2(self):
        resSubType2 = Gentuan_BOH_flight().getDetailResources()['resSubType2']
        return resSubType2
    def gentuan_get_resSubType3(self):
        resSubType3 = Gentuan_BOH_flight().getDetailResources()['resSubType3']
        return resSubType3

    # 获取机票资源id
    def gentuan_get_resourceId1(self):
        resourceId1 = Gentuan_BOH_flight().getDetailResources()['resId1_flight']
        return resourceId1

    # 获取机票资源类型
    def gentuan_get_res1_flight_type(self):
        res1_flight_type = Gentuan_BOH_flight().getDetailResources()['res1_flight_type']
        return res1_flight_type
    
    #设置出发时间为当前时间+10天
    def gentuan_get_startDate(self):
        startDate = (datetime.datetime.now()+datetime.timedelta(days=10)).strftime("%Y-%m-%d")
        return startDate

    #行程结束时间
    def gentuan_get_endDate(self):
        endDate = (datetime.datetime.now()+datetime.timedelta(days=12)).strftime("%Y-%m-%d")
        return endDate

    #获取产品id
    def gentuan_get_productId(self):
        productId = productdata_gentuan["productId_flight"]
        return productId

    #获取产品出发城市
    def gentuan_get_startCityCode(self):
        #startCityCode = Gentuan_BOH().getDetailResources()['startCityCode']
        startCityCode = '1602'
        return startCityCode

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
    #备用的memberid：6676180,71656257,71656195
    def GenTuan_Params_order(self):
        order='''"order": {
                "memberId": 6676180,
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

    def GenTuan_Params_subOrders(self):
        subOrders=''' "subOrders": [
    {
      "orderId": 0,
      "orderType": 11,
      "totalPrice": 334280,
      "totalResPrice": 334280,
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
          "journeyId": '''+self.gentuan_get_journeyId1()+''',
          "resourceTour": [
            
          ],
          "resourceScatterFlightTicket": [
            
          ],
          "resourceFlightTicket": [
            {
              "resourceId": '''+self.gentuan_get_resourceId1()+''',
              "resourceName": "",
              "resourceType": '''+self.gentuan_get_res1_flight_type()+''',
              "adultCount": 3,
              "childCount": 0,
              "startDate": "'''+self.gentuan_get_startDate()+'''",
              "ibeRule": [
                
              ],
              "externalInfo": null,
              "solutionId": 0,
              "adultPrice": 3000,
              "childPrice": 2250
            }
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
          "journeyId": '''+self.gentuan_get_journeyId2()+''',
          "resourceTour": [
            {
              "resourceId": '''+self.gentuan_get_resId2()+''',
              "resourceName": "[\u6625\u8282]<gwl\u8ddf\u56e2\u6253\u5305\u6e38>\u5c0f\u9ed1\u5361",
              "resourceType": '''+self.gentuan_get_resType2()+''',
              "adultCount": 3,
              "childCount": 0,
              "memo": "",
              "subResourceType": '''+self.gentuan_get_resSubType2()+''',
              "endDate": "'''+self.gentuan_get_endDate()+'''",
              "startDate": "'''+self.gentuan_get_startDate()+'''"
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
        "endDate": "'''+self.gentuan_get_endDate()+'''",
        "night": 2,
        "price": 111760,
        "tuniuPrice": 111760,
        "tuniuChildPrice": 78682,
        "productId": '''+self.gentuan_get_productId()+''',
        "productLineDestId": 0,
        "productLineId": 40262,
        "productLineTypeId": 0,
        "productNewLineTypeId": 12,
        "productName": "&lt;\u81ea\u52a8\u5316\u751f\u6210\u8ddf\u56e2\u4ea7\u54c1&gt;",
        "productType": 1,
        "startCity": "\u5357\u4eac",
        "startCityCode": 1602,
        "startDate": "'''+self.gentuan_get_startDate()+'''",
        "productClassId": 1,
        "productChildClassId": 0,
        "productLineDesName": 97,
        "productLineDesGroup": 17,
        "productLineDesType": 12
      },
      "requirement": {
        "planId": 93427,
        "backCityCode": 1602,
        "backCityName": "\u5357\u4eac",
        "bookCity": "\u5317\u4eac",
        "bookCityCode": 200,
        "departureDate": "'''+self.gentuan_get_startDate()+'''",
        "endDate": "'''+self.gentuan_get_endDate()+'''",
        "desCity": "\u82cf\u5dde",
        "desCityCode": 1615,
        "groupCost": 334280,
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
          "touristType": 0,
          "flightResIds": [
            2249552051
          ]
        },
        {
          "name": "ZHOUHUI",
          "tel": "18876594036",
          "firstname": null,
          "lastname": null,
          "country": "\u4e2d\u56fd",
          "psptType": 2,
          "psptId": "G12344678",
          "psptEndDate": "2021-01-01",
          "sex": 1,
          "personId": 1948279,
          "birthday": "1975-06-19",
          "telCountryId": 40,
          "intlCode": "0086",
          "intlTel": "008618876594036",
          "relatedResList": [
            
          ],
          "isAdult": 1,
          "touristType": 0,
          "flightResIds": [
            2249552051
          ]
        },
        {
          "name": "TESTTST",
          "tel": "15000123456",
          "firstname": null,
          "lastname": null,
          "country": "\u4e2d\u56fd",
          "psptType": 999,
          "psptId": null,
          "psptEndDate": "",
          "sex": 9,
          "personId": 1945223,
          "birthday": "1985-01-01",
          "telCountryId": 31,
          "intlCode": "0061",
          "intlTel": "006115000123456",
          "relatedResList": [
            
          ],
          "isAdult": 1,
          "touristType": 0,
          "flightResIds": [
            2249552051
          ]
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


    def GenTuan_Order_params_gentuanflight(self):
        GenTuan_Order_params_gentuanflight = "{" + str(self.GenTuan_Params_channelData()) + "," + str(self.GenTuan_Params_order()) + "," + str(self.GenTuan_Params_subOrders()) + "}"

        return GenTuan_Order_params_gentuanflight


if __name__ == '__main__':

    genp = GenTuan_Order_params_gentuanflight()
    genp = GenTuan_Order_params_gentuanflight()
    params=genp.GenTuan_Order_params_gentuanflight()
    print (params)



