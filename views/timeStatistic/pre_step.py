# -*- coding: utf-8 -*-
# TIME:         6.27
# Author:       huangfang
# Explain：     从excel获取资本化数据入库---弃用

from app.models.models import *
from flask import Blueprint
from sqlalchemy import func, and_, desc
import json
import sys
from flask import current_app
import xlrd

def getprestep():
    # 从excel读取资本化数据信息入库
    # 文件位置
    ExcelFile = xlrd.open_workbook(r'/Users/tuniu/Desktop/timeworking/项目人力&概况看板-线上BU.xlsx')
    # 定位到指定的sheet读取数据
    sheet = ExcelFile.sheet_by_name('概述（填写）')
    # 获取表格中最新的周数
    week = sheet.cell(sheet.nrows - 1, 1).value
    print (week)
    # 获取表格中的资本化工时
    capitalizationTime = round(sheet.cell(sheet.nrows - 1, 11).value)
    # 获取表格中的项目工时
    projectTime = round(sheet.cell(sheet.nrows - 1, 7).value)
    # 获取表格中的技术支持工时round
    supportTime = round(sheet.cell(sheet.nrows - 1, 13).value)
    # 获取表格中的理论工时
    theoreticalTime = round(sheet.cell(sheet.nrows - 1, 5).value)

    # 将表格中的数据入库
    time = Time_working(week=week, capitalizationTime=capitalizationTime, projectTime=projectTime,
                        supportTime=supportTime,
                        theoreticalTime=theoreticalTime)

    db.session.merge(time)

    db.session.commit()

if __name__ == '__main__':

    # 从excel读取资本化数据信息入库
    # 文件位置
    ExcelFile = xlrd.open_workbook(r'/Users/tuniu/Desktop/timeworking/项目人力&概况看板-线上BU.xlsx')
    # 定位到指定的sheet读取数据
    sheet = ExcelFile.sheet_by_name('概述（填写）')
    # 获取表格中最新的周数
    week = sheet.cell(sheet.nrows - 1, 1).value
    # 获取表格中的资本化工时
    capitalizationTime = round(sheet.cell(sheet.nrows - 1, 11).value)
    # 获取表格中的项目工时
    projectTime = round(sheet.cell(sheet.nrows - 1, 7).value)
    # 获取表格中的技术支持工时round
    supportTime = round(sheet.cell(sheet.nrows - 1, 13).value)
    # 获取表格中的理论工时
    theoreticalTime = round(sheet.cell(sheet.nrows - 1, 5).value)

    # 将表格中的数据入库
    time = Time_working(week=week, capitalizationTime=capitalizationTime, projectTime=projectTime,
                        supportTime=supportTime,
                        theoreticalTime=theoreticalTime)

    db.session.merge(time)

    db.session.commit()


