class Common_params():
    version = "10.19.0"
    env = "pre"
    def __init__(self):
        pass

interface_conf = {
    'portal_app_channel_index': {
        'domain': {'pre':'api-p.tuniu.com', 'prd':'api.tuniu.com'},
        'method': 'get',
        'path': '/portal/app/channel/index',
        'comments': '频道页主信息获取接口'
    },
    'portal_app_channel_index_旅游': {
        'domain': {'pre':'api-p.tuniu.com', 'prd':'api.tuniu.com'},
        'method': 'get',
        'path': '/portal/app/channel/index',
        'comments': '频道页主信息获取接口'
    },
    'portal_app_channel_index_跟团': {
        'domain': {'pre':'api-p.tuniu.com', 'prd':'api.tuniu.com'},
        'method': 'get',
        'path': '/portal/app/channel/index',
        'comments': '频道页主信息获取接口'
    },
    'portal_app_channel_index_出境游': {
        'domain': {'pre':'api-p.tuniu.com', 'prd':'api.tuniu.com'},
        'method': 'get',
        'path': '/portal/app/channel/index',
        'comments': '频道页主信息获取接口'
    },
    'guessLike': {
        'domain': {'pre':'api-p.tuniu.com', 'prd':'api.tuniu.com'},
        'method': 'get',
        'path': '/portal/home/guessLike',
        'comments': '首页猜你喜欢接口'
    },
    'portal_home_data_index': {
        'domain': {'pre':'api-p.tuniu.com', 'prd':'api.tuniu.com'},
        'method': 'get',
        'path': '/portal/home/data/index',
        'comments': '首页宫格数据'
    },
    'portal_home_list_v3': {
        'domain': {'pre':'api-p.tuniu.com', 'prd':'api.tuniu.com'},
        'method': 'get',
        'path': '/portal/home/list/v3',
        'comments': '首页瀑布流（境内）'
    },
    'portal_home_list_abroad_v2': {
        'domain': {'pre':'api-p.tuniu.com', 'prd':'api.tuniu.com'},
        'method': 'get',
        'path': '/portal/home/list/abroad/v2',
        'comments': '首页瀑布流（境外）'
    }
}