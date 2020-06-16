# -*- coding:UTF-8 -*-
# @Author  : huangfang

from views.productOrder.BOH_params.Gentuan_BOH_train import Gentuan_BOH_train
from app.actions.tools.commonData import productdata_gentuan
import datetime
import random

class GenTuan_Order_params_gentuantrain1(Gentuan_BOH_train):
    #获取行程1ID
    def gentuan_get_journeyId1(self):
        journeyId1 = Gentuan_BOH_train().getDetailResources()['journeyId1']
        return journeyId1

    # 获取行程2ID
    def gentuan_get_journeyId2(self):
        journeyId2 = Gentuan_BOH_train().getDetailResources()['journeyId2']
        return journeyId2


    #获取行程资源ID
    def gentuan_get_resId1(self):
        resId1 = Gentuan_BOH_train().getDetailResources()['resId1']
        #resourceId1 = '2249640554'
        return resId1

    # 获取行程资源type
    def gentuan_get_resType(self):
        resType = Gentuan_BOH_train().getDetailResources()['resType']
        return resType

    # 获取行程子资源type
    def gentuan_get_resSubType(self):
        resSubType = Gentuan_BOH_train().getDetailResources()['resSubType']
        return resSubType

    #设置出发时间为当前时间+10天
    def gentuan_get_startDate(self):
        startDate = (datetime.datetime.now()+datetime.timedelta(days=10)).strftime("%Y-%m-%d")
        return startDate

    #行程结束时间
    def gentuan_get_endDate(self):
        endDate = (datetime.datetime.now()+datetime.timedelta(days=12)).strftime("%Y-%m-%d")
        return endDate

    # 获取火车票+地接的产品id
    def gentuan_get_productId(self):
        productId = productdata_gentuan["productId_train"]
        return productId

    #获取火车票资源id
    #去程火车票资源
    def gentuan_get_resourceId1(self):
        resourceId1 = Gentuan_BOH_train().getDetailResources()['resId1_train']
        return resourceId1

    #返程火车票资源
    def gentuan_get_resourceId2(self):
        resourceId2 = Gentuan_BOH_train().getDetailResources()['resId2_train']
        return resourceId2

    #获取火车票资源类型
    def gentuan_get_res1_train_type(self):
        res1_train_type = Gentuan_BOH_train().getDetailResources()['res1_train_type']
        return res1_train_type

    def gentuan_get_res2_train_type(self):
        res2_train_type = Gentuan_BOH_train().getDetailResources()['res2_train_type']
        return res2_train_type


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

    def GenTuan_Params_requestId(self):
         requestId1=''.join(random.sample(
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', '0', '1', '2', '3', 'i', 'h', 'g', 'f', 'e',
         'd', 'c', 'b', 'a'], 12))
         requestId="OLBB_PC_0150d01b-4ac1-441b-b710-"+requestId1
         print ("requestId11 is ",requestId)
         return  requestId

    #备用的memberid：6676180,71656257
    def GenTuan_Params_order(self):
        order='''"order": {
                "memberId": 6676180,
                "source": 3,
                "sourceType": 0,
                "systemInfo": {
                  "transferMode": 1,
                  "requestId": '''+self.GenTuan_Params_requestId()+'''
                },
                "interFlightResFlag": 1,
                "extension": {
                  "transferNetReason": ""
                }
                }'''

        return order

    def GenTuan_Params_subOrders(self):
        subOrders='''     "subOrders": [
                {
                    "orderId": 0,
                    "orderType": 11,
                    "totalPrice": 212732,
                    "totalResPrice": 212732,
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
        
                            ],
                            "resourceGenShuttle": [
        
                            ],
                            "resourceAddition": [
        
                            ],
                            "resourceInsurance": [
        
                            ],
                            "resourceTrainTicket": [
                                {
                                    "resourceId": 32048953,
                                    "resourceName": "",
                                    "resourceType": '''+self.gentuan_get_res1_train_type()+''',
                                    "adultCount": 2,
                                    "childCount": 0,
                                    "adultPrice": 553,
                                    "childPrice": 553,
                                    "startDate": "'''+self.gentuan_get_startDate()+'''"
                                },
                                {
                                    "resourceId": 29934910,
                                    "resourceName": "",
                                    "resourceType": '''+self.gentuan_get_res2_train_type()+''',
                                    "adultCount": 2,
                                    "childCount": 0,
                                    "adultPrice": 553,
                                    "childPrice": 553,
                                    "startDate": "'''+self.gentuan_get_endDate()+'''"
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
                            "destinations": "\u82cf\u5dde",
                            "journeyId": '''+self.gentuan_get_journeyId2()+''',
                            "resourceTour": [
                                {
                                    "resourceId": 2249640554,
                                    "resourceName": "[\u6625\u8282]<gwl\u8ddf\u56e2\u6253\u5305\u6e38>\u5c0f\u9ed1\u5361",
                                    "resourceType": '''+self.gentuan_get_resType()+''',
                                    "adultCount": 2,
                                    "childCount": 0,
                                    "memo": "",
                                    "subResourceType": '''+self.gentuan_get_resSubType()+''',
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
                        "price": 106366,
                        "tuniuPrice": 106366,
                        "tuniuChildPrice": 74788,
                        "productId": '''+self.gentuan_get_productId()+''',
                        "productLineDestId": 0,
                        "productLineId": 3742730,
                        "productLineTypeId": 0,
                        "productNewLineTypeId": 11,
                        "productName": "&lt;\u8ddf\u56e2\u706b\u8f66\u7968+\u5730\u63a5\u81ea\u52a8\u5316\u4ea7\u54c1&gt;",
                        "productType": 1,
                        "startCity": "\u5317\u4eac",
                        "startCityCode": 200,
                        "startDate": "'''+self.gentuan_get_startDate()+'''",
                        "productClassId": 1,
                        "productChildClassId": 0,
                        "productLineDesName": 5267,
                        "productLineDesGroup": 16,
                        "productLineDesType": 11
                    },
                    "requirement": {
                        "planId": 93247,
                        "backCityCode": 200,
                        "backCityName": "\u5317\u4eac",
                        "bookCity": "\u5317\u4eac",
                        "bookCityCode": 200,
                        "departureDate": "2019-02-28",
                        "endDate": "2019-03-02",
                        "desCity": "\u82cf\u5dde",
                        "desCityCode": 1615,
                        "groupCost": 212732,
                        "hasOld": 0,
                        "isL": 0,
                        "roomCharge": 4,
                        "roomChargeRemark": "",
                        "startCity": "\u5317\u4eac",
                        "startCityCode": 200,
                        "adultCount": 2,
                        "childCount": 0
                    },
                    "touristList": [
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
                                {
                                    "resourceType": 8,
                                    "resourceId": 32048953,
                                    "sellMode": 1
                                },
                                {
                                    "resourceType": 8,
                                    "resourceId": 29934910,
                                    "sellMode": 1
                                }
                            ],
                            "isAdult": 1,
                            "touristType": 0
                        },
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
                                    "resourceId": 32048953,
                                    "sellMode": 1
                                },
                                {
                                    "resourceType": 8,
                                    "resourceId": 29934910,
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


    def GenTuan_Order_params_gentuantrain1(self):
        GenTuan_Order_params_gentuantrain1 = "{" + str(self.GenTuan_Params_channelData()) + "," + str(self.GenTuan_Params_order()) + "," + str(self.GenTuan_Params_subOrders()) + "}"

        return GenTuan_Order_params_gentuantrain1


if __name__ == '__main__':

    genp = GenTuan_Order_params_gentuantrain1()
    params=genp.GenTuan_Order_params_gentuantrain1()
    print (params)



