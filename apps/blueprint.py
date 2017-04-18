#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask import Blueprint
__author__ = 'Allen Woo'

'''
蓝本
'''
# 视图路由
view = Blueprint('view', __name__, template_folder="templates", static_url_path='/static', static_folder='static')

# api路由
api = Blueprint('api', __name__)

'''
将需要用到路由的文件都导入到下面,必须是下面
'''

from apps import views
from apps.user.apis import user


