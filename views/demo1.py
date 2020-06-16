# -*- coding: utf-8 -*-
# TIME:         下午10:34
# Author:       xutaolin


from flask_restful import Resource


class TodoList(Resource):
    def get(self):
        return "get-hi flask!!"
    def post(self):
        return "post-hi flask!!"

