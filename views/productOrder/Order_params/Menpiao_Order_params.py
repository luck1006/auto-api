# -*- coding:UTF-8 -*-
# @Author  : huangfang

from views.productOrder.BOH_params.Menpiao_BOH import Menpiao_BOH
from app.actions.tools.commonData import productdata_menpiao
import datetime
import random,string

class Menpiao_Order_params(Menpiao_BOH):
    #获取行程1ID
    def menpiao_get_journeyId1(self):
        journeyId1 = Menpiao_BOH().getDetailResources()['journeyId1']
        return journeyId1

    # 获取行程2ID
    def menpiao_get_journeyId2(self):
        journeyId2 = Menpiao_BOH().getDetailResources()['journeyId2']
        return journeyId2


    #获取行程资源ID
    def menpiao_get_resId1(self):
        resId1 = Menpiao_BOH().getDetailResources()['resId1']
        return resId1

    # 获取行程资源type
    def menpiao_get_resType(self):
        resType = Menpiao_BOH().getDetailResources()['resType']
        return resType

    # 获取行程子资源type
    def menpiao_get_resSubType(self):
        resSubType = Menpiao_BOH().getDetailResources()['resSubType']
        return resSubType

    #设置出发时间为当前时间+10天
    def menpiao_get_startDate(self):
        startDate = (datetime.datetime.now()+datetime.timedelta(days=10)).strftime("%Y-%m-%d")
        return startDate

    #行程结束时间
    def menpiao_get_endDate(self):
        endDate = (datetime.datetime.now()+datetime.timedelta(days=12)).strftime("%Y-%m-%d")
        return endDate

    # 获取门票产品id
    def menpiao_get_productId(self):
        productId = productdata_menpiao["productId_menpiao"]
        return productId

    ## 获取门票requestid
    def menpiao_get_requestId(self):
        requestId = ""
        num = string.ascii_letters + string.digits
        for i in range(32):
            requestId += random.choice(num)
        # print (requestId)
        return requestId



    def Menpiao_Params_channelData(self):
        channelData='''
        "channelData": {
        "clientType": "20000",
        "fromUrl": "",
        "pExt": "__",
        "pValue": "200"
  }'''

        return channelData
    #备用的memberid：6676180,71656257
    def Menpiao_Params_order(self):
        order='''"order": {
    "interFlightResFlag": 0,
    "isAppOrder": 0,
    "isEvilOrder": 0,
    "memberId": 6676180,
    "source": 3,
    "systemInfo": {
      "requestId": "'''+self.menpiao_get_requestId()+'''",
      "transferMode": 0
    }
  }'''

        return order

    def Menpiao_Params_subOrders(self):
        subOrders='''     "subOrders": [
    {
      "contactList":[
        {
          "isDefault": 1,
          "name": "途牛测试",
          "relatedResList": [
            {
              "bookingInfo": "[{\\"bookInfoGroupId\\":1,\\"bookInfoGroupName\\":\\"取票人\\",\\"bookInfoItemId\\":1,\\"bookInfoItemName\\":\\"姓名\\",\\"nameToGuest\\":\\"姓名\\",\\"stage\\":1,\\"textValue\\":\\"途牛测试\\"},{\\"bookInfoGroupId\\":1,\\"bookInfoGroupName\\":\\"取票人\\",\\"bookInfoItemId\\":2,\\"bookInfoItemName\\":\\"手机号\\",\\"nameToGuest\\":\\"手机号\\",\\"stage\\":1,\\"textValue\\":\\"18876594036\\"}]",
              "relationType": 2,
              "resourceId": 2147595523,
              "resourceType": 4
            }
          ],
          "tel": "18876594036"
        }
         ],
      "couponList": [
        
      ],
      "journey": [
        {
          "journeyId": '''+self.menpiao_get_journeyId2()+''',
          "journeySeqNum": 1,
          "resourceInsurance": [
            
          ],
          "resourceMenpiao": [
            {
              "adultCount": 1,
              "childCount": 0,
              "endDate": "'''+self.menpiao_get_endDate()+'''",
              "resourceId": '''+self.menpiao_get_resId1()+''',
              "resourceName": "崔门票sit自动化01勿动2017-02-14",
              "resourceType": '''+self.menpiao_get_resType()+''',
              "startDate": "'''+self.menpiao_get_startDate()+'''"
            }
          ]
        }
      ],
      "orderType": 75,
      "product": {
        "desCityCode": 1602,
        "isGiveIns": 0,
        "productClassId": 6,
        "productId": '''+self.menpiao_get_productId()+''',
        "productLineId": 2,
        "productName": "<门票产品黑卡测试-单票>20190102",
        "productType": 6,
        "startCityCode": 0,
        "startDate": "'''+self.menpiao_get_startDate()+'''"
      },
      "promotionList": [
        
      ],
      "requirement": {
        "adultCount": 1,
        "bookCityCode": 2500,
        "childCount": 0,
        "departureDate": "'''+self.menpiao_get_startDate()+'''",
        "desCityCode": 1602,
        "duration": 1,
        "startCityCode": 0
      },
      "totalPrice": 700,
      "touristList": [
        
      ]
    }
  ]'''



        return subOrders


    def Menpiao_Order_params(self):
        Menpiao_Order_params = "{" + str(self.Menpiao_Params_channelData()) + "," + str(self.Menpiao_Params_order()) + "," + str(self.Menpiao_Params_subOrders())+ "}"

        return Menpiao_Order_params


if __name__ == '__main__':

    genp = Menpiao_Order_params()
    params=genp.Menpiao_Order_params()
    print (params)



