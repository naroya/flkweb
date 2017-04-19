#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask import jsonify, request
from apps import config
from apps.blueprint import api
from apps.init_app import mongo

__author__ = "Allen Woo"


@api.route('/user/role/permissions',  methods=['GET','POST'])
def permissions():
    return jsonify(config.Role.PERMISSIONS)

@api.route('/user/role/add',  methods=['POST'])
def add_role():

    '''
    只允许使用post方式请求
    :return:
    '''
    data = {"msg":None}
    # 获取前端post的数据
    name = request.values["name"]
    permissions = request.values["permissions"]
    if not name.strip():
        data = {"msg":"名字不能为空"}
    else:
        role = {"name":name, "permissions":permissions}
        # 如果数据库中存在这个name的角色则不做任何事,否则插入数据库
        r = mongo.db.role.update({"name":name}, {"$setOnInsert":role}, upsert=True)
        if r['updatedExisting']:
            data = {"msg":"角色已经存在"}
        else:
            data = {"msg":"添加角色成功"}
    return jsonify(data)

@api.route('/user/profile',  methods=['GET','POST'])
def index():
    '''
    只允许使用get和post方式请求
    :return:
    '''
    data = {"username":"Allen Woo",
            "sex":"M",
            "age":23,
            "public_no":"人人可以学Python"}

    return jsonify(data)