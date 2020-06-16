# -*- coding:UTF-8 -*-
# @Author  : huangfang

from views.productOrder.BOH_params.Zizhu_BOH_flight import Zizhu_BOH_flight
from app.actions.tools.commonData import productdata_zizhu
import datetime

class Zizhu_Order_params_zizhuflight(Zizhu_BOH_flight):
    #获取行程1ID
    def zizhu_get_journeyId1(self):
        journeyId1 = Zizhu_BOH_flight().getDetailResources()['journeyId1']
        return journeyId1

    # 获取行程2ID
    def zizhu_get_journeyId2(self):
        journeyId2 = Zizhu_BOH_flight().getDetailResources()['journeyId2']
        return journeyId2


    #获取行程资源ID1
    def zizhu_get_resId1(self):
        resId1 = Zizhu_BOH_flight().getDetailResources()['resId1']
        #resourceId1 = '2249640554'
        return resId1

    # 获取行程资源ID2
    def zizhu_get_resId2(self):
        resId2 = Zizhu_BOH_flight().getDetailResources()['resId2']
        # resourceId1 = '2249640554'
        return resId2

    # 获取行程资源type
    def zizhu_get_resType(self):
        resType = Zizhu_BOH_flight().getDetailResources()['resType']
        return resType

    # 获取行程子资源type
    def zizhu_get_resSubType(self):
        resSubType = Zizhu_BOH_flight().getDetailResources()['resSubType']
        return resSubType

    #设置出发时间为当前时间+10天
    def zizhu_get_startDate(self):
        startDate = (datetime.datetime.now()+datetime.timedelta(days=10)).strftime("%Y-%m-%d")
        return startDate

    #行程行程第二天
    def zizhu_get_startDate1(self):
        startDate1 = (datetime.datetime.now()+datetime.timedelta(days=11)).strftime("%Y-%m-%d")
        return startDate1

    #行程行程第三天
    def zizhu_get_startDate2(self):
        startDate2 = (datetime.datetime.now()+datetime.timedelta(days=12)).strftime("%Y-%m-%d")
        return startDate2

    #行程行程第四天
    def zizhu_get_startDate3(self):
        startDate3 = (datetime.datetime.now()+datetime.timedelta(days=13)).strftime("%Y-%m-%d")
        return startDate3


    #行程行程结束
    def zizhu_get_endDate(self):
        endDate = (datetime.datetime.now()+datetime.timedelta(days=14)).strftime("%Y-%m-%d")
        return  endDate

    #获取产品iden
    def zizhu_get_productId(self):
        productId = productdata_zizhu["productId_zizhu_flight"]
        return productId
        # 获取机票资源id

    def zizhu_get_resourceId1(self):
        resourceId1 = Zizhu_BOH_flight().getDetailResources()['resId1_flight']
        return resourceId1

        # 获取机票资源类型

    def zizhu_get_res1_flight_type(self):
        res1_flight_type = Zizhu_BOH_flight().getDetailResources()['res1_flight_type']
        return res1_flight_type

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
            "totalPrice": 10192,
            "totalResPrice": 10192,
            "contactList": [
                {
                    "appellation": 1,
                    "email": "test1234567@test.tuniu.com",
                    "isDefault": 1,
                    "name": "中文",
                    "phone": null,
                    "tel": "13062527078",
                    "type": 2,
                    "telCountryId": 40,
                    "intlCode": "0086",
                    "intlTel": "008613062527078"
                }
            ],
            "promotionList": [],
            "journey": [
                {
                    "journeySeqNum": 0,
                    "isChange": 0,
                    "destinations": "",
                    "journeyId": '''+self.zizhu_get_journeyId1()+''',
                    "resourceTour": [],
                    "resourceScatterFlightTicket": [
                        {
                            "extension": {
                                "interFlightFlag": 1
                            },
                            "resourceId": '''+self.zizhu_get_resourceId1()+''',
                            "resourceName": "",
                            "resourceType": 21,
                            "adultCount": 2,
                            "childCount": 0,
                            "startDate": "'''+self.zizhu_get_startDate()+'''",
                            "externalInfo": null,
                            "solutionId": 1,
                            "adultPrice": 3724
                        }
                    ],
                    "resourceFlightTicket": [],
                    "resourceGenShuttle": [],
                    "resourceAddition": [],
                    "resourceInsurance": [],
                    "resourceTrainTicket": [],
                    "resourceHotelRoom": [],
                    "resourceBusTicket": [],
                    "resourceMenpiao": [],
                    "resourceVisa": [],
                    "resourcePackage": [],
                    "resourceCon": [],
                    "resourceLocal": []
                },
                {
                    "journeySeqNum": 1,
                    "isChange": 0,
                    "destinations": "香港",
                    "journeyId": 598004,
                    "resourceTour": [],
                    "resourceFlightTicket": [],
                    "resourceAddition": [
                        {
                            "resourceId": '''+self.zizhu_get_resId2()+''',
                            "resourceName": "【当地玩乐】香港迪士尼乐园1日长者门票（65岁或以上）",
                            "resourceType": 18,
                            "adultCount": 2,
                            "adultPrice": 100,
                            "childCount": 0,
                            "childPrice": 100,
                            "startDate": "'''+self.zizhu_get_startDate()+'''",
                            "endDate": "'''+self.zizhu_get_endDate()+'''",
                            "memo": "",
                            "subResourceType": 2
                        }
                    ],
                    "resourceInsurance": [],
                    "resourceHotelRoom": [
                        {
                            "resourceId": '''+self.zizhu_get_resId1()+''',
                            "resourceName": "全季酒店(上海虹桥中山西路店)[无早](限时特惠)",
                            "resourceType": 2,
                            "hotelId": "2147616112",
                            "memo": "",
                            "isIndividualHotel": 0,
                            "hotelRoomDetail": [
                                {
                                    "startDate": "'''+self.zizhu_get_startDate()+'''",
                                    "endDate": "'''+self.zizhu_get_startDate1()+'''",
                                    "adultCount": 1,
                                    "price": 270
                                },
                                {
                                    "startDate": "'''+self.zizhu_get_startDate1()+'''",
                                    "endDate": "'''+self.zizhu_get_startDate2()+'''",
                                    "adultCount": 1,
                                    "price": 270
                                },
                                {
                                    "startDate": "'''+self.zizhu_get_startDate2()+'''",
                                    "endDate": "'''+self.zizhu_get_startDate3()+'''",
                                    "adultCount": 1,
                                    "price": 270
                                },
                                {
                                    "startDate": "'''+self.zizhu_get_startDate3()+'''",
                                    "endDate": "'''+self.zizhu_get_endDate()+'''",
                                    "adultCount": 1,
                                    "price": 270
                                }
                            ]
                        }
                    ],
                    "resourceBusTicket": [],
                    "resourceMenpiao": [],
                    "resourceVisa": [],
                    "resourcePackage": [],
                    "resourceCon": [],
                    "resourceLocal": []
                }
            ],
            "product": {
                "desCity": "香港",
                "desCityCode": 1300,
                "duration": 1,
                "endDate": "'''+self.zizhu_get_startDate()+'''",
                "night": 8,
                "price": 2331,
                "tuniuPrice": 2331,
                "tuniuChildPrice": 1024,
                "productId": '''+self.zizhu_get_productId()+''',
                "productLineDestId": 0,
                "productLineId": 15393,
                "productLineTypeId": 0,
                "productNewLineTypeId": 11,
                "productName": "&lt;自助游自动化机票+资源勿动&gt;",
                "productType": 2,
                "startCity": "南京",
                "startCityCode": 1602,
                "startDate": "'''+self.zizhu_get_startDate()+'''",
                "productClassId": 2,
                "productChildClassId": 16,
                "productLineDesName": 10,
                "productLineDesGroup": 156,
                "productLineDesType": 11
            },
            "requirement": {
                "planId": 149128477,
                "backCityCode": 1602,
                "backCityName": "南京",
                "bookCity": "南京",
                "bookCityCode": 1602,
                "departureDate": "'''+self.zizhu_get_startDate()+'''",
                "endDate": "'''+self.zizhu_get_endDate()+'''",
                "desCity": "香港",
                "desCityCode": 1300,
                "groupCost": 4762,
                "hasOld": 0,
                "isL": 0,
                "roomCharge": 4,
                "roomChargeRemark": "",
                "startCity": "南京",
                "startCityCode": 1602,
                "adultCount": 2,
                "childCount": 0
            },
            "touristList": [
                {
                    "name": "段永华",
                    "tel": "13842774307",
                    "firstname": null,
                    "lastname": null,
                    "country": "中国",
                    "psptType": 2,
                    "psptId": "EF7819235",
                    "psptEndDate": "2029-03-20",
                    "sex": 0,
                    "personId": 49690715,
                    "birthday": "1981-02-05",
                    "telCountryId": 40,
                    "intlCode": "0086",
                    "intlTel": "008613842774307",
                    "relatedResList": [],
                    "isAdult": 1,
                    "touristType": 0,
                    "flightResIds": [
                        1676998825
                    ]
                },
                {
                    "name": "张爱军",
                    "tel": "13062527078",
                    "firstname": null,
                    "lastname": null,
                    "country": "中国",
                    "psptType": 1,
                    "psptId": "210323199004241620",
                    "psptEndDate": "",
                    "sex": 0,
                    "personId": 48457219,
                    "birthday": "1990-04-24",
                    "telCountryId": 40,
                    "intlCode": "0086",
                    "intlTel": "008613062527078",
                    "relatedResList": [],
                    "isAdult": 1,
                    "touristType": 0,
                    "flightResIds": [
                        1676998825
                    ]
                }
            ],
            "couponList": [
                {
                    "couponType": 1,
                    "useValue": 0
                }
            ],
            "invoiceList": []
        }
    ]'''



        return subOrders


    def Zizhu_Order_params_zizhuflight(self):
        Zizhu_Order_params_zizhuflight = "{" + str(self.Zizhu_Params_channelData()) + "," + str(self.Zizhu_Params_order()) + "," + str(self.Zizhu_Params_subOrders()) + "}"

        return Zizhu_Order_params_zizhuflight


if __name__ == '__main__':

    genp = Zizhu_Order_params_zizhuflight()
    params=genp.Zizhu_Order_params_zizhuflight()
    print (params)



