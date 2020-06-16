# /usr/bin/python
# -*- coding:utf-8 -*-
"""
# project:autoapi
# user:: liju
@author: liju
@time: 2019-10-8 15:11
"""
import datetime
import random
import time

from views.quicklyOrder.FHPackagequicklyOrder.FHPackageConf import FHPackageConf
from views.quicklyOrder.Interface import InterfaceBase

"""获取session"""
class Begin_Session(InterfaceBase):
    # 定义接口地址变量
    config = "Auth_BeginSession"

    def __init__(self, cParam={"cc": 1602, "ct": 10, "p": 14588, "ov": 20, "dt": 0, "v": "9.53.0"}, session=None):
        # 获取本接口url
        urldata = FHPackageConf[self.config]
        super().__init__(urlData=urldata, cParam=cParam, session=session)

    def setReqParam(self):
        """"
        设置请求参数的另一种方式，可以通过dParam直接设置请求参数，这样的话 需要调用方拼接好参数
        增加这种方式是想调用方不用管具体数据格式，只需要传递过来参数即可，不同的接口因为请求的入参个数都不一样，甚至还需要取上下文接口才能组合成完整入参，所以对入参不做特别限制了，不同接口根据情况定义这个接口
        """
        createTime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        lg = int(round(time.time() * 1000))
        print("lg is " +  str(lg))
        self.pData = {"activateTimes": 0, "sessionId": "",
                      "parameters": {"token": "OTU0NTQ3NTMzZjBjNjllYmJjNWUzNDM4YmYwNzBjMjU=",
                                     "imei": "954547533f0c69ebbc5e3438bf070c259dc3966f",
                                     "partner": 14588, "apiType": 0, "clientType": 10,
                                     "deviceType": 0, "version": "10.7.1",
                                     "expireDuration": 336,
                                     "sid": "0609784551345648291846272130568961600",
                                     "createTime": createTime, "lg": lg}}


    def getSessionId(self):
        return self.responsedata['data']['sessionId']

"""登陆"""
class Login(InterfaceBase):

    def __init__(self, cParam, sessionId =None):
        # 获取本接口url
        urldata = FHPackageConf['Auth_Login']
        super().__init__(urlData=urldata, cParam=cParam,session =sessionId)



    def setReqParam(self, sessionId):
        self.dParam = {"password": "5228537688dcbf85c87e59c1ae6b11a3", "loginId": "13584089726",
                       "deviceId": "LGkIJiCCQge7LCejsxyQI1YneKna5kiYD7hmIHKqg7IiuPP-hHxLpsohYiCjUoL39ZXO06jW0I3-5tkQa2KpggpfBlPiWTdomOsH1nzC8Gvh1KyjGVDgj3BlAcH6VxazxQMEkWEpqrRfd0LRWi9A6njB5i5ucMs_",
                       "sessionId": sessionId, "intlCode": "", "captcha": ""}

