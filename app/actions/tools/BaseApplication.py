#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import base64
import json
import sys
import os
sys.path.append( '..'+ os.sep ) ## “ '..'+ os.sep ” => 向上一层
from app.actions.tools.InterfaceKeyword import InterfaceKeyword



def interface(arg):
    return arg(InterfaceKeyword())



def base(arg):
    return arg(BaseApplication())







def plan(pathList,flag=None):
    def run(func):
        baseA = BaseApplication()
        list = []
        baseA.runDir(pathList, list)
        if(flag==None or flag==1):
            baseA.logExcel(list, sys.argv[0])
        return func(list)
    return run

#class BaseApplication(CommonKeyword,DatabaseKeyword,InterfaceKeyword,UIKeyword):
class BaseApplication(InterfaceKeyword):
	pass
