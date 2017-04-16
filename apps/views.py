#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask import render_template
from apps.blueprint import view
__author__ = "Allen Woo"

@view.route('/')
def index():
    return "Flask02-人人可以学python"

# 其他html路由
@view.route('/<path:path>')
def pages1(path):
    path = path.strip("/")
    return render_template('{}.html'.format(path))

