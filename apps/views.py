# -*-coding:utf-8-*-
import os
from flask import render_template
from flask_login import login_required
from werkzeug.exceptions import abort
from apps.blueprint import view

__author__ = "Allen Woo"

@view.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

# 所有以user开头的页面都会跑这里了
@view.route('/user/<path:path>', methods=['GET','POST'])
@login_required
def user_pages(path):
    path = "/user/{}".format(path)
    absolute_path = os.path.abspath("{}/{}/{}.html".format(os.path.dirname(__file__), view.template_folder,path))
    if not os.path.isfile(absolute_path):
        abort(404)
    return render_template('{}.html'.format(path))

# 通用视图函数
@view.route('/<path:path>', methods=['GET','POST'])
def pages(path):
    absolute_path = os.path.abspath("{}/{}/{}.html".format(os.path.dirname(__file__), view.template_folder,path))
    if not os.path.isfile(absolute_path):
        abort(404)
    return render_template('{}.html'.format(path))
