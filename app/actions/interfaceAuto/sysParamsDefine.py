# coding = utf-8
# Time: 2019-11-27
# Author: dongff

import datetime
class SysParams():

    def curr_date(self,addOrsubtract='',unit='',num=0):
        if num not in('',None):
            num = int(num)
        else:
            num = 0
        curr_date = datetime.datetime.now()
        if unit == 'M':
            dynamic = datetime.timedelta(days=(num*30))
        elif unit == 'd':
            dynamic = datetime.timedelta(days=num)
        elif unit == 't':
            dynamic = datetime.timedelta(hours=num)
        elif unit == 'm':
            dynamic = datetime.timedelta(minutes=num)
        elif unit == 's':
            dynamic = datetime.timedelta(seconds=num)
        else:
            dynamic = datetime.timedelta(days=0)

        if addOrsubtract == 'add':
            curr_date = (curr_date + dynamic).strftime("%Y-%m-%d")
        elif addOrsubtract == 'subtract':
            curr_date = (curr_date - dynamic).strftime("%Y-%m-%d")
        else:
            curr_date = curr_date.strftime("%Y-%m-%d")
        return curr_date

    def curr_time(self,addOrsubtract='',unit='',num=0):
        if num not in('',None):
            num = int(num)
        else:
            num = 0
        curr_time = datetime.datetime.now()
        if unit == 'M':
            dynamic = datetime.timedelta(days=(num*30))
        elif unit == 'd':
            dynamic = datetime.timedelta(days=num)
        elif unit == 't':
            dynamic = datetime.timedelta(hours=num)
        elif unit == 'm':
            dynamic = datetime.timedelta(minutes=num)
        elif unit == 's':
            dynamic = datetime.timedelta(seconds=num)
        else:
            dynamic = datetime.timedelta(days=0)

        if addOrsubtract == 'add':
            curr_time = (curr_time + dynamic).strftime("%Y-%m-%d %H:%M:%S")
        elif addOrsubtract == 'subtract':
            curr_time = (curr_time - dynamic).strftime("%Y-%m-%d %H:%M:%S")
        else:
            curr_time = curr_time.strftime("%Y-%m-%d %H:%M:%S")
        return curr_time

    def curr_month(self,addOrsubtract='',unit='',num=0):
        if num not in('',None):
            num = int(num)
        else:
            num = 0
        curr_month = datetime.datetime.now()
        if unit == 'M':
            dynamic = datetime.timedelta(days=(num*30))
        elif unit == 'd':
            dynamic = datetime.timedelta(days=num)
        elif unit == 't':
            dynamic = datetime.timedelta(hours=num)
        elif unit == 'm':
            dynamic = datetime.timedelta(minutes=num)
        elif unit == 's':
            dynamic = datetime.timedelta(seconds=num)
        else:
            dynamic = datetime.timedelta(days=0)

        if addOrsubtract == 'add':
            curr_month = (curr_month + dynamic).strftime("%Y-%m")
        elif addOrsubtract == 'subtract':
            curr_month = (curr_month - dynamic).strftime("%Y-%m")
        else:
            curr_month = curr_month.strftime("%Y-%m")
        return curr_month




if __name__ == '__main__':
    d1 = SysParams()
    print(d1.curr_date('subtract','m',2), type(d1.curr_date('subtract','m',2)))
    print(d1.curr_time('subtract','s',2), type(d1.curr_time('subtract','s',2)))
    print(d1.curr_month('subtract','M',2),type(d1.curr_month('subtract','M',2)))
