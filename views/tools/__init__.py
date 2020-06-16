# -*- coding: utf-8 -*-
from flask import Blueprint

tool = Blueprint('tool', __name__, url_prefix='/tool')
from views.tools import sessionCount
from views.tools import qrcode
