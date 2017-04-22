#!/usr/bin/env python
# -*-coding:utf-8-*-
__author__ = "Allen Woo"

class MongoDB():
    '''
    mongodb数据库基本配置,更多的配置需要时再陪
    '''
    MONGO_HOST = "127.0.0.1"
    MONGO_PORT = 27017 #MONGO默认端口
    MONGO_DBNAME = "flkweb"
    MONGO_USERNAME = "test"
    MONGO_PASSWORD = "123456"

class Secret():
    SECRET_KEY = "sebrdntnrsthryhrthetyjetyj"