"""推荐接口"""
class FHPackage_getDefaultRecommend(InterfaceBase):
    # 定义接口变量地址
    config = "getDefaultRecommend"

    def __init__(self, cParam, session=None):
        # 获取本接口URL
        urlData = FHPackageConf[self.config]
        super().__init__(urlData=urlData, cParam=cParam, session=session)

    def setReqParam(self, bookCityCode, bookCityName, departCityCode, departCityName, departDate, adultNum, childNum,
                    isInternational, journeyType,
                    cabinType, startCityCode, startCityName, destCityCode, destCityName, journeyDepartDate,
                    journeyEndDate, sessionId,packType=1):
        self.dParam = {
            "packType":packType,
            "bookCityCode": bookCityCode,
            "bookCityName": bookCityName,
            "departCityCode": departCityCode,
            "departCityName": departCityName,
            "departDate": departDate,
            "adultNum": adultNum,
            "childNum": childNum,
            "isInternational": isInternational,
            "journeyType": journeyType,
            "journeyList": [{"cabinType": cabinType, "startCityCode": startCityCode, "startCityName": startCityName,
                             "destCityCode": destCityCode, "destCityName": destCityName,
                             "journeyDepartDate": journeyDepartDate, "journeyEndDate": journeyEndDate}],
            "sessionId": sessionId}

    ###自动随机获取一个随机团期，日期距离当前时间1个月
    def getRandomTourdate(self):
        """calendarInfo
        随机获取一个有效出游日期
        :return:
        """
        now = datetime.datetime.now()
        start_delta = datetime.timedelta(days=30)
        start_days = now + start_delta
        print(str(start_days.date()))

        startint = random.randint(0, 15)
        start_delta1 = datetime.timedelta(days=startint)
        journeyDepartDate = start_days + start_delta1
        print(str(journeyDepartDate.date()))

        touristduration = random.randint(1, 5)
        end_delta11 = datetime.timedelta(days=touristduration)
        journeyEndDate = journeyDepartDate + end_delta11
        print(str(journeyEndDate.date()))

    def checkflight(self):
        if not self.responsedata['data'] is None:
            if self.responsedata['data']['flightList']:
                return True
            else:
                return False

    def checkHotel(self):
        if not self.responsedata['data']['hotelList'] is None:
            if not self.responsedata['data']['hotelList'][0] is None:
                return True
        else:
            return False

        ###判断去程是否是中转

    def checkdepartflightistransit(self):
        if not self.responsedata['data']['flightList'] is None:
            if not self.responsedata['data']['flightList'][0] is None:
                if len(self.responsedata['data']['flightList'][0]['flightOptions'][0]['flightItems']) > 2:
                    return True
                else:
                    return False
        else:
            return False

        ###判断返程是否是中转

    def checkdestflightistransit(self):
        if not self.responsedata['data']['flightList'] is None:
            if not self.responsedata['data']['flightList'][0] is None:
                if len(self.responsedata['data']['flightList'][0]['flightOptions'][1]['flightItems']) > 2:
                    return True
                else:
                    return False
        else:
            return False

    """机酒信息是否完善"""
    def checkFHResourceComplete(self):
        if self.checkflight() and self.checkHotel():
            return True
        else:
            return False

    ###判断返程是否是中转
    def checkdestflightistransit(self):
        if not self.responsedata['data']['flightList'] is None:
            if not self.responsedata['data']['flightList'][0] is None:
                if len(self.responsedata['data']['flightList'][0]['flightOptions'][1]['flightItems']) > 2:
                    return True
                else:
                    return False
        else:
            return False

    # 获取机票的总价，航班和舱等信息
    def getFlightInfo(self):
        # DepartFlight1Info = []
        # DestFlight1Info = []
        # DepartFlight2Info = []
        # DestFlight2Info = []
        flightInfo = []
        if not self.responsedata['data']['flightList'] is None:
            if not self.responsedata['data']['flightList'][0] is None:
                totalPrice = {"totalPrice": self.responsedata['data']['flightList'][0]['price']['totalPrice']}
                flightInfo.append(totalPrice)
                FlightNo1 = {
                    "FlightNo1": self.responsedata['data']['flightList'][0]['flightOptions'][0]['flightItems'][0][
                        'flightNo']}
                FlightCabin1 = {
                    "FlightCabin1":
                        self.responsedata['data']['flightList'][0]['flightOptions'][0]['flightItems'][0][
                            'cabinType']}
                flightInfo.append(FlightNo1)
                flightInfo.append(FlightCabin1)
                if self.checkdepartflightistransit() == True:
                    FlightNo3 = {
                        "FlightNo3":
                            self.responsedata['data']['flightList'][0]['flightOptions'][0]['flightItems'][1][
                                'flightNo']}
                    FlightCabin3 = {"FlightCabin3":
                                        self.responsedata['data']['flightList'][0]['flightOptions'][0][
                                            'flightItems'][
                                            1][
                                            'cabinType']}

                    flightInfo.append(FlightNo3)
                    flightInfo.append(FlightCabin3)
                FlightNo2 = {
                    "FlightNo2": self.responsedata['data']['flightList'][0]['flightOptions'][1]['flightItems'][0][
                        'flightNo']}
                FlightCabin2 = {
                    "FlightCabin2":
                        self.responsedata['data']['flightList'][0]['flightOptions'][1]['flightItems'][0][
                            'cabinType']}
                flightInfo.append(FlightNo2)
                flightInfo.append(FlightCabin2)
                if self.checkdestflightistransit() == True:
                    FlightNo4 = {
                        "FlightNo4":
                            self.responsedata['data']['flightList'][0]['flightOptions'][1]['flightItems'][1][
                                'flightNo']}
                    FlightCabin4 = {"FlightCabin4":
                                        self.responsedata['data']['flightList'][0]['flightOptions'][10][
                                            'flightItems'][
                                            1][
                                            'cabinType']}

                    flightInfo.append(FlightNo4)
                    flightInfo.append(FlightCabin4)
        return flightInfo

    def getHotelInfo(self):
        hotelInfo = []
        if not self.responsedata['data']['hotelList'] is None:
            if not self.responsedata['data']['hotelList'][0] is None:
                HotelName = {
                    "HotelName": self.responsedata['data']['hotelList'][0]['chineseName']}
                CheckInDate = {
                    "checkInDate": self.responsedata['data']['hotelList'][0]['checkInDate']}
                CheckOutDate = {
                    "checkOutDate": self.responsedata['data']['hotelList'][0]['checkOutDate']}
                ratePlanName = {
                    "ratePlanName": self.responsedata['data']['hotelList'][0]['rooms'][0]['ratePlans'][0][
                        'ratePlanName']}
                totalPrice = {
                    "totalPrice": self.responsedata['data']['hotelList'][0]['rooms'][0]['ratePlans'][0][
                        'price']['totalPrice']}
                hotelInfo.append(HotelName)
                hotelInfo.append(CheckInDate)
                hotelInfo.append(CheckOutDate)
                hotelInfo.append(ratePlanName)
                hotelInfo.append(totalPrice)
                return hotelInfo

    ### 获取推荐接口的vendor信息,用于更换房型后保存酒店信息的接口（saveInternalHotel）入参
    def getRecomHotelVendorInfo(self):
        if not self.responsedata['data']['hotelList'] is None:
            if not self.responsedata['data']['hotelList'][0] is None:
                vendorId = self.responsedata['data']['hotelList'][0]['rooms'][0]['ratePlans'][0]['vendorId']
                vendorRatePlanId = self.responsedata['data']['hotelList'][0]['rooms'][0]['ratePlans'][0][
                    'vendorRatePlanId']
                return vendorId, vendorRatePlanId

    ### 获取推荐接口的酒店ID,用于酒店列表入参入参

    def getHotelId(self):
        if not self.responsedata['data']['hotelList'] is None:
            if not self.responsedata['data']['hotelList'][0] is None:
                return self.responsedata['data']['hotelList'][0]['hotelId']

    def getHoteluniqueFlag(self):
        if self.checkHotel() == True:
            return self.responsedata['data']['hotelList'][0]['uniqueFlag']

    def getFlightuniqueFlag(self):
        if self.checkflight() == True:
            return self.responsedata['data']['flightList'][0]['uniqueFlag']

    # 获取酒店可预定最大房间数
    def getHotelMaxNum(self):
        if self.checkHotel() == True:
            return self.responsedata['data']['hotelList'][0]['rooms'][0]['ratePlans'][0]['maxNum']

