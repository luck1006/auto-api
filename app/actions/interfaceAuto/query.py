# -*- coding: utf-8 -*-
# TIME:         下午3:17
# Author:       xutaolin
from app.models.models import *
from sqlalchemy import and_, or_, desc
from app import db
from sqlalchemy import func


# 查询节点下的所有父节点
def query(idlist, r_list):
    for id in idlist:
        pids = db.session.query(Tree_Task.tree_id).filter(
            and_(Tree_Task.parent_id == id, Tree_Task.tree_type == 1)).all()
        pid_list = [(row.tree_id) for row in pids]
        if (pid_list):
            query(pid_list, r_list)
            r_list.append(pid_list)
    return r_list

#查出某个子节点的所有父节点
def queryallpid(id):
     count=1
     pid=[]
     while count==1:
         ids=db.session.query(Tree_Task.parent_id).filter(Tree_Task.tree_id==id).first()
         id=ids[0]
         pid.append(ids[0])
         # count = Tree_Task.query.filter_by(tree_id=id).count()
         count = db.session.query(func.count(Tree_Task.tree_id)).filter(Tree_Task.tree_id==id).scalar()
     return pid

#层级表刷数据
def demo():
    #查询出所有的用例id
    ids = db.session.query(Tree_Task.tree_id).filter(Tree_Task.tree_type == 0).all()
    for i in range(len(ids)):
        pids=queryallpid(ids[i][0])
        add_case_level = Case_Level(case_id=ids[i][0],
                                       levels=str(pids))
        db.session.add(add_case_level)
        db.session.commit()
    return


# 多层嵌套list递归拆分
def newlist(oldlist):
    """
      功能:用递归方法展开多层列表,以生成器方式输出
    """
    if isinstance(oldlist, list):
        for li in oldlist:
            for el in newlist(li):
                yield el
    else:
        yield oldlist

    return oldlist

#父节点和旗下某些子节点组装成的dict
def querychilddict(parent_id,scope_id,count_id):
    # print('count='+ str(count_id))
    # out_json={'type':'suite','id':parent_id,'name':parent_name,'child':[],'runtime':None,'result':None,'inparams':'','outparams':'','checkout':''}
    # max_count_query=Report.query.filter_by().order_by(Report.count.desc()).first()
    out_json=[]

    out_info = db.session.query(Tree_Task.tree_id, Tree_Task.tree_type, Tree_Task.tree_name).filter(
        Tree_Task.parent_id == parent_id).order_by(Tree_Task.tree_order).all()

    for id in ([(row.tree_id, int(row.tree_type), row.tree_name) for row in out_info]):
        if (id[0] in scope_id):
            # tree_type 为目录
            if (id[1] == 1):
                # count = db.session.query(Tree_Task.tree_id).filter(Tree_Task.parent_id == id[0] and Tree_Task.tree_type==0).count()
                count = db.session.query(func.count(Tree_Task.tree_id)).filter(Tree_Task.parent_id == id[0] and Tree_Task.tree_type==0).scalar()
                inter_info=querychilddict(id[0],scope_id,count_id)
                p_info = Tree_Task.query.filter_by(tree_id=id[0]).first()
                report_child = {'type': 'suite', 'id': p_info.tree_id, "num":None,'name': p_info.tree_name, 'child': [],
                                'runtime': None, 'rest':'','result': None}
                if (count != 0):
                    for i in inter_info:
                        report_child['child'].append(i)
                    out_json.append(report_child)   # 20190708 dff；由于下面统一处理的out_json.append(report_child)被屏蔽了，故此处放到if, elif里分别处理

            # tree_type 为用例
            elif (id[1] == 0):
                # p_info = Report.query.filter(and_(Report.case_id==id[0],Report.count==max_count_query.count)).first()
                #20190708 - dff: 修改为查询该用例及运行count批次下所有的执行记录（参数化后一个用例可能被执行了多次）
                # p_info = Report.query.filter(and_(Report.case_id==id[0],Report.count==count_id)).all()
                p_info = db.session.query(Report.result,Report.runtime,Report.rest,Report.id).filter(and_(Report.case_id==id[0],Report.count==count_id)).all()
                case_run_count = db.session.query(func.count(Tree_Task.tree_id)).filter(and_(Report.case_id==id[0],Report.count==count_id)).scalar()
                if case_run_count > 1:
                    case_count = 1 # 用来记录用例执行次数
                    for p_info_item in p_info:

                        if (p_info_item[0] == 1):
                            result = 'success'
                        elif (p_info_item[0] == 0):
                            result = 'fail'
                        report_child = {'type': 'test', 'id': id[0],'name': id[2]+'_'+str(case_count), 'child': [],
                                        'runtime': p_info_item[1],"num":p_info_item[3],
                                        'result': result, 'rest':p_info_item[2]}
                        out_json.append(report_child)
                        case_count+=1  #20190708 dff；用例执行次数计数器
                else:
                    if (p_info[0].result == 1):
                        result = 'success'
                    elif (p_info[0].result == 0):
                        result = 'fail'
                    report_child = {'type': 'test', 'id': id[0],'name': id[2],"num":p_info_item[3], 'child': [],
                                        'runtime': p_info[0].runtime,
                                        'result': result, 'rest':p_info[0].rest,'inparams': p_info[0].inparams, 'outparams': p_info[0].outparams,
                                        'checkout': p_info[0].checkout}
                    out_json.append(report_child)
            # 20190708-dff  为了能把同一用例多次执行记录都获取到，下面原代码屏蔽，采用上述的for 循环来处理
            #     if (p_info.result == 1):
            #         result = 'success'
            #     elif (p_info.result == 0):
            #         result = 'fail'
            #     report_child = {'type': 'test', 'id': id[0],'name': id[2], 'child': [],
            #                     'runtime': p_info.runtime,
            #                     'result': result, 'rest':p_info.rest,'inparams': p_info.inparams, 'outparams': p_info.outparams,
            #                     'checkout': p_info.checkout}
            # out_json.append(report_child)
    return out_json


if __name__ == '__main__':
    # a=querychilddict(2,[0,1,2,8,11])
    # print(json.dumps(a),'\n',len(a))
    demo()
    # pids = db.session.query(Tree_Task.tree_id, Tree_Task.tree_order).filter(
    #     and_(Tree_Task.parent_id == 204, Tree_Task.tree_type == 1)).all()
    # pid_list = [(row.tree_id) for row in pids]
    #
    # p = query(pid_list, [])
    #
    # print(p + pid_list)
    # print(list(newlist(p + pid_list)))
    # print(queryallpid(211))
