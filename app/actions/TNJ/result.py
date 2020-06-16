# encode=utf-8
from app.actions.TNJ.jira_sql import query_by_project
from app.actions.TNJ.jira_sql import query_epicby_month
from app.actions.TNJ.jira_conf import execute
import pandas as pd
from app.actions.TNJ.team import wiki_team
import json, time


class JIRA_EPIC():
    def __init__(self):
        data = execute(query_by_project)
        # print(json.dumps(data))
        value = {'epic': '无', 'timeworked': 0}
        self.df = pd.DataFrame().from_records(data=data).fillna(value=value)

        return

    def by_epic_oa(self):
        res = self.df.groupby(['epic', 'dept_sec'])['timeworked'].sum().reset_index()
        # self.df['epic'] = self.df['epic'].sort_values()
        df = res.reset_index().pivot('epic', 'dept_sec', 'timeworked').fillna(value='').reset_index()
        # print(json.dumps(df.to_dict(orient='split')))
        return df

    def epic_by_sprint_team(self):
        # 读wiki要4s 所以先写死吧
        # ttt=time.time()
        # d = wiki_team()
        # print('2131321312',time.time()-ttt)
        d = {'第38集团军': ['王墁鑫', '李曼媚', '王晶14', '张首伟', '吉星星', '孙雪雪', '史翌志', '周云萍', '王林林3', '刘金明2', '王亚明', '童静2', '史维强',
                        '王静21'],
             '金鳌队': ['徐萍3', '刘文彬', '张松2', '叶超', '范学民', '钱宏伟', '陈超9', '季赛楠', '钱宏伟', '乔旭', '姜扬2', '金晨3', '黄晓雪2'],
             '奚鼠': ['王晶14', '王路静', '李楠7', '赵东', '卢俊华', '张雯3'],
             '青龙': ['李梦阳', '杨开薪', '华金良', '郭喜芝', '李秋婷2', '赵君8', '朱家标', '刘桃桃', '崔淑华', '马姣姣'],
             '山猫': ['郭君龙', '郭君龙', '陈建炜2', '梅存兵', '马晶5', '张小魏', '孙海亮', '席雨伟', '杨洁8', '李昌盛2', '刘晶祖'],
             '玄武': ['李海红', '唐玥2', '邢恩禄', '袁浩茹', '赵茜5', '薛明星', '李风明', '王明波', '赵阳3', '张瑞文', '赵修玲', '郭倩3', '王慧勇', '董芳芳'],
             '麒麟': ['李海红', '唐玥2', '邢恩禄', '袁浩茹', '李勇6', '褚福玺', '汤靖咚', '汪军11', '李青3', '邹传华', '徐桃林'],
             '朱雀': ['李曼媚', '王墁鑫', '张扬15', '朱彬3', '刘翠翠', '陈瑜婷', '李兵2', '高萍萍', '孙传鑫'],
             '貔貅': ['张松2', '郝若颖', '王玲玲4', '李行', '戚挺', '郑金梅', '葛文婧', '徐志成3', '朱小兵'],
             '金蟾': ['张松2', '赵凌岳', '杨丽3', '李飞2', '卞云康', '刘成4', '祝全振', '赵贺', '匡亚明'],
             '长林军': ['孟珅宇', '杨丽3', '谢肖肖', '程文晶', '龚剑锋', '佘呈呈', '李冒妍2', '吴蛟4', '季帮', '杨丹丹'],
             '火箭军': ['陈进4', '李弘5', '杨涛', '李珍5', '文辉2', '王晴晴3', '李传仁', '杨恒跃', '周伟10', '许健6'],
             '锦鲤队': ['刘闯', '朱菊', '孟珅宇', '彭勃然', '张冬3', '林峰', '孙全民', '戴强', '王竹', '张涛12', '吴满军', '鲍业如', '徐佩颖'],
             '白虎': ['徐鹏', '丁超6', '杨培军2', '何洪臣', '虞娟娟']}
        nums = []
        for k, v in d.items():
            for i in v:
                nums.append([i, k])
        df_sprint_team = pd.DataFrame(data=nums, columns=['name_cn', 'st'])
        return df_sprint_team


def detail_to_excel():
    data = execute(query_by_project)
    print(data)
    
    col = []
    for i in data:
        for k, v in i.items():
            col.append(k)

        print(col)
        break

    df = pd.DataFrame(data=data, columns=col)

    filepath = 'temp.xlsx'
    excelWriter = pd.ExcelWriter(filepath, engine='openpyxl')
    df.to_excel(excelWriter)
    excelWriter.save()

    return


def result():
    d = JIRA_EPIC()
    df_by_oa = d.by_epic_oa()
    dict_by_oa = df_by_oa.to_dict(orient='records')
    st = d.epic_by_sprint_team()
    temp = pd.merge(d.df, st, on='name_cn')
    res = temp.groupby(['epic', 'st'])['timeworked'].sum().reset_index()
    df_by_st = res.reset_index().pivot('epic', 'st', 'timeworked').fillna(value='').reset_index()
    dic_by_st = df_by_st.to_dict(orient='records')
    # {'dict', 'list', 'series', 'split', 'records', 'index'}
    data = {
        'dict_by_oa': dict_by_oa,
        'dic_by_st': dic_by_st
    }
    return data


def test():
    df = pd.DataFrame(
        [(2011, 'a', 1.3), (2012, 'a', 1.4), (2013, 'a', 1.6), (2011, 'b', 0.7), (2012, 'b', 0.9),
         (2013, 'b', 1.2), ],
        columns=['year', 'district', 'price'])
    # df.set_index(['year'], inplace=True)
    df.head(n=10)
    df = df.reset_index().pivot('year', 'district', 'price')
    return df


def detail():

    '''工时明细'''
    data = execute(query_by_project)
    return data

#epic月投入
def byepic_month():
    month=0
    list=[]
    listdata={}
    data = execute(query_epicby_month)
    # data=json.dumps(info)
    # print(json.dumps(data))
    for  item  in  data:
        if item['month']!=month:
            listdata={'month': item['month']}
            listdata.update({item['epic']:item['timeworded']})
            list.append(listdata)
        else:
            listdata.update({item['epic']:item['timeworded']})
        month=item['month']
    return list