#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask import jsonify
from apps.blueprint import api
__author__ = "Allen Woo"

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