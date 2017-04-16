#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask import Flask

__author__ = "Allen Woo"

# 创建flask实例对象
app = Flask(__name__)

# 注册蓝本
from apps.blueprint import api, view
app.register_blueprint(view, url_prefix="/")
app.register_blueprint(api, url_prefix="/api")