"""验仓验价"""
class FHPackage_CheckPriceAndPackage(InterfaceBase):
    # 定义接口变量地址
    config = "CheckPriceAndPackage"

    def __init__(self, cParam, session=None):
        # 获取本接口urlData
        urlData = FHPackageConf[self.config]
        super().__init__(urlData=urlData, cParam=cParam, session=session)

    def setReqParam(self, bookCityCode, bookCityName, departCityCode, departCityName, startCityCode, startCityName,
                    destCityCode,
                    destCityName, journeyDepartDate, journeyEndDate, sessionId,packType=1):
        self.dParam = {
            "packType":packType,
            "bookCityCode": bookCityCode,
            "bookCityName": bookCityName,
            "departCityCode": departCityCode,
            "departCityName": departCityName,
            "journeyList": [
                {"startCityCode": startCityCode, "startCityName": startCityName, "destCityCode": destCityCode,
                 "destCityName": destCityName, "journeyDepartDate": journeyDepartDate,
                 "journeyEndDate": journeyEndDate}],
            "sessionId": sessionId}

    ### 获取打包结果
    def getCheckResult(self):
        if not self.responsedata['data'] is None:
            return self.responsedata['data']['allSuccess']

    ### 获取打包成功的资源变化提示 和 打包失败提示
    def getCheckDesc(self):
        if self.getCheckResult() == True:
            if self.responsedata['data']['changeDesc']:
                return self.responsedata['data']['changeDesc']
        else:
             return self.responsedata['data']['failedDesc']


    def getProductId(self):
        """
        返回打包产品ID
        :return:
        """
        if not self.responsedata['data'] is None:
            if not self.responsedata['data']['productId'] is None:
                return self.responsedata['data']['productId']
        return False

