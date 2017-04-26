#!/usr/bin/env python
# -*-coding:utf-8-*-
from bson.objectid import ObjectId
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from apps.config import Role
from apps.init_app import login_manger, mongo

__author__ = "Allen Woo"

class User(UserMixin):

    def __init__(self, id, **kwargs):
        super(User, self).__init__(**kwargs)
        user = mongo.db.user.find_one({'_id':ObjectId(id)})
        if user:
            self.id = ObjectId(id)
            self.username = user["username"]
            self.role_id = user["role_id"]
            self.password_hash = user["password"]
            '''
            教程中为了减少学习难度,用户注册信息并没有加入一下这两个字段,
            所以都默认,如果你有这两个注册信息,就指定为当前查询出来的值
            '''
            self.active = True
            self.is_delete = False
        else:
            return None

    @property
    def password(self):
        raise ArithmeticError(u'密码不能这样获取')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def auth_judge(self, permissions):
        role = mongo.db.role.find_one({"_id":self.role_id})
        return role and permissions <= role.permissions  and self.active and not self.is_delete

    def can(self, permissions):
        role = mongo.db.role.find_one({"_id":self.role_id})
        return role and permissions <= role["permissions"] and self.active and not self.is_delete

    def is_this_role(self, permissions):
        role = mongo.db.role.find_one({"_id":self.role_id})
        return role and permissions == role["permissions"] and self.active and not self.is_delete

    @property
    def is_administrator(self):
        return self.can(Role.ADMIN)

    @property
    def is_root(self):
        return self.can(Role.ROOT)

    @property
    def is_active(self):
        return self.active
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.username)

@login_manger.user_loader
def load_user(user_id):
    user = User(user_id)
    return user