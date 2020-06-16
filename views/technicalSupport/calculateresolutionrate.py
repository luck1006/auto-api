from app.models.models import *
from sqlalchemy import and_


#根据数据库值，计算解决率并更新数据库
def CalculaterResolutionRate():
    ll=['order','supplychain','confirm','ticket','member','market','other','all']
    s=2
    if s==1:
        for i in ll:
            result = db.session.query(Technical_Support.name, Technical_Support.week,Technical_Support.newnum,Technical_Support.hisunsolvednum).filter(Technical_Support.name==i).filter(Technical_Support.del_flag == 0).order_by(Technical_Support.week).all()
            print(result)
            datalist=[]
            for n in range(len(result)-1):
                if((result[n][3]+result[n+1][2])!=0):
                    rate = '%.4f'%((result[n][3]+result[n+1][2]-result[n+1][3])/(result[n][3]+result[n+1][2]))
                    print(rate)
                    Technical_Support.query.filter(and_(Technical_Support.name==i,Technical_Support.week==result[n+1][1],Technical_Support.del_flag == 0)).update({'resolutionrate':rate})
            db.session.commit()
            db.session.close()
        return result
    elif s==2:
        for i in ll:
            result = db.session.query(Technical_MonthSupport.name, Technical_MonthSupport.month,Technical_MonthSupport.newnum,Technical_MonthSupport.hisunsolvednum).filter(Technical_MonthSupport.name==i).filter(Technical_MonthSupport.del_flag == 0).order_by(Technical_MonthSupport.month).all()
            print(result)
            datalist=[]
            for n in range(len(result)-1):
                if((result[n][3]+result[n+1][2])!=0):
                    rate = '%.4f'%((result[n][3]+result[n+1][2]-result[n+1][3])/(result[n][3]+result[n+1][2]))
                    print(rate)
                    Technical_MonthSupport.query.filter(and_(Technical_MonthSupport.name==i,Technical_MonthSupport.month==result[n+1][1],Technical_MonthSupport.del_flag == 0)).update({'resolutionrate':rate})
            db.session.commit()
            db.session.close()
        return result
    elif s==3:
        for i in ll:
            result = db.session.query(Technical_QuarterSupport.name, Technical_QuarterSupport.quarter,Technical_QuarterSupport.newnum,Technical_QuarterSupport.hisunsolvednum).filter(Technical_QuarterSupport.name==i).filter(Technical_QuarterSupport.del_flag == 0).order_by(Technical_QuarterSupport.quarter).all()
            print(result)
            datalist=[]
            for n in range(len(result)-1):
                if((result[n][3]+result[n+1][2])!=0):
                    rate = '%.4f'%((result[n][3]+result[n+1][2]-result[n+1][3])/(result[n][3]+result[n+1][2]))
                    print(rate)
                    Technical_QuarterSupport.query.filter(and_(Technical_QuarterSupport.name==i,Technical_QuarterSupport.quarter==result[n+1][1],Technical_QuarterSupport.del_flag == 0)).update({'resolutionrate':rate})
            db.session.commit()
            db.session.close()
        return result
    else:
        return "false"



def test(week):
    print(week-1)
    g = {"order":'(Boss3订单系统, 分单系统)',"supplychain":'(产品系统, 资源系统, 库存系统, 采购系统, 投诉质检, NB系统, 出团通知, BOH)',"ticket":'(门票系统)',"member":'(crm系统, 会员系统)',"market":'(营销)',"confirm":'(确认管理)',"other":'(其他)'}
    for k,v in g.items():
        result = db.session.query(Technical_Support.hisunsolvednum).filter(Technical_Support.week==(str(week-1)+'W')).filter(Technical_Support.name==k).filter(Technical_Support.del_flag==0)[0][0]
        return result

#计算24W、1M、Q1的解决率
def jisuan():
    result = db.session.query(Technical_QuarterSupport.newnum,Technical_QuarterSupport.hisunsolvednum).filter(Technical_QuarterSupport.name == 'all').filter(Technical_QuarterSupport.del_flag == 0).filter(Technical_QuarterSupport.quarter=='Q1').all()
    lasthis=239
    b='%.4f'%((lasthis+result[0][0]-result[0][1])/(lasthis+result[0][0]))
    Technical_QuarterSupport.query.filter(and_(Technical_QuarterSupport.name == 'all', Technical_QuarterSupport.quarter == 'Q1',Technical_QuarterSupport.del_flag == 0)).update({'resolutionrate': b})
    db.session.commit()
    db.session.close()
    return b


#插入数据
def insertdata(insert_data):
    s=2
    if s==1:
        db.session.execute(Technical_Support.__table__.insert(), insert_data)
        db.session.commit()
    elif s==2:
        db.session.execute(Technical_MonthSupport.__table__.insert(), insert_data)
        db.session.commit()
    elif s==3:
        db.session.execute(Technical_QuarterSupport.__table__.insert(), insert_data)
        db.session.commit()
    else:
        return "false"




#计算历史数据



if __name__ == '__main__':
    #week = int(datetime.datetime.now().strftime('%U')) + 1
    #print(test(week))
    #print(jisuan())
    data=[{'month':'9M','name':'order','newnum':797,'closenum':785,'unsolvednum':2,'hisunsolvednum':5},
          {'month': '9M', 'name': 'supplychain', 'newnum': 367, 'closenum': 368, 'unsolvednum': 10, 'hisunsolvednum': 10},
          {'month': '9M', 'name': 'ticket', 'newnum': 71, 'closenum': 69, 'unsolvednum': 3, 'hisunsolvednum': 7},
          {'month': '9M', 'name': 'member', 'newnum': 155, 'closenum': 145, 'unsolvednum': 9, 'hisunsolvednum': 10},
          {'month': '9M', 'name': 'market', 'newnum': 57, 'closenum': 53, 'unsolvednum': 1, 'hisunsolvednum': 1},
          {'month': '9M', 'name': 'confirm', 'newnum': 440, 'closenum': 445, 'unsolvednum': 1, 'hisunsolvednum': 2},
          {'month': '9M', 'name': 'all', 'newnum': 1887, 'closenum': 1865, 'unsolvednum': 26, 'hisunsolvednum': 35}]
    #insertdata(data)
    CalculaterResolutionRate()