"""下单第一步"""
class FHPackage_stepOne(InterfaceBase):
    # 定义接口变量地址
    config = "stepOne"

    def __init__(self, cParam):
        # 获取本接口URL
        urlData = FHPackageConf[self.config]
        super().__init__(urlData=urlData, cParam=cParam)

    def setReqParam(self, productId, beginDate, endDate, bookCityCode, departureCityCode, backCityCode, adultNum,
                    childNum,sessionId,packType =1):
        # departureCity 出发城市  backcity 目的地城市（接口定义如此）
        self.pData = {
            "productId": productId,
            "beginDate": beginDate,
            "endDate": endDate,
            "bookCityCode": bookCityCode,
            "departureCityCode": departureCityCode,
            "backCityCode": backCityCode,
            "adultNum": adultNum,
            "childNum": childNum,
            "packType":packType,
            "sessionId": sessionId
        }
    def getBookId(self):
        """
        返回bookId
        :return:
        """
        if not self.responsedata['data'] is None:
            if not self.responsedata['data'][1]['data']['bookId'] is None:
                return self.responsedata['data'][1]['data']['bookId']
        return None

"""获取保险信息"""
class FHPackage_getInsurance(InterfaceBase):
    # 定义接口变量地址
    config = "getInsurance"

    def __init__(self, cParam):
        # 获取本接口URL
        urlData = FHPackageConf[self.config]
        super().__init__(urlData=urlData, cParam=cParam)

    def setReqParam(self, productId, beginDate, endDate, bookCityCode, departureCityCode, backCityCode, adultNum,
                    childNum, sessionId,packType =1 ):
        self.pData = {
            "packType":packType,
            "productId": productId,
            "beginDate": beginDate,
            "endDate": endDate,
            "bookCityCode": bookCityCode,
            "departureCityCode": departureCityCode,
            "backCityCode": backCityCode,
            "adultNum": adultNum,
            "childNum": childNum,
            "sessionId": sessionId
        }

    def setReqParam2(self, beginDate, endDate, bookCityCode, departureCityCode, backCityCode, adultNum,
                     childNum, sessionId, **kwargs):
        self.setReqParam(beginDate=beginDate, endDate=endDate, bookCityCode=bookCityCode,
                         departureCityCode=departureCityCode, backCityCode=backCityCode, adultNum=adultNum,
                         childNum=childNum, sessionId=sessionId, productId=kwargs["productId"])

    def CheckResult(self):
        if not self.responsedata['data'] == '':
            return True
        else:
            return False

    def GetRandomInsurance(self):
        if self.CheckResult():
            i = random.randint(0, len(self.responsedata['data']['insurance']) - 1)
            InsuranceList = {"resId": self.responsedata['data']['insurance'][i]['resId'],
                             "resType": self.responsedata['data']['insurance'][i]['resType']}
            InsurancePrice = self.responsedata['data']['insurance'][i]['price']
            return InsuranceList,InsurancePrice

"""获取优惠信息"""
class FHPackage_getPromotion(InterfaceBase):
    # 定义接口变量地址
    config = "getPromotion"

    def __init__(self, cParam):
        # 获取本接口URL
        urlData = FHPackageConf[self.config]
        super().__init__(urlData=urlData, cParam=cParam)

    def setReqParam(self, productId, beginDate, endDate, bookCityCode, departureCityCode, backCityCode, adultNum,
                    childNum, sessionId,packType=1):
        # departureCity 出发城市  backcity 目的地城市（接口定义如此）
        self.pData = {
            "packType": packType,
            "productId": productId,
            "beginDate": beginDate,
            "endDate": endDate,
            "bookCityCode": bookCityCode,
            "departureCityCode": departureCityCode,
            "backCityCode": backCityCode,
            "adultNum": adultNum,
            "childNum": childNum,
            "sessionId": sessionId
        }
    def CheckResult(self):
        if not self.responsedata['data'] == '':
            return True
        else:
            return False

    def GetRandomPromotion(self):
        if self.CheckResult():
            i = random.randint(0, len(self.responsedata['data']['promotion']) - 1)
            PromotionList = {"promotionId": self.responsedata['data']['promotion'][i]['promotionId'],
                             "promotionType": self.responsedata['data']['promotion'][i]['promotionType']}
            PromotionPrice = self.responsedata['data']['promotion'][i]['promotionPrice']
            return PromotionList,PromotionPrice

