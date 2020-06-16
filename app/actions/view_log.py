# -*- coding: utf-8 -*-

def viewlog():
    # with open('/Users/sunchuanxin/PycharmProjects/autoapi/views/tardis/mob_hercules.log') as f:
    with open("/opt/tuniu/www/Pandora/log/gunicorn_error.log") as f:
        #     for i  in
        return f.readlines()


def view_db():
    with open("/opt/tuniu/www/Pandora/db.config") as f:
        return f.readlines()
