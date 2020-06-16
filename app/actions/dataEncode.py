import json
import datetime


class DateEncoder(json.JSONEncoder):
    '''
    moudles中字段格式转换
    '''

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, Decimal):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)
