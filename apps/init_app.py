#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask import Flask
from flask_pymongo import PyMongo
from apps.db_config import MongoDB

__author__ = "Allen Woo"

# 创建flask实例对象
app = Flask(__name__)
# 创建对象
mongo = PyMongo()

# app加载配置
app.config.from_object(MongoDB)

# 初始化mongo我们数据库库配置变量的前缀都是MONGO
mongo.init_app(app, config_prefix='MONGO')

# 注册蓝本
from apps.blueprint import api, view
app.register_blueprint(view, url_prefix="")
app.register_blueprint(api, url_prefix="/api")




