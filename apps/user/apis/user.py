#!/usr/bin/env python
# -*-coding:utf-8-*-
import re
from flask import jsonify, request
import time
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect
from apps import config
from apps.blueprint import api
from apps.init_app import mongo
from flask_login import current_user, login_user, logout_user, login_required
from apps.user.process.permissions import permission_required
from apps.user.process.user import User

__author__ = "Allen Woo"


@api.route('/user/role/permissions',  methods=['GET','POST'])
def permissions():
    return jsonify(config.Role.PERMISSIONS)


@api.route('/user/role/add',  methods=['POST'])
@permission_required(config.Role.ADMIN)
def add_role():

    '''
    只允许使用post方式请求
    :return:
    '''
    data = {"msg":None}
    # 获取前端post的数据
    name = request.values["name"]
    permissions = int(request.values["permissions"])
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

@api.route('/user/sign-up',  methods=['POST'])
def sign_up():

    '''
    只允许使用post方式请求
    :return:
    '''
    data = {"msg":None}
    # 获取前端post的数据
    username = request.values["username"]
    email = request.values["email"]
    password = request.values["password"]
    password2 = request.values["password2"]
    if not username.strip():
        data = {"msg":"名字不能为空"}
    elif not re.search(r"^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$",email.strip()):
        data = {"msg":"邮箱地址格式不对"}
    elif len(password.strip()) < 8:
        data = {"msg":"密码至少8个字符"}
    elif password.strip() != password2.strip():
        data = {"msg":"前后密码不一致"}
    else:
        # 获取一个角色,默认权重使用USER
        role_id = mongo.db.role.find_one({"permissions":config.Role.USER})["_id"]

        # 对密码加密处理
        password_hash = generate_password_hash(password)
        user = {"username":username.strip(),
                "email":email.strip(),
                "password":password_hash,
                "create_at":time.time(),
                "role_id":role_id
                }

        if mongo.db.user.find_one({"username":username.strip()}):
            data = {"msg":"用户名已存在"}
        elif mongo.db.user.find_one({"email":email.strip()}):
            data = {"msg":"此邮箱已被注册"}
        else:
            mongo.db.user.insert(user)
            data = {"msg":"注册成功", "url":"/sign-in"}
    return jsonify(data)


@api.route('/user/sign-in',  methods=['POST'])
def sign_in(adm = False):

    '''
    用户登录api
    :param adm:
    :return:
    '''

    data = {}
    if current_user.is_authenticated:
        data = {"msg":"已经登录", "url":"/"}
        return jsonify(data)
    username = request.values['username'].strip()
    password = request.values['password'].strip()
    remember_me = request.values['remember_me']

    # 判断用户是使用名字还是邮箱登录
    if "." in username and '@' in username:
        user = mongo.db.user.find_one({"email":username})
    else:
        user = mongo.db.user.find_one({"username":username})
    if user:
        user = User(user["_id"])
        # 密码验证
        if user.verify_password(password) and not user.is_delete:
            if user.is_active:
                login_user(user, remember_me)
                data = {"msg":"登录成功", "url":"/"}
            else:
                data = {"msg":"账户未激活"}
        else:
            data = {"msg":"账户或密码错误"}
    else:
        data = {"msg":"账户或密码错误"}
    return jsonify(data)

@api.route('/user/sign-out',  methods=['GET'])
@login_required
def sign_out():

    '''
    用户登录api
    :param adm:
    :return:
    '''
    logout_user()
    # 退出后跳到主页
    return redirect("/")


@api.route('/user/profile',  methods=['GET','POST'])
@login_required
def user_profile():
    '''
    只允许使用get和post方式请求
    :return:
    '''
    print current_user.is_root
    user = mongo.db.user.find_one({"_id":current_user.id})
    data = {"username":user["username"],
            "email":user["email"]}

    return jsonify(data)