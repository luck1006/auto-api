# /usr/bin/python
# -*- coding:utf-8 -*-
"""
# project:autoapi
# user:: liju
@author: liju
@time: 2019-10-8 15:09
"""

# 机酒打包相关接口
FHPackageConf = { "Auth_BeginSession": {
        "protocol": "http",
        "domain": {"prd": "api.tuniu.com", "pre": "api-p.tuniu.com", "sit": "api-sit.tuniu.org"},
        "path": "auth/beginSession",
        "method": "post",
        "comments": "获取session"
    },
    "Auth_Login": {
        "protocol": "http",
        "domain": {"prd": "m.tuniu.com", "pre": "m-p.tuniu.com", "sit": "m-sit.tuniu.com"},
        "path": "api/user/auth/login",
        "method": "get",
        "comments": "使用帐号和session登录"
    },
    "getDefaultRecommend": {
        "protocol": "http",
        "domain": {"prd": "api.tuniu.com", "pre": "api-p.tuniu.com", "sit": "api-sit.tuniu.org"},
        "path": "res/pack/getDefaultRecommend/app",
        "method": "get",
        "comments": "推荐机票+酒店"
    },

    "SaveInternalFlight": {
        "protocol": "http",
        "domain": {"prd": "api.tuniu.com", "pre": "api-p.tuniu.com", "sit": "api-sit.tuniu.org"},
        "path": "res/pack/saveInternalFlight/app",
        "method": "post",
        "comments": "保存国内机票"
    },

    "SaveInternalHotel": {
        "protocol": "http",
        "domain": {"prd": "api.tuniu.com", "pre": "api-p.tuniu.com", "sit": "api-sit.tuniu.org"},
        "path": "res/pack/saveInternalHotel/app",
        "method": "post",
        "comments": "保存国内酒店"
    },
    "getChangedResources": {
        "protocol": "http",
        "domain": {"prd": "api.tuniu.com", "pre": "api-p.tuniu.com", "sit": "api-sit.tuniu.org"},
        "path": "res/pack/getChangedResouces/app",
        "method": "get",
        "comments": "从大缓存获取保存内容"
    },
    "CheckPriceAndPackage": {
        "protocol": "http",
        "domain": {"prd": "api.tuniu.com", "pre": "api-p.tuniu.com", "sit": "api-sit.tuniu.org"},
        "path": "res/pack/checkPriceAndPackage/app",
        "method": "get",
        "comments": "验仓验价+打包"
    },
    "getHistoryJourney": {
        "protocol": "http",
        "domain": {"prd": "api.tuniu.com", "pre": "api-p.tuniu.com", "sit": "api-sit.tuniu.org"},
        "path": "res/pack/getHistoryJourney/app",
        "method": "get",
        "comments": "查询历史行程"
    },
    "deleteHistoryJourney": {
        "protocol": "http",
        "domain": {"prd": "api.tuniu.com", "pre": "api-p.tuniu.com", "sit": "api-sit.tuniu.org"},
        "path": "res/pack/deleteHistoryJourney/app",
        "method": "get",
        "comments": "删除历史行程"
    },
    "changeHotelRoomNum": {
        "protocol": "http",
        "domain": {"prd": "api.tuniu.com", "pre": "api-p.tuniu.com", "sit": "api-sit.tuniu.org"},
        "path": "res/pack/changeResourceNumber/app",
        "method": "get",
        "comments": "更改房间数"
    },
    "getInsurance": {
        "protocol": "http",
        "domain": {"prd": "m.tuniu.com", "pre": "m-p.tuniu.com", "sit": "m-sit.tuniu.org"},
        "path": "api/book/pack/getInsurance",
        "method": "post",
        "comments": "查询保险信息"
    },
    "getPromotion": {
        "protocol": "http",
        "domain": {"prd": "m.tuniu.com", "pre": "m-p.tuniu.com", "sit": "m-sit.tuniu.org"},
        "path": "api/book/pack/getPromotion",
        "method": "post",
        "comments": "查询优惠信息"
    },
    "stepOne": {
        "protocol": "http",
        "domain": {"prd": "m.tuniu.com", "pre": "m-p.tuniu.com", "sit": "m-sit.tuniu.org"},
        "path": "api/book/pack/stepOne",
        "method": "post",
        "comments": "下单stepOne"
    },
    "addOrder": {
        "protocol": "http",
        "domain": {"prd": "m.tuniu.com", "pre": "m-p.tuniu.com", "sit": "m-sit.tuniu.org"},
        "path": "api/book/pack/addOrder",
        "method": "post",
        "comments": "下单"
    },
    "hotellist": {
        "protocol": "http",
        "domain": {"prd": "api.tuniu.com", "pre": "api-p.tuniu.com", "sit": "api-sit.tuniu.org"},
        "path": "hotel/hotel/package/list",
        "method": "post",
        "comments": "酒店列表"
    },
    "hotelrateplan": {
        "protocol": "http",
        "domain": {"prd": "api.tuniu.com", "pre": "api-p.tuniu.com", "sit": "api-sit.tuniu.org"},
        "path": "hotel/hotel/package/rateplan",
        "method": "post",
        "comments": "酒店价格计划列表"
    },
    "CancelOrder": {
        "protocol": "http",
        "domain": {"prd": "public-api.tof.tuniu.org", "pre": "public-api.tof.tuniu.org", "sit": "public-api.nws.tuniu-sit.org"},
        "path": "tof/manage/order/cancel",
        "method": "post",
        "comments": "取消订单"
    }
}
