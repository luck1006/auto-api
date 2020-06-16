# -*- coding:UTF-8 -*-
# @Author  : huangfang

# from _02Businesskeyword._01Package.abstract.prdTourJourneyResAbtract import prdTourJourneyResAbtract
from _01Commonkeyword import BaseApplication
from _02Businesskeyword._01Package.abstract.prdTourAbstract import prdTourAbstract
# from _02Businesskeyword._01Package.abstract.prdTourJourneyResAbtract import prdTourJourneyResAbtract
from _02Businesskeyword._01Package.businessKeyword import businessKeyword
from _01Commonkeyword import InterfaceKeyword
from _01Commonkeyword._01Basemethod.BaseInterface import BaseInterface
import json

{
    "channelData": {
        "callPhone": "",
        "clientType": 20000,
        "clientTypeExpand": 0,
        "fromUrl": "",
        "pSource": 3,
        "pValue": "100",
        "channelRelationId": "010100000020"
    },
    "order": {
        "memberId": 6676180,
        "source": 3,
        "sourceType": 0,
        "systemInfo": {
            "transferMode": 1,
            "requestId": "OLBB_PC_82ef98bb-44b3-4f72-a024-258a274e56b2"
        },
        "interFlightResFlag": 1,
        "extension": {
            "transferNetReason": ""
        }
    },
    "subOrders": [
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
                    "journeyId": 598243,
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
                            "resourceType": 8,
                            "adultCount": 2,
                            "childCount": 0,
                            "adultPrice": 553,
                            "childPrice": 553,
                            "startDate": "2019-02-28"
                        },
                        {
                            "resourceId": 31488015,
                            "resourceName": "",
                            "resourceType": 8,
                            "adultCount": 2,
                            "childCount": 0,
                            "adultPrice": 553,
                            "childPrice": 553,
                            "startDate": "2019-03-02"
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
                    "journeyId": 598244,
                    "resourceTour": [
                        {
                            "resourceId": 2249640554,
                            "resourceName": "[\u6625\u8282]<gwl\u8ddf\u56e2\u6253\u5305\u6e38>\u5c0f\u9ed1\u5361",
                            "resourceType": 27,
                            "adultCount": 2,
                            "childCount": 0,
                            "memo": "",
                            "subResourceType": 1,
                            "endDate": "2019-03-01",
                            "startDate": "2019-02-28"
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
                "endDate": "2019-03-02",
                "night": 2,
                "price": 106366,
                "tuniuPrice": 106366,
                "tuniuChildPrice": 74788,
                "productId": 210017619,
                "productLineDestId": 0,
                "productLineId": 3742730,
                "productLineTypeId": 0,
                "productNewLineTypeId": 11,
                "productName": "&lt;\u8ddf\u56e2\u706b\u8f66\u7968+\u5730\u63a5\u81ea\u52a8\u5316\u4ea7\u54c1&gt;",
                "productType": 1,
                "startCity": "\u5317\u4eac",
                "startCityCode": 200,
                "startDate": "2019-02-28",
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
                            "resourceId": 31488015,
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
                            "resourceId": 31488015,
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
    ]
}