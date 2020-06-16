import pandas as pd
from app.models.models import *
from app import  db


def jira_tuniu_merge_test():
    temp_data = []
    unmerged_list = []
    a = [{'python': '1', 'java': '333', 'c': 345, 'name': 'dff2'}, {'python': '2', 'java': '333', 'c': 345, 'name': 'dff'}]
    b = [{'name': 'dff2', 'e': 'adaaaa', 'c': 345, 'd': 22}]
    b = []
    b_init = { 'e': '', 'c': '', 'd': ''}

    for x in a:
        x_times=0
        for y in b:
            if x['name'] == y['name']:
                temp_data.append(dict(x, **y))
                x_times+=1
        if x_times == 0:
            unmerged_list.append(x)
    if len(unmerged_list) >0:
        for i in unmerged_list:
            temp_data.append(dict(i,**b_init))
    print('the not mergetd:\n', unmerged_list)
    print('the end temp_data is : \n', temp_data, '\n', len(temp_data))

def read_excel(file_name, sheet_name):
    worker_list = pd.read_excel(file_name, sheet_name=sheet_name)
    print(tuple(worker_list['姓名']))
    print(tuple(worker_list['ScrumTeam']))
    insert_data = tuple(list(zip(tuple(worker_list['姓名']),tuple(worker_list['ScrumTeam']))))
    # for worker in worker_list:
    #     print(worker, type(worker))
    return insert_data

def insert_database(data):
    insert_num = 0
    for item in data:
        worker = Worker_ScrumTeam(worker_name=item[0], scrum_team=item[1])
        db.session.add(worker)
        db.session.commit()
        insert_num += 1
    print('inset %d records success...'%insert_num)
    return insert_num


if __name__ == '__main__':

    data = read_excel('名单.xlsx','Sheet1')
    insert_database(data)