"""下单第二步"""
class FHPackage_addOrder(InterfaceBase):
    # 定义接口变量地址
    config = "addOrder"

    def __init__(self, cParam):
        # 获取本接口URL
        urlData = FHPackageConf[self.config]
        super().__init__(urlData=urlData, cParam=cParam)

    def setticketTacker(self, number, resUniqueFlag, touristIds):
        ticketTaker = []
        i = 0
        while i < number:
            ticketTaker.append({
                "resUniqueFlag": resUniqueFlag,
                "touristId": touristIds[i]})
            i = i + 1
        return ticketTaker

    def setticketTourist(self, number, resUniqueFlag, touristIds):
        ticketTourist = []
        i = 0
        while i < number:
            ticketTourist.append({
                "resUniqueFlag": resUniqueFlag,
                "touristId": touristIds[i]})
            i = i + 1
        return ticketTourist

    def setReqParam(self, productId, beginDate, endDate, bookCityCode, departureCityCode, backCityCode, adultNum,
                    childNum, bookId, promotionList, insuranceList, travelCoupon, contactInfo, specialPeopleInfo,
                    touristInfo, blackCardCheckResult, noFillTourist, ticketTaker, ticketTourist,
                    sessionId, packType=1):
        # departureCity 出发城市  backcity 目的地城市（接口定义如此）
        self.pData = {
            "packType": packType,
            "productId": productId,
            "beginDate": beginDate,
            "endDate": endDate,
            "bookCityCode": bookCityCode,
            "departureCityCode": departureCityCode,
            "backCityCode": backCityCode,
            "adultNum": adultNum,
            "childNum": childNum,
            "bookId": bookId,
            "promotionList": promotionList,
            "insuranceList": insuranceList,
            "travelCoupon": travelCoupon,
            "contactInfo": contactInfo,
            "specialPeopleInfo": specialPeopleInfo,
            "touristInfo": touristInfo,
            "blackCardCheckResult": blackCardCheckResult,
            "noFillTourist": noFillTourist,
            "ticketTaker": ticketTaker,
            "ticketTourist": ticketTourist,
            "sessionId": sessionId
        }

    def setReqParam2(self, productId, beginDate, endDate, bookCityCode, departureCityCode, backCityCode, adultNum,
                     childNum, bookId, promotionList, insuranceList, travelCoupon, contactInfo, specialPeopleInfo,
                     touristInfo, blackCardCheckResult, noFillTourist, resUniqueFlag, touristId,
                     sessionId, packType=1):
        # departureCity 出发城市  backcity 目的地城市（接口定义如此）
        self.pData = {
            "packType": packType,
            "productId": productId,
            "beginDate": beginDate,
            "endDate": endDate,
            "bookCityCode": bookCityCode,
            "departureCityCode": departureCityCode,
            "backCityCode": backCityCode,
            "adultNum": adultNum,
            "childNum": childNum,
            "bookId": bookId,
            "promotionList": promotionList,
            "insuranceList": insuranceList,
            "travelCoupon": travelCoupon,
            "contactInfo": contactInfo,
            "specialPeopleInfo": specialPeopleInfo,
            "touristInfo": touristInfo,
            "blackCardCheckResult": blackCardCheckResult,
            "noFillTourist": noFillTourist,
            "ticketTaker": [{
                "resUniqueFlag": resUniqueFlag,
                "touristId": touristId}],
            "ticketTourist": [],
            "sessionId": sessionId
        }

    def getOrderResult(self):
        if not self.responsedata['data'] is None:
            return self.responsedata['data']['success']

    def getOrderInfo(self):
        return self.responsedata['data']


"""取消订单"""
class CancelOrder(InterfaceBase):
    # 定义接口变量地址
    config = "CancelOrder"

    def __init__(self):
        # 获取本接口URL
        urlData = FHPackageConf[self.config]
        super().__init__(urlData=urlData)

    def setReqParam(self, orderId):
        self.pData = {
            "uid": "26683",
            "token": '',
            "nickname": "李菊",
            "r": 0.7413435727922948,
            "cancelType0": "5",
            "cancelType1": "502",
            "cancelType2": "50201",
            "cancelReason": "111",
            "repeatOrder": "",
            "intentionTime": "",
            "intention": "",
            "canceledName": "",
            "canceledTime": "",
            "isFreewill": 1,
            "cancelType": "50201",
            "repeatFlag": 0,
            "cancelTypeDetail": "系统测试订单",
            "orderId": orderId
        